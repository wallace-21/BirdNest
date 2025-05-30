import pytest
from sqlalchemy.orm import Session
from app import crud, schemas


class TestBirdCRUD:

    def test_create_bird(self, db: Session, sample_bird_data):
        """Test creating a bird via CRUD."""
        bird_in = schemas.BirdCreate(**sample_bird_data)
        bird = crud.bird.create(db=db, obj_in=bird_in)

        assert bird.bird_id == sample_bird_data["bird_id"]
        assert bird.name == sample_bird_data["name"]
        assert bird.scientific_name == sample_bird_data["scientific_name"]
        assert bird.id is not None
        assert bird.created_at is not None
        assert bird.updated_at is not None

    def test_get_bird_by_id(self, db: Session, sample_bird_data):
        """Test getting a bird by database ID."""
        bird_in = schemas.BirdCreate(**sample_bird_data)
        created_bird = crud.bird.create(db=db, obj_in=bird_in)

        stored_bird = crud.bird.get(db=db, id=created_bird.id)
        assert stored_bird
        assert stored_bird.id == created_bird.id
        assert stored_bird.bird_id == sample_bird_data["bird_id"]

    def test_get_bird_by_bird_id(self, db: Session, sample_bird_data):
        """Test getting a bird by bird_id."""
        bird_in = schemas.BirdCreate(**sample_bird_data)
        crud.bird.create(db=db, obj_in=bird_in)

        stored_bird = crud.bird.get_by_bird_id(
            db=db, bird_id=sample_bird_data["bird_id"])
        assert stored_bird
        assert stored_bird.bird_id == sample_bird_data["bird_id"]
        assert stored_bird.name == sample_bird_data["name"]

    def test_update_bird(self, db: Session, sample_bird_data):
        """Test updating a bird."""
        bird_in = schemas.BirdCreate(**sample_bird_data)
        created_bird = crud.bird.create(db=db, obj_in=bird_in)

        new_name = "Updated Test Falcon"
        bird_update = schemas.BirdUpdate(name=new_name)
        updated_bird = crud.bird.update(
            db=db, db_obj=created_bird, obj_in=bird_update)

        assert updated_bird.id == created_bird.id
        assert updated_bird.name == new_name
        assert updated_bird.bird_id == sample_bird_data["bird_id"]
        # Should remain unchanged

    def test_delete_bird(self, db: Session, sample_bird_data):
        """Test deleting a bird."""
        bird_in = schemas.BirdCreate(**sample_bird_data)
        created_bird = crud.bird.create(db=db, obj_in=bird_in)

        deleted_bird = crud.bird.remove(db=db, id=created_bird.id)
        assert deleted_bird.id == created_bird.id

        # Verify bird is deleted
        stored_bird = crud.bird.get(db=db, id=created_bird.id)
        assert stored_bird is None

    def test_search_birds_by_name(self, db: Session, sample_bird_data):
        """Test searching birds by name."""
        bird_in = schemas.BirdCreate(**sample_bird_data)
        crud.bird.create(db=db, obj_in=bird_in)

        # Search by partial name
        found_birds = crud.bird.search_by_name(db=db, name="Test")
        assert len(found_birds) >= 1
        assert any(bird.name == sample_bird_data["name"]
                   for bird in found_birds)

        # Search by full name (case insensitive)
        found_birds = crud.bird.search_by_name(db=db, name="test falcon")
        assert len(found_birds) >= 1

    def test_search_birds_by_scientific_name(self, db: Session,
                                             sample_bird_data):
        """Test searching birds by scientific name."""
        bird_in = schemas.BirdCreate(**sample_bird_data)
        crud.bird.create(db=db, obj_in=bird_in)

        # Search by partial scientific name
        found_birds = crud.bird.search_by_scientific_name(
            db=db, scientific_name="testicus")
        assert len(found_birds) >= 1
        assert any(bird.scientific_name == sample_bird_data["scientific_name"]
                   for bird in found_birds)

    def test_get_birds_by_conservation_status(self, db: Session,
                                              sample_bird_data):
        """Test filtering birds by conservation status."""
        bird_in = schemas.BirdCreate(**sample_bird_data)
        crud.bird.create(db=db, obj_in=bird_in)

        found_birds = crud.bird.get_by_conservation_status(
            db=db, status="least-concern")
        assert len(found_birds) >= 1
        assert any(
            bird.conservation_status["status"] == "least-concern"
            for bird in found_birds
        )

    def test_get_multi_birds(self, db: Session, sample_bird_data):
        """Test getting multiple birds with pagination."""
        # Create multiple birds
        for i in range(3):
            bird_data = sample_bird_data.copy()
            bird_data["bird_id"] = f"test-falcon-{i}"
            bird_data["name"] = f"Test Falcon {i}"
            bird_in = schemas.BirdCreate(**bird_data)
            crud.bird.create(db=db, obj_in=bird_in)

        # Test pagination
        birds = crud.bird.get_multi(db=db, skip=0, limit=2)
        assert len(birds) == 2

        birds = crud.bird.get_multi(db=db, skip=2, limit=2)
        assert len(birds) >= 1
