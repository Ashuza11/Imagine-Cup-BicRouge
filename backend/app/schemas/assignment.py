from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Union, List


class AssignmentBase(BaseModel):
    title: str
    instruction: Optional[str] = None
    points: int
    composition: bool = False
    course_id: int
    due_date: Optional[datetime] = None
    chapters: Union[str, List[str]] = None
    questions_number: Optional[int] = None


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentRead(BaseModel):
    id: int
    title: str
    instruction: Optional[str]
    points: int
    composition: bool = False
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    course_id: int
    chapters: Optional[str]
    questions_number: Optional[int]

    class Config:
        from_attributes = True


class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    instruction: Optional[str] = None
    points: Optional[int] = None
    composition: bool = False
    due_date: Optional[datetime] = None
    course_id: Optional[int] = None
    chapter: Union[str, List[str]] = None
    questions_number: Optional[int] = None

    class Config:
        from_attributes = True
