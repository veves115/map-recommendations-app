from typing import Optional
from sqlalchemy.orm import Session
from app.models.preference import Preference
from app.schemas.preference import PreferenceCreate


class PreferenceService:
    @staticmethod
    def get_user_preferences(db: Session, user_id: int, skip: int = 0, limit: int = 20) -> list[Preference]:
        """Returns list of user preferences"""
        return db.query(Preference).filter(Preference.user_id == user_id).offset(skip).limit(limit).all()

    @staticmethod
    def get_preference_by_id(db: Session, preference_id: int, user_id: int) -> Preference:
        """Returns a single preference by ID, only if it belongs to user_id"""
        return db.query(Preference).filter(
            Preference.id == preference_id,
            Preference.user_id == user_id
        ).first()

    @staticmethod
    def create_preference(db: Session, user_id: int, preference_data: PreferenceCreate) -> Preference:
        """Creates a new preference for a user"""
        new_preference = Preference(
            user_id=user_id,
            category=preference_data.category,
            subcategory=preference_data.subcategory
        )
        db.add(new_preference)
        db.commit()
        db.refresh(new_preference)
        return new_preference

    @staticmethod
    def update_preference(
        db: Session,
        preference: Preference,
        category: Optional[str],
        subcategory: Optional[str]
    ) -> Preference:
        """
        Updates an existing preference with the provided fields.
        Only non-None values are applied so callers can do partial updates.
        """
        if category is not None:
            preference.category = category
        if subcategory is not None:
            preference.subcategory = subcategory
        db.commit()
        db.refresh(preference)
        return preference

    @staticmethod
    def delete_preference(db: Session, preference: Preference) -> bool:
        """Deletes a preference from the database"""
        db.delete(preference)
        db.commit()
        return True

    @staticmethod
    def check_duplicate(db: Session, user_id: int, category: str, subcategory: Optional[str]) -> bool:
        """
        Returns True if the user already has a preference with the same
        category + subcategory combination.
        """
        query = db.query(Preference).filter(
            Preference.user_id == user_id,
            Preference.category == category
        )
        if subcategory:
            query = query.filter(Preference.subcategory == subcategory)
        else:
            query = query.filter(Preference.subcategory.is_(None))
        return query.first() is not None
