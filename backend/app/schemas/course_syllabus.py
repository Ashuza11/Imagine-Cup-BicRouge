from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any


# Base class for CourseSyllabus
class CourseSyllabusBase(BaseModel):
    title: str
    content: str  # Syllabus content
    chapters: Optional[Dict[str, Any]] = None  # JSON for chapter-wise content


# Model for creating a CourseSyllabus
class CourseSyllabusCreate(CourseSyllabusBase):
    course_id: int  # Foreign key to associate with a course


# Model for reading a CourseSyllabus
class CourseSyllabusRead(CourseSyllabusBase):
    id: int
    course_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Model for updating a CourseSyllabus
class CourseSyllabusUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    chapters: Optional[Dict[str, Any]] = None
