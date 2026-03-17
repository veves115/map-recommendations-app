from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Preference(Base):
    __tablename__ = "preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String, nullable=False)  # restaurantes, museos, parques, etc.
    subcategory = Column(String, nullable=True)  # comida italiana, arte moderno, etc.
    
    # Relación con User
    user = relationship("User", back_populates="preferences")