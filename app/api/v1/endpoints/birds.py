from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.BirdResponse)
def create_bird(*, db: Session = Depends(deps.get_db),
                bird_in: schemas.BirdCreate,) -> Any:
    """
        Create new bird.
    """
    # Check if bird already exists
    existing_bird = crud.bird.get_by_bird_id(db, bird_id=bird_in.bird_id)
    if existing_bird:
        raise HTTPException(
            status_code=400,
            detail="Bird with this ID already exists"
        )

    bird = crud.bird.create(db, obj_in=bird_in)
    return schemas.BirdResponse(success=True, data=bird)


@router.get("/", response_model=List[schemas.Bird])
def read_birds(db: Session = Depends(deps.get_db), skip: int = 0,
               limit: int = Query(default=100, le=100),) -> Any:
    """
        Retrieve birds.
    """
    birds = crud.bird.get_multi(db, skip=skip, limit=limit)
    return birds


@router.get("/{bird_id}", response_model=schemas.BirdResponse)
def read_bird(*, db: Session = Depends(deps.get_db), bird_id: str,) -> Any:
    """Get bird by ID."""
    bird = crud.bird.get_by_bird_id(db, bird_id=bird_id)
    if not bird:
        raise HTTPException(status_code=404, detail="Bird not found")
    return schemas.BirdResponse(success=True, data=bird)


@router.put("/{bird_id}", response_model=schemas.BirdResponse)
def update_bird(*, db: Session = Depends(deps.get_db), bird_id: str,
                bird_in: schemas.BirdUpdate,
                ) -> Any:
    """
        Update a bird.
    """
    bird = crud.bird.get_by_bird_id(db, bird_id=bird_id)
    if not bird:
        raise HTTPException(status_code=404, detail="Bird not found")
    bird = crud.bird.update(db, db_obj=bird, obj_in=bird_in)
    return schemas.BirdResponse(success=True, data=bird)


@router.delete("/{bird_id}", response_model=schemas.BirdResponse)
def delete_bird(*, db: Session = Depends(deps.get_db), bird_id: str,) -> Any:
    """
        Delete a bird.
    """
    bird = crud.bird.get_by_bird_id(db, bird_id=bird_id)
    if not bird:
        raise HTTPException(status_code=404, detail="Bird not found")
    bird = crud.bird.remove(db, id=bird.id)
    return schemas.BirdResponse(success=True, data=bird)


@router.get("/search/name", response_model=List[schemas.Bird])
def search_birds_by_name(
    *,
    db: Session = Depends(deps.get_db),
    name: str = Query(..., min_length=2, description="Bird name to search for"
                      ),) -> Any:
    """
        Search birds by name.
    """
    birds = crud.bird.search_by_name(db, name=name)
    return birds


@router.get("/search/scientific", response_model=List[schemas.Bird])
def search_birds_by_scientific_name(
    *,
    db: Session = Depends(deps.get_db),
    scientific_name: str = Query(..., min_length=3,
                                 description="Scientific name to search for"),
) -> Any:
    """
        Search birds by scientific name.
    """
    birds = crud.bird.search_by_scientific_name(
        db, scientific_name=scientific_name)
    return birds


@router.get("/filter/conservation", response_model=List[schemas.Bird])
def filter_birds_by_conservation_status(
    *,
    db: Session = Depends(deps.get_db),
    status: str = Query(..., description="Conservation status to filter by"),
) -> Any:
    """
        Filter birds by conservation status.
    """
    birds = crud.bird.get_by_conservation_status(db, status=status)
    return birds
