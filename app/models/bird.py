from sqlalchemy import Column, String, JSON
from .base import BaseModel


class Bird(BaseModel):
    """
        Bird model based on the JSON structure.
    """
    __tablename__ = "birds"

    # Basic info
    bird_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    scientific_name = Column(String, nullable=False)

    # Conservation status
    conservation_status = Column(JSON)  # Stores the entire conservation
    # status object

    # Quick facts
    quick_facts = Column(JSON)  # Array of fact objects

    # Tags
    tags = Column(JSON)  # Array of tag objects

    # Images
    images = Column(JSON)  # Contains main and gallery images

    # Overview sections
    overview = Column(JSON)  # About, physical characteristics, conservation

    # Habitat and distribution
    habitat_and_distribution = Column(JSON)  # Habitat, distribution, migration

    # Diet and behavior
    diet_and_behavior = Column(JSON)  # Diet, hunting, lifecycle

    # Sounds
    sounds = Column(JSON)  # Vocalizations and sound information

    # Related birds
    related_birds = Column(JSON)  # Array of related bird objects

    # Metadata
    meta_data = Column(JSON)  # Last updated, contributors, sources, tags
