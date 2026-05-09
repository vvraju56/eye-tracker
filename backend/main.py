from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import List
import uuid

from database import (
    get_db,
    Session as SessionModel,
    FocusLog as FocusLogModel,
    Base,
    engine,
)
from schemas import (
    SessionCreate,
    SessionResponse,
    FocusLogCreate,
    FocusLogResponse,
    StatsResponse,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Eye Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Eye Tracker API", "status": "running"}


@app.post("/sessions", response_model=SessionResponse)
def create_session(device_id: str, db: Session = Depends(get_db)):
    session = SessionModel(device_id=device_id, start_time=datetime.utcnow())
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@app.post("/sessions/{session_id}/end")
def end_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session.end_time = datetime.utcnow()
    db.commit()
    db.refresh(session)
    return session


@app.post("/sessions/{session_id}/logs", response_model=FocusLogResponse)
def create_focus_log(
    session_id: int, log: FocusLogCreate, db: Session = Depends(get_db)
):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    focus_log = FocusLogModel(
        session_id=session_id,
        timestamp=log.timestamp,
        status=log.status.value,
        duration_ms=log.duration_ms,
        gaze_x=log.gaze_x,
        gaze_y=log.gaze_y,
        reason=log.reason,
    )

    if log.status.value == "focused":
        session.total_focus_time += log.duration_ms / 1000
    else:
        session.total_distracted_time += log.duration_ms / 1000

    db.add(focus_log)
    db.commit()
    db.refresh(focus_log)
    return focus_log


@app.get("/sessions/{session_id}", response_model=SessionResponse)
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@app.get("/stats/{device_id}", response_model=StatsResponse)
def get_stats(device_id: str, db: Session = Depends(get_db)):
    sessions = db.query(SessionModel).filter(SessionModel.device_id == device_id).all()

    if not sessions:
        return StatsResponse(
            total_sessions=0,
            total_focus_time=0,
            total_distracted_time=0,
            focus_percentage=0,
            average_session_duration=0,
        )

    total_focus = sum(s.total_focus_time for s in sessions)
    total_distracted = sum(s.total_distracted_time for s in sessions)
    total_time = total_focus + total_distracted

    focus_percentage = (total_focus / total_time * 100) if total_time > 0 else 0

    completed_sessions = [s for s in sessions if s.end_time]
    avg_duration = (
        sum((s.end_time - s.start_time).total_seconds() for s in completed_sessions)
        / len(completed_sessions)
        if completed_sessions
        else 0
    )

    return StatsResponse(
        total_sessions=len(sessions),
        total_focus_time=total_focus,
        total_distracted_time=total_distracted,
        focus_percentage=round(focus_percentage, 2),
        average_session_duration=round(avg_duration, 2),
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
