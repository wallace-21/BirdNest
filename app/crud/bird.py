from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.crud.base import CRUDBase
from app.models.bird import Bird
from app.schemas.bird import BirdCreate, BirdUpdate


class CRUDBird(CRUDBase[Bird, BirdCreate, BirdUpdate]):
    def get_by_bird_id(self, db: Session, *, bird_id: str) -> Optional[Bird]:
        """Get bird by bird_id (e.g., 'peregrine-falcon')."""
        return db.query(Bird).filter(Bird.bird_id == bird_id).first()

    def search_by_name(self, db: Session, *, name: str) -> List[Bird]:
        """Search birds by name (case-insensitive partial match)."""
        return db.query(Bird).filter(
            Bird.name.ilike(f"%{name}%")
        ).all()

    def search_by_scientific_name(self, db: Session, *, scientific_name: str
                                  ) -> List[Bird]:
        """Search birds by scientific name (case-insensitive partial match)."""
        return db.query(Bird).filter(
            Bird.scientific_name.ilike(f"%{scientific_name}%")
        ).all()

    def get_by_conservation_status(self, db: Session, *, status: str
                                   ) -> List[Bird]:
        """Get birds by conservation status."""
        return db.query(Bird).filter(
            func.json_extract(Bird.conservation_status, '$.status') == status
        ).all()


bird = CRUDBird(Bird)
