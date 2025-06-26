from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FitnessData(BaseModel):
    id: str
    device_id: str
    timestamp: datetime
    heart_rate: Optional[int] = None
    steps: Optional[int] = None 