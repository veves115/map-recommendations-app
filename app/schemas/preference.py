from pydantic import BaseModel
from typing import Optional

class PreferenceBase(BaseModel):
    category: str  # e.g., restaurantes, museos, parques
    subcategory: Optional[str] = None  # e.g., comida italiana, arte moderno
    
class PreferenceCreate(PreferenceBase):
    value: str

class PreferenceResponse(PreferenceBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True