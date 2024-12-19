from .session import Base, engine, SessionLocal

from models.user_models import *
from backend.app.models.operation_models1 import *


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
