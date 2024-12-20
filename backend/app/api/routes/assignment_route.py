from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Optional, Union
from db.init_db import get_db
from crud.assignment_crud import (
    create_assignment,
    get_all_assignments,
    get_assignment,
    delete_assignment,
    update_assignment,
    get_student_assignments,
)
from schemas.assignment import AssignmentCreate, AssignmentRead, AssignmentUpdate
from core.security import check_user_active
from services.generate_questions import (
    compose_evaluation,
)

router = APIRouter()


@router.post("/assignments", response_model=AssignmentRead)
async def create_new_assignment(
    assignment: AssignmentCreate,
    user=Depends(check_user_active),
    db: Session = Depends(get_db),
):
    """
    Create a new assignment.

    Parameters:
    - assignment: AssignmentCreate - The assignment data to create.
    - user: Depends(check_user_active) - The active user making the request.
    - db: Session - The database session.

    Returns:
    - AssignmentRead: The created assignment data.
    """

    return await create_assignment(user=user, db=db, assignment=assignment)


@router.get("/courses/{course_id}/assignments", response_model=List[AssignmentRead])
async def fetch_all_assignments(
    course_id: int,
    user=Depends(check_user_active),
    db: Session = Depends(get_db),
):
    """
    Get all assignments for a course.

    Parameters:
    - course_id: int - The ID of the course.
    - user: Depends(check_user_active) - The active user making the request.
    - db: Session - The database session.

    Returns:
    - List[AssignmentRead]: A list of assignments for the specified course.
    """
    return await get_all_assignments(user=user, db=db, course_id=course_id)


@router.get("/assignments/{assignment_id}", response_model=AssignmentRead)
async def fetch_assignment(
    assignment_id: int,
    user=Depends(check_user_active),
    db: Session = Depends(get_db),
):
    """
    Get a specific assignment by ID.

    Parameters:
    - assignment_id: int - The ID of the assignment.
    - user: Depends(check_user_active) - The active user making the request.
    - db: Session - The database session.

    Returns:
    - AssignmentRead: The assignment data.
    """

    return await get_assignment(assignment_id, user, db)


@router.delete("/assignments/{assignment_id}", status_code=200)
async def delete_existing_assignment(
    assignment_id: int, user=Depends(check_user_active), db: Session = Depends(get_db)
):
    """
    Delete an assignment by ID.

    Parameters:
    - assignment_id: int - The ID of the assignment.
    - user: Depends(check_user_active) - The active user making the request.
    - db: Session - The database session.

    Returns:
    - dict: A message indicating successful deletion.
    """
    await delete_assignment(assignment_id, user, db)
    return {"message": "Assignment successfully deleted"}


@router.put("/assignments/{assignment_id}", response_model=AssignmentRead)
async def update_existing_assignment(
    assignment_id: int,
    assignment: AssignmentUpdate,
    user=Depends(check_user_active),
    db: Session = Depends(get_db),
):
    """
    Update an assignment by ID.

    Parameters:
    - assignment_id: int - The ID of the assignment.
    - assignment: AssignmentUpdate - The updated assignment data.
    - user: Depends(check_user_active) - The active user making the request.
    - db: Session - The database session.

    Returns:
    - AssignmentRead: The updated assignment data.
    """
    return await update_assignment(assignment_id, assignment, user, db)


@router.get(
    "/students/{student_id}/courses/{course_id}/assignments",
    response_model=List[AssignmentRead],
)
async def fetch_student_assignments(
    student_id: int,
    course_id: int,
    user=Depends(check_user_active),
    db: Session = Depends(get_db),
):
    """
    Get all assignments for a student in a specific course.

    Parameters:
    - student_id: int - The ID of the student.
    - course_id: int - The ID of the course.
    - user: Depends(check_user_active) - The active user making the request.
    - db: Session - The database session.

    Returns:
    - List[AssignmentRead]: A list of assignments for the specified student and course.
    """
    return await get_student_assignments(
        user=user, db=db, student_id=student_id, course_id=course_id
    )


@router.post("/assignments/{assignment_id}/compose_evaluation/")
async def generate_evaluation(
    assignment_id: int,
    course_id: int,
    question_number: int,
    # chapters: Optional[str],
    db: Session = Depends(get_db),
):
    try:
        result = await compose_evaluation(
            db=db,
            assignment_id=assignment_id,
            course_id=course_id,
            question_number=question_number,
            # chapters=chapters,
        )
        return result  # return the result as a dictionary
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
