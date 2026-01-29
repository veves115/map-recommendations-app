from sqlalchemy.orm import Session
from app.models.preference import Preference
from app.schemas.preference import PreferenceCreate

class PreferenceService:
    @staticmethod
    def get_user_preferences(db: Session, user_id: int) -> list[Preference]:
        """Returns list of user preferences"""
        return db.query(Preference).filter(Preference.user_id == user_id).all()
    
    @staticmethod
    def get_preference_by_id(db: Session, preference_id: int, user_id: int) -> Preference:
        return db.query(Preference).filter(
        Preference.id == preference_id,
        Preference.user_id == user_id  # Only return if user owns it!
    ).first()
    @staticmethod
    def create_preference(db: Session, user_id: int, preference_data: PreferenceCreate) -> Preference:
        """Creates a new preference for a user"""
        new_preference = Preference(user_id=user_id, category=preference_data.category, subcategory=preference_data.subcategory)
        db.add(new_preference)
        db.commit()
        db.refresh(new_preference)
        return new_preference
    @staticmethod
    def delete_preference(db: Session, preference: Preference) -> bool:
        db.delete(preference)
        db.commit()
        return True
    @staticmethod    
    def check_duplicate(db: Session, user_id: int, category: str, subcategory: str) -> bool:
        """Checks for duplicate preferences"""
        query = db.query(Preference).filter(
            Preference.user_id == user_id,
            Preference.category == category
        )
        if subcategory:
            query = query.filter(Preference.subcategory == subcategory)
        else:
            query = query.filter(Preference.subcategory.is_(None))
        existing = query.first()
        return existing is not None
