#!/usr/bin/env python3
"""
Script to populate the database with sample bird data.
Run this script to add the Peregrine Falcon data from your JSON example.
"""

import json
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.base import BaseModel
from app import crud, schemas

# Create tables
BaseModel.metadata.create_all(bind=engine)

# Sample data based on your JSON structure
PEREGRINE_FALCON_DATA = {
    "bird_id": "peregrine-falcon",
    "name": "Peregrine Falcon",
    "scientific_name": "Falco peregrinus",
    "conservation_status": {
      "status": "least-concern",
      "label": "Least Concern",
      "description": "The Peregrine Falcon has made a remarkable recovery from near extinction in many regions. After populations crashed due to DDT poisoning in the mid-20th century, conservation efforts and the banning of DDT have allowed numbers to rebound significantly.",
      "currentThreats": [
        "Habitat loss",
        "Illegal hunting",
        "Collisions with human-made structures"
      ]
    },
    "quick_facts": [
      {
        "label": "Family",
        "value": "Falconidae",
        "icon": "feather"
      },
      {
        "label": "Order",
        "value": "Falconiformes",
        "icon": "sitemap"
      },
      {
        "label": "Wingspan",
        "value": "89-120 cm",
        "icon": "ruler-horizontal"
      },
      {
        "label": "Weight",
        "value": "0.45-1.5 kg",
        "icon": "weight-hanging"
      }
    ],
    "tags": [
      {
        "text": "Migratory",
        "icon": "plane"
      },
      {
        "text": "Not Extinct",
        "icon": "skull",
        "class": "extinct-tag"
      }
    ],
    "images": {
      "main": [
        {
          "url": "https://placehold.co/600x400",
          "alt": "Peregrine Falcon",
          "caption": "Adult Peregrine Falcon perched on a cliff"
        },
        {
          "url": "https://placehold.co/600x400",
          "alt": "Peregrine Falcon in flight",
          "caption": "Peregrine Falcon soaring through the sky"
        }
      ],
      "gallery": [
        {
          "url": "https://placehold.co/600x400",
          "alt": "Peregrine Falcon in flight",
          "caption": "Peregrine Falcon in flight"
        },
        {
          "url": "https://placehold.co/600x400",
          "alt": "Peregrine Falcon portrait",
          "caption": "Close-up portrait showing distinctive facial markings"
        }
      ]
    },
    "overview": {
      "about": {
        "title": "About the Peregrine Falcon",
        "paragraphs": [
          "The Peregrine Falcon is renowned for its speed, reaching over 320 km/h (200 mph) during its characteristic hunting dive (stoop), making it the fastest bird in the world and the fastest member of the animal kingdom.",
          "A successful conservation effort has helped restore populations after they were decimated by pesticides, particularly DDT, in the mid-20th century. In many regions, their numbers have rebounded significantly."
        ]
      },
      "physicalCharacteristics": {
        "title": "Physical Characteristics",
        "features": [
          {
            "name": "Appearance",
            "value": "Blue-gray back, barred white underparts, and a black head with distinctive \"mustache\" markings"
          },
          {
            "name": "Size",
            "value": "Medium-sized falcon, 34-58 cm in length"
          },
          {
            "name": "Wingspan",
            "value": "89-120 cm"
          },
          {
            "name": "Weight",
            "value": "0.45-1.5 kg, with females typically larger than males"
          },
          {
            "name": "Lifespan",
            "value": "Up to 15-20 years in the wild"
          }
        ]
      },
      "taxonomy": {
        "title": "Taxonomy",
        "levels": [
          {
            "level": "Kingdom",
            "name": "Animalia"
          },
          {
            "level": "Phylum",
            "name": "Chordata"
          },
          {
            "level": "Class",
            "name": "Aves"
          },
          {
            "level": "Order",
            "name": "Falconiformes"
          },
          {
            "level": "Family",
            "name": "Falconidae"
          },
          {
            "level": "Genus",
            "name": "Falco"
          },
          {
            "level": "Species",
            "name": "F. peregrinus"
          }
        ]
      }
    },
    "habitat_and_distribution": {
      "habitat": {
        "title": "Habitat",
        "description": "Peregrine Falcons are highly adaptable and can be found in a wide variety of habitats, including:",
        "types": [
          {
            "name": "Mountain ranges and cliffs",
            "icon": "mountain"
          },
          {
            "name": "Forests and woodlands",
            "icon": "tree"
          },
          {
            "name": "Coastal areas and sea cliffs",
            "icon": "water"
          },
          {
            "name": "Urban environments (nesting on tall buildings and bridges)",
            "icon": "city"
          },
          {
            "name": "River valleys and gorges",
            "icon": "dungeon"
          }
        ]
      },
      "distribution": {
        "title": "Geographic Distribution",
        "description": "The Peregrine Falcon has one of the most widespread distributions of any bird of prey. It can be found on every continent except Antarctica.",
        "regions": [
          "North America",
          "South America",
          "Europe",
          "Africa",
          "Asia",
          "Australia"
        ]
      },
      "migration": {
        "title": "Migration Patterns",
        "status": "Migratory",
        "description": [
          "Migration patterns vary by population:",
          "Northern populations tend to be highly migratory",
          "Populations in temperate regions may be partially migratory",
          "Tropical and subtropical populations are typically non-migratory"
        ]
      }
    },
    "diet_and_behavior": {
      "diet": {
        "title": "Diet",
        "description": "Peregrine Falcons are carnivorous birds of prey with a diet consisting primarily of:",
        "items": [
          {
            "name": "Medium-sized birds",
            "image": "https://placehold.co/100x100",
            "alt": "Bird"
          },
          {
            "name": "Pigeons and doves",
            "image": "https://placehold.co/100x100",
            "alt": "Pigeon"
          },
          {
            "name": "Waterfowl",
            "image": "https://placehold.co/100x100",
            "alt": "Waterfowl"
          },
          {
            "name": "Songbirds",
            "image": "https://placehold.co/100x100",
            "alt": "Songbird"
          }
        ]
      },
      "hunting": {
        "title": "Hunting Technique",
        "subtitle": "The Hunting Stoop",
        "steps": [
          {
            "number": 1,
            "description": "Soars to high altitude (300-3000 meters)"
          },
          {
            "number": 2,
            "description": "Spots prey below using exceptional vision"
          },
          {
            "number": 3,
            "description": "Dives in a controlled stoop at speeds of 320+ km/h"
          },
          {
            "number": 4,
            "description": "Strikes prey mid-air with a clenched foot"
          },
          {
            "number": 5,
            "description": "Either catches the stunned prey or retrieves it from the ground"
          }
        ]
      }
    },
    "sounds": {
      "title": "Peregrine Falcon Sounds",
      "introduction": "Peregrine Falcons have several distinct vocalizations used for different purposes, from territorial calls to mating displays.",
      "calls": [
        {
          "title": "Territorial Call",
          "description": "A series of harsh, rapid \"kak-kak-kak\" calls used to defend territory and during nest defense.",
          "context": "Most commonly heard during breeding season when defending nest sites.",
          "audioSrc": "https://example.com/peregrine-territorial.mp3",
          "duration": "0:30"
        },
        {
          "title": "Alarm Call",
          "description": "A sharp, piercing \"eechip\" call used to alert others to potential danger or intruders.",
          "context": "Often heard when humans or predators approach too close to a nest site.",
          "audioSrc": "https://example.com/peregrine-alarm.mp3",
          "duration": "0:22"
        },
        {
          "title": "Mating Call",
          "description": "A softer, more melodic series of calls exchanged between mates during courtship.",
          "context": "Heard primarily during the early breeding season as pairs form or reunite.",
          "audioSrc": "https://example.com/peregrine-mating.mp3",
          "duration": "0:45"
        },
        {
          "title": "Feeding Chicks",
          "description": "Chicks make high-pitched begging calls when parents return with food.",
          "context": "Commonly heard at nest sites during the chick-rearing period.",
          "audioSrc": "https://example.com/peregrine-chicks.mp3",
          "duration": "0:38"
        }
      ],
      "facts": [
        "Peregrine Falcons are generally silent outside of the breeding season",
        "Males and females have slightly different vocalizations, with females typically having deeper calls",
        "Young peregrines develop their adult calls gradually during their first year"
      ]
    },
    "related_birds": [
      {
        "name": "Gyrfalcon",
        "scientific_name": "Falco rusticolus",
        "image": "https://placehold.co/300x200",
        "alt": "Gyrfalcon",
        "profile_url": "#"
      },
      {
        "name": "Merlin",
        "scientific_name": "Falco columbarius",
        "image": "https://placehold.co/300x200",
        "alt": "Merlin",
        "profile_url": "#"
      },
      {
        "name": "American Kestrel",
        "scientific_name": "Falco sparverius",
        "image": "https://placehold.co/300x200",
        "alt": "Kestrel",
        "profile_url": "#"
      },
      {
        "name": "Prairie Falcon",
        "scientific_name": "Falco mexicanus",
        "image": "https://placehold.co/300x200",
        "alt": "Prairie Falcon",
        "profile_url": "#"
      }
    ],
    "meta_data": {
      "last_updated": "2025-04-01T08:30:00Z",
      "contributors": [
        "Dr. Jane Smith, Ornithologist",
        "Mark Johnson, Wildlife Photographer",
        "Peregrine Conservation Society"
      ],
      "sources": [
        "Global Raptor Information Network",
        "Cornell Lab of Ornithology",
        "International Union for Conservation of Nature (IUCN)"
      ],
      "tags": [
        "raptor",
        "falcon",
        "bird of prey",
        "predator",
        "fast bird",
        "conservation success"
      ]
    }
  }
