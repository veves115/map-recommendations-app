from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.location import Location
from app.schemas.location import LocationCreate


class LocationService:
    @staticmethod
    def create_location(db: Session, user_id: int, location_data: LocationCreate) -> Location:
        """
        Persists a new location record for the given user.

        Args:
            db: SQLAlchemy database session
            user_id: ID of the authenticated user
            location_data: Validated payload with latitude, longitude and optional place_name

        Returns:
            The newly created Location ORM instance.
        """
        new_location = Location(
            user_id=user_id,
            latitude=location_data.latitude,
            longitude=location_data.longitude,
            place_name=location_data.place_name
        )
        db.add(new_location)
        db.commit()
        db.refresh(new_location)
        return new_location

    @staticmethod
    def get_user_locations(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 20
    ) -> List[Location]:
        """
        Returns a paginated list of location records for the given user,
        ordered from most recent to oldest.

        Args:
            db: SQLAlchemy database session
            user_id: ID of the authenticated user
            skip: Number of records to skip (pagination offset)
            limit: Maximum number of records to return

        Returns:
            List of Location ORM instances.
        """
        return (
            db.query(Location)
            .filter(Location.user_id == user_id)
            .order_by(Location.timestamp.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_latest_location(db: Session, user_id: int) -> Optional[Location]:
        """
        Returns the most recent location record for the given user,
        or None if the user has no recorded locations.

        Args:
            db: SQLAlchemy database session
            user_id: ID of the authenticated user

        Returns:
            The most recent Location ORM instance or None.
        """
        return (
            db.query(Location)
            .filter(Location.user_id == user_id)
            .order_by(Location.timestamp.desc())
            .first()
        )
