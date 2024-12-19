from datetime import datetime
from db.session import Base
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    Float,
    JSON,
)
from sqlalchemy.orm import relationship


class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    section = Column(String)
    subject = Column(String)
    code = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    url = Column(String, nullable=True)
    course_chapters = Column(JSON, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    teacher = relationship("Teacher", back_populates="courses")
    assignments = relationship(
        "Assignment", back_populates="course", cascade="all, delete-orphan"
    )
    enrollments = relationship(
        "Enrollment", back_populates="course", foreign_keys="Enrollment.course_id"
    )


# Added Features :
# 1. For Syllabus Management


# class CourseSyllabus(Base):
#     __tablename__ = "course_syllabus"
#     id = Column(Integer, primary_key=True)
#     title = Column(String, nullable=False)
#     url = Column(String, nullable=True)
#     content = Column(Text, nullable=False)  # Syllabus content
#     chapters = Column(JSON, nullable=True)  # Store chapters as a list of dictionaries
#     # Example JSON for chapters
#     # [
#     #     {
#     #         "chapter_number": 1,
#     #         "title": "Introduction to Python",
#     #         "topics": [
#     #             "History of Python",
#     #             "Setting up the environment",
#     #             "Basic Syntax"
#     #         ]
#     #     },
#     #     {
#     #         "chapter_number": 2,
#     #         "title": "Data Structures",
#     #         "topics": [
#     #             "Lists",
#     #             "Tuples",
#     #             "Dictionaries",
#     #             "Sets"
#     #         ]
#     #     }
#     # ]
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#     course_id = Column(Integer, ForeignKey("course.id"))
#     course = relationship("Course", back_populates="syllabus")


class Enrollment(Base):
    __tablename__ = "enrollment"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    state = Column(
        String, nullable=False, default="enrolled"
    )  # enrolled, completed, failed
    student_id = Column(Integer, ForeignKey("student.id"))
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    student = relationship("Student", back_populates="enrollments")
    course_code = Column(String, ForeignKey("course.code"))
    course = relationship(
        "Course", back_populates="enrollments", foreign_keys=[course_id]
    )


class Assignment(Base):
    __tablename__ = "assignment"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    instruction = Column(Text)
    points = Column(Integer, nullable=False)
    composition = Column(
        Boolean, default=False
    )  # (False, True) doesn't have composition, has composition
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    course_id = Column(Integer, ForeignKey("course.id"))
    course = relationship("Course", back_populates="assignments")
    questions = relationship(
        "Question", back_populates="assignment", cascade="all, delete-orphan"
    )
    student_responses = relationship(
        "StudentResponse", back_populates="assignment", cascade="all, delete-orphan"
    )
    feedbacks = relationship(
        "Feedback", back_populates="assignment", cascade="all, delete-orphan"
    )
    is_generated = Column(
        Boolean, default=False
    )  # Attribute to specify if the questions were generated


# class GeneratedAssignment(Base):
#     __tablename__ = "generated_evaluation"

#     # Columns
#     id = Column(Integer, primary_key=True)
#     title = Column(String, nullable=False)
#     description = Column(
#         Text, nullable=True
#     )  # when a section of the course syllabus is selected
#     course_syllabus_id = Column(
#         Integer, ForeignKey("course_syllabus.id"), nullable=True
#     )  # Optional for whole syllabus
#     # course_syllabus = relationship("SyllabusContext", back_populates="evaluations")
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     # Relationships
#     questions = relationship(
#         "Question", back_populates="generated_evaluation", cascade="all, delete-orphan"
#     )
#     student_responses = relationship(
#         "StudentResponse",
#         back_populates="generated_evaluation",
#         cascade="all, delete-orphan",
#     )
#     feedbacks = relationship(
#         "Feedback", back_populates="generated_evaluation", cascade="all, delete-orphan"
#     )


class TeacherResponse(Base):
    __tablename__ = "teacher_response"

    id = Column(Integer, primary_key=True, index=True)
    response_text = Column(Text, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"), nullable=False)
    question = relationship("Question", back_populates="teacher_responses")


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    max_points = Column(Integer, nullable=False)
    assignment_id = Column(Integer, ForeignKey("assignment.id"), nullable=True)
    assignment = relationship("Assignment", back_populates="questions")
    # generated_evaluation_id = Column(
    #     Integer, ForeignKey("generated_evaluation.id"), nullable=True
    # )
    # generated_evaluation = relationship(
    #     "GeneratedEvaluation", back_populates="questions"
    # )
    student_responses = relationship(
        "StudentResponse", back_populates="question", cascade="all, delete-orphan"
    )
    teacher_responses = relationship(
        "TeacherResponse", back_populates="question", cascade="all, delete-orphan"
    )
    # question_type_id = Column(Integer, ForeignKey("question_type.id"))
    # question_type = relationship("QuestionType", back_populates="questions")


# To Review


# # 2. For Question Types
# class QuestionType(Base):
#     __tablename__ = "question_type"
#     id = Column(Integer, primary_key=True)
#     name = Column(
#         String, nullable=False
#     )  # e.g., "multiple_choice", "open_ended", "illustrative"
#     configuration = Column(JSON, nullable=True)  # Store type-specific configuration
#     questions = relationship("Question", back_populates="question_type")


# # 3. For Multiple Choice Options
# class QuestionOption(Base):
#     __tablename__ = "question_option"
#     id = Column(Integer, primary_key=True)
#     content = Column(Text, nullable=False)
#     is_correct = Column(Boolean, default=False)
#     question_id = Column(Integer, ForeignKey("question.id"))
#     question = relationship("Question", back_populates="options")


# class GradingCriteria(Base):
#     __tablename__ = "grading_criteria"
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     description = Column(Text, nullable=True)
#     rules = Column(JSON, nullable=False)  # JSON for flexible rule definitions
#     course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
#     course = relationship("Course", back_populates="grading_criteria")
#     created_at = Column(DateTime, default=datetime.utcnow)


class StudentResponse(Base):
    __tablename__ = "student_response"
    id = Column(Integer, primary_key=True)
    response_text = Column(Text, nullable=False)
    grade = Column(Float, nullable=True)
    grades = Column(JSON, nullable=True)
    comment = Column(Text, nullable=True)
    file = Column(String, nullable=True)
    assignment_id = Column(Integer, ForeignKey("assignment.id"))
    assignment = relationship("Assignment", back_populates="student_responses")
    # generated_evaluation_id = Column(
    #     Integer, ForeignKey("generated_evaluation.id"), nullable=True
    # )
    # generated_evaluation = relationship(
    #     "GeneratedEvaluation", back_populates="student_responses"
    # )
    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship("Question", back_populates="student_responses")
    feedback = relationship(
        "Feedback", back_populates="student_response", uselist=False
    )


class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    advice = Column(Text, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    state = Column(Boolean, default=False)  # (False, True) disapproved, approved
    assignment_id = Column(Integer, ForeignKey("assignment.id"), nullable=True)
    assignment = relationship("Assignment", back_populates="feedbacks")
    # generated_evaluation_id = Column(
    #     Integer, ForeignKey("generated_evaluation.id"), nullable=True
    # )
    # generated_evaluation = relationship(
    #     "GeneratedEvaluation", back_populates="feedbacks"
    # )
    student_response_id = Column(
        Integer, ForeignKey("student_response.id"), unique=True
    )
    student_response = relationship("StudentResponse", back_populates="feedback")


# class SyllabusContext(Base):
#     evaluations = relationship(
#         "GeneratedEvaluation",
#         back_populates="syllabus_context",
#         cascade="all, delete-orphan",
#     )
