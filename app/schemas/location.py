from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LocationBase(BaseModel):
    latitude: float
    longitude: float
    place_name: Optional[str] = None
    
class LocationCreate(LocationBase):
    pass

class LocationResponse(LocationBase):
    id: int
    user_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True