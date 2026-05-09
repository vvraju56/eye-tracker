from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./eyetracker.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    total_focus_time = Column(Float, default=0.0)
    total_distracted_time = Column(Float, default=0.0)

    focus_logs = relationship("FocusLog", back_populates="session")


class FocusLog(Base):
    __tablename__ = "focus_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    timestamp = Column(DateTime)
    status = Column(String)
    duration_ms = Column(Integer)
    gaze_x = Column(Float, nullable=True)
    gaze_y = Column(Float, nullable=True)
    reason = Column(String, nullable=True)

    session = relationship("Session", back_populates="focus_logs")


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
