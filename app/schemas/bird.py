from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


# Individual component schemas
class QuickFact(BaseModel):
    label: str
    value: str
    icon: str


class Tag(BaseModel):
    text: str
    icon: str
    class_: Optional[str] = Field(None, alias="class")


class ImageInfo(BaseModel):
    url: str
    alt: str
    caption: str


class Images(BaseModel):
    main: List[ImageInfo]
    gallery: List[ImageInfo]


class ConservationStatus(BaseModel):
    status: str
    label: str
    description: str
    currentThreats: List[str]


class TaxonomyLevel(BaseModel):
    level: str
    name: str


class PhysicalFeature(BaseModel):
    name: str
    value: str


class HabitatType(BaseModel):
    name: str
    icon: str


class LifecycleStage(BaseModel):
    name: str
    icon: str
    description: str
    season: Optional[str] = None
    clutchSize: Optional[str] = None
    lifespan: Optional[str] = None


class Sound(BaseModel):
    title: str
    description: str
    context: str
    audioSrc: str
    duration: str


class RelatedBird(BaseModel):
    name: str
    scientificName: str
    image: str
    alt: str
    profileUrl: str


class Metadata(BaseModel):
    lastUpdated: str
    contributors: List[str]
    sources: List[str]
    tags: List[str]


# Main schemas
class BirdBase(BaseModel):
    bird_id: str
    name: str
    scientific_name: str


class BirdCreate(BirdBase):
    conservation_status: Dict[str, Any]
    quick_facts: List[Dict[str, Any]]
    tags: List[Dict[str, Any]]
    images: Dict[str, Any]
    overview: Dict[str, Any]
    habitat_and_distribution: Dict[str, Any]
    diet_and_behavior: Dict[str, Any]
    sounds: Dict[str, Any]
    related_birds: List[Dict[str, Any]]
    meta_data: Dict[str, Any]


class BirdUpdate(BaseModel):
    name: Optional[str] = None
    scientific_name: Optional[str] = None
    conservation_status: Optional[Dict[str, Any]] = None
    quick_facts: Optional[List[Dict[str, Any]]] = None
    tags: Optional[List[Dict[str, Any]]] = None
    images: Optional[Dict[str, Any]] = None
    overview: Optional[Dict[str, Any]] = None
    habitat_and_distribution: Optional[Dict[str, Any]] = None
    diet_and_behavior: Optional[Dict[str, Any]] = None
    sounds: Optional[Dict[str, Any]] = None
    related_birds: Optional[List[Dict[str, Any]]] = None
    meta_data: Optional[Dict[str, Any]] = None


class BirdInDBBase(BirdBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Bird(BirdInDBBase):
    conservation_status: Dict[str, Any]
    quick_facts: List[Dict[str, Any]]
    tags: List[Dict[str, Any]]
    images: Dict[str, Any]
    overview: Dict[str, Any]
    habitat_and_distribution: Dict[str, Any]
    diet_and_behavior: Dict[str, Any]
    sounds: Dict[str, Any]
    related_birds: List[Dict[str, Any]]
    meta_data: Dict[str, Any]


class BirdInDB(BirdInDBBase):
    pass


# API Response schema
class BirdResponse(BaseModel):
    success: bool
    data: Bird
