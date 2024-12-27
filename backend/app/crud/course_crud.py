import random
import string
from typing import List
from sqlalchemy.orm import Session, joinedload
from pydantic import HttpUrl
import requests
from io import BytesIO
from PyPDF2 import PdfReader
from fastapi import HTTPException
from datetime import datetime
from models.operation_models import Course, Enrollment
from models.user_models import Teacher, Student
from schemas.course import CourseCreate, CourseUpdate, CourseRead
from schemas.teacher import TeacherRead
from services.course_chapters import extract_chapters_from_syllabus


def generate_course_code(length=7):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


# Step 1: Download the PDF file
async def download_pdf(syllabus_url: HttpUrl) -> BytesIO:
    try:
        response = requests.get(syllabus_url)
        response.raise_for_status()
        return BytesIO(response.content)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error downloading syllabus PDF: {str(e)}"
        )


# Step 2: Extract text from the PDF
async def extract_text_from_pdf(pdf_content: BytesIO) -> str:
    try:
        reader = PdfReader(pdf_content)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text.strip()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error extracting text from PDF: {str(e)}"
        )


# Main function to create a course
async def create_course(
    user: TeacherRead, db: Session, course: CourseCreate
) -> CourseRead:
    # Generate a unique course code
    while True:
        course_code = generate_course_code()
        existing_course = db.query(Course).filter_by(code=course_code).first()
        if not existing_course:
            break

    # Download the syllabus PDF
    if not course.syllabus_url:
        raise HTTPException(status_code=400, detail="Syllabus URL is required")

    pdf_content = await download_pdf(course.syllabus_url)

    # Extract syllabus content from the PDF
    syllabus_content = await extract_text_from_pdf(pdf_content)
    # Extract chapters from the syllabus content using the LLM
    course_chapters = await extract_chapters_from_syllabus(syllabus_content)
    print(course_chapters)

    # Create the course object
    db_course = Course(
        name=course.name,
        section=course.section,
        subject=course.subject,
        teacher_id=course.teacher_id,
        code=course_code,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        syllabus_url=course.syllabus_url,
        syllabus_content=syllabus_content,
        course_chapters=course_chapters,
    )

    # Add to database
    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    # Prepare the response
    return CourseRead(
        id=db_course.id,
        name=db_course.name,
        section=db_course.section,
        subject=db_course.subject,
        code=db_course.code,
        teacher_name=db_course.teacher.name,
        created_at=db_course.created_at,
        updated_at=db_course.updated_at,
        syllabus_url=db_course.syllabus_url,
    )


async def get_all_courses(user: TeacherRead, db: Session) -> List[CourseRead]:
    courses = db.query(Course).filter(Course.teacher_id == user.id).all()
    course_list = []
    for course in courses:
        course_data = course.__dict__.copy()
        course_data["teacher_name"] = (
            f"{course.teacher.name} {course.teacher.postname or ''} {course.teacher.last_name or ''}".strip()
            if course.teacher
            else None
        )
        course_read = CourseRead(**course_data)
        course_list.append(course_read)
    return course_list


# Select a course
async def course_selector(course_id: int, user: TeacherRead, db: Session):
    # Use `joinedload` to eagerly load the teacher relationship
    course = (
        db.query(Course)
        .options(joinedload(Course.teacher))
        .filter_by(teacher_id=user.id)
        .filter_by(id=course_id)
        .first()
    )
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


async def get_course(course_id: int, user: TeacherRead, db: Session):
    course = await course_selector(course_id, user, db)
    # Constructing the full teacher name
    if course.teacher:
        teacher_full_name = f"{course.teacher.name} {course.teacher.postname or ''} {course.teacher.last_name or ''}".strip()
    else:
        teacher_full_name = None

    course_data = CourseRead.from_orm(course)
    course_data.teacher_name = teacher_full_name
    return course_data


async def delete_course(course_id: int, user: TeacherRead, db: Session):
    course = await course_selector(course_id, user, db)
    db.delete(course)
    db.commit()


async def update_course(
    course_id: int, course: CourseUpdate, user: TeacherRead, db: Session
):
    db_course = await course_selector(course_id, user, db)
    for key, value in course.dict(exclude_unset=True).items():
        if key == "teacher_id":
            continue
        setattr(db_course, key, value)
    db_course.updated_at = datetime.now()
    db.commit()
    db.refresh(db_course)
    return CourseRead.from_orm(db_course)


# Get all course chapters and their IDs
async def get_chapters_by_course_id(course_id: int, db: Session):
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        return None

    return course.course_chapters


# Get the teacher and a list of all of students who joined a course
def get_teacher_and_students(
    db: Session,
    course_id: int,
):
    # Query to get the course and associated teacher
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        return None

    # Fetch the teacher associated with the course
    teacher = db.query(Teacher).filter(Teacher.id == course.teacher_id).first()

    if not teacher:
        return None

    # Fetch the list of students enrolled in the course
    students_query = (
        db.query(Student)
        .join(Enrollment, Enrollment.student_id == Student.id)
        .filter(Enrollment.course_id == course_id)
    )

    students = students_query.all()

    # Prepare the response
    result = {
        "teacher": {
            "id": teacher.id,
            "name": f"{teacher.name} {teacher.postname}",
            "email": teacher.email,
        },
        "students": [
            {
                "id": student.id,
                "name": f"{student.name} {student.postname}",
                "email": student.email,
            }
            for student in students
        ],
    }

    return result
