from datetime import datetime
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
from db.session import Base


class SyllabusContext(Base):
    __tablename__ = "syllabus_context"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    course = relationship("Course", back_populates="syllabus_contexts")
    created_at = Column(DateTime, default=datetime.utcnow)


class GeneratedEvaluation(Base):
    __tablename__ = "generated_evaluation"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    syllabus_context_id = Column(
        Integer, ForeignKey("syllabus_context.id"), nullable=False
    )
    syllabus_context = relationship("SyllabusContext", back_populates="evaluations")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    questions = relationship(
        "Question", back_populates="generated_evaluation", cascade="all, delete-orphan"
    )


class QuestionType(Base):
    __tablename__ = "question_type"
    id = Column(Integer, primary_key=True)
    name = Column(
        String, nullable=False
    )  # e.g., "multiple_choice", "open_ended", "illustrative"
    configuration = Column(JSON, nullable=True)  # Store type-specific configuration
    questions = relationship("Question", back_populates="question_type")


class QuestionOption(Base):
    __tablename__ = "question_option"
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship("Question", back_populates="options")


class GradingCriteria(Base):
    __tablename__ = "grading_criteria"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    rules = Column(JSON, nullable=False)  # JSON for flexible rule definitions
    course_id = Column(Integer, ForeignKey("course.id"), nullable=False)
    course = relationship("Course", back_populates="grading_criteria")
    created_at = Column(DateTime, default=datetime.utcnow)


# Adjust existing models to include relationships
class Course(Base):
    __tablename__ = "course"
    # Existing columns
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    section = Column(String)
    subject = Column(String)
    code = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    teacher = relationship("Teacher", back_populates="courses")
    assignments = relationship(
        "Assignment", back_populates="course", cascade="all, delete-orphan"
    )
    enrollments = relationship(
        "Enrollment", back_populates="course", foreign_keys="Enrollment.course_id"
    )
    syllabus_contexts = relationship(
        "SyllabusContext", back_populates="course", cascade="all, delete-orphan"
    )
    grading_criteria = relationship(
        "GradingCriteria", back_populates="course", cascade="all, delete-orphan"
    )


class Question(Base):
    __tablename__ = "question"
    # Existing columns
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    max_points = Column(Integer, nullable=False)
    assignment = relationship("Assignment", back_populates="questions")
    assignment_id = Column(Integer, ForeignKey("assignment.id"))
    student_responses = relationship(
        "StudentResponse", back_populates="question", cascade="all, delete-orphan"
    )
    teacher_responses = relationship(
        "TeacherResponse", back_populates="question", cascade="all, delete-orphan"
    )
    # New relationships
    question_type_id = Column(Integer, ForeignKey("question_type.id"), nullable=False)
    question_type = relationship("QuestionType", back_populates="questions")
    options = relationship(
        "QuestionOption", back_populates="question", cascade="all, delete-orphan"
    )
    generated_evaluation_id = Column(
        Integer, ForeignKey("generated_evaluation.id"), nullable=True
    )
    generated_evaluation = relationship(
        "GeneratedEvaluation", back_populates="questions"
    )


class SyllabusContext(Base):
    evaluations = relationship(
        "GeneratedEvaluation",
        back_populates="syllabus_context",
        cascade="all, delete-orphan",
    )
