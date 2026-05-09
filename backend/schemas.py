from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class FocusStatus(str, Enum):
    FOCUSED = "focused"
    DISTRACTED = "distracted"
    NO_FACE = "no_face"


class SessionCreate(BaseModel):
    device_id: str
    start_time: datetime


class SessionResponse(BaseModel):
    id: int
    device_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    total_focus_time: float = 0.0
    total_distracted_time: float = 0.0

    class Config:
        from_attributes = True


class FocusLogCreate(BaseModel):
    session_id: int
    timestamp: datetime
    status: FocusStatus
    duration_ms: int
    gaze_x: Optional[float] = None
    gaze_y: Optional[float] = None
    reason: Optional[str] = None


class FocusLogResponse(BaseModel):
    id: int
    session_id: int
    timestamp: datetime
    status: FocusStatus
    duration_ms: int
    gaze_x: Optional[float] = None
    gaze_y: Optional[float] = None
    reason: Optional[str] = None

    class Config:
        from_attributes = True


class StatsResponse(BaseModel):
    total_sessions: int
    total_focus_time: float
    total_distracted_time: float
    focus_percentage: float
    average_session_duration: float
