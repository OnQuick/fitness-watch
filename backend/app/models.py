from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FitnessData(BaseModel):
    id: str
    device_id: str
    timestamp: datetime
    heart_rate: Optional[int] = None
    steps: Optional[int] = None
    calories: Optional[int] = None
    distance: Optional[float] = None
    sleep_hours: Optional[float] = None

class FitnessDataCreate(BaseModel):
    device_id: str
    heart_rate: Optional[int] = None
    steps: Optional[int] = None
    calories: Optional[int] = None
    distance: Optional[float] = None
    sleep_hours: Optional[float] = None

class FitnessStats(BaseModel):
    device_id: str
    period_days: int
    total_steps: int
    avg_heart_rate: float
    total_calories: int
    total_distance: float
    avg_sleep_hours: float
    data_points_count: int 