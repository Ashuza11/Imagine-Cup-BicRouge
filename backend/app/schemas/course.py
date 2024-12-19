from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional, List, Dict


class CourseBase(BaseModel):
    name: str
    section: Optional[str]
    subject: Optional[str]
    syllabus_url: Optional[str] = None
    # course_chapters: Optional[List[Dict]] = None


class CourseCreate(CourseBase):
    teacher_id: int
    syllabus_url: Optional[str] = None


class CourseRead(CourseBase):
    id: int
    code: str
    teacher_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CourseUpdate(CourseBase):
    pass
