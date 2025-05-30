# BirdNest API

A comprehensive FastAPI application for managing bird information with detailed species data, conservation status, behavior, and more.

## Features

- **Complete CRUD operations** for bird species
- **Detailed bird profiles** including conservation status, physical characteristics, habitat, diet, and behavior
- **Search functionality** by name, scientific name, and conservation status
- **Professional API structure** with proper error handling
- **Comprehensive test coverage** for API endpoints and CRUD operations
- **SQLAlchemy ORM** with SQLite database
- **Pydantic schemas** for data validation
- **Automatic API documentation** with Swagger UI

## Project Structure

```
birdnest_api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── config.py          # Application configuration
│   │   └── database.py        # Database setup and connection
│   ├── models/
│   │   ├── base.py           # Base model with common fields
│   │   └── bird.py           # Bird SQLAlchemy model
│   ├── schemas/
│   │   └── bird.py           # Pydantic schemas for validation
│   ├── api/
│   │   ├── deps.py           # Dependencies
│   │   └── v1/
│   │       ├── api.py        # API router
│   │       └── endpoints/
│   │           └── birds.py   # Bird endpoints
│   └── crud/
│       ├── base.py           # Base CRUD operations
│       └── bird.py           # Bird-specific CRUD operations
├── tests/
│   ├── conftest.py           # Test configuration
│   ├── test_api/
│   │   └── test_birds.py     # API endpoint tests
│   └── test_crud/
│       └── test_bird.py      # CRUD operation tests
├── requirements.txt
├── .env.example
├── README.md
└── run.py                    # Application runner
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/wallace-21/BirdNest-backend
   cd BirdNest-backend
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Create the virtual enviroment
   #  inside the BirdNest repo
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   nvim .env
   # Edit .env file as needed
   ```

## Running the Application

### Development Server

```bash
python run.py
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Birds

- `POST /api/v1/birds/` - Create a new bird
- `GET /api/v1/birds/` - Get all birds (with pagination)
- `GET /api/v1/birds/{bird_id}` - Get a specific bird by ID
- `PUT /api/v1/birds/{bird_id}` - Update a bird
- `DELETE /api/v1/birds/{bird_id}` - Delete a bird

### Search & Filter

- `GET /api/v1/birds/search/name?name={query}` - Search birds by name
- `GET /api/v1/birds/search/scientific?scientific_name={query}` - Search by scientific name
- `GET /api/v1/birds/filter/conservation?status={status}` - Filter by conservation status

## Example Usage

### Creating a Bird

```bash
curl -X POST "http://localhost:8000/api/v1/birds/" \
     -H "Content-Type: application/json" \
     -d '{
       "bird_id": "peregrine-falcon",
       "name": "Peregrine Falcon",
       "scientific_name": "Falco peregrinus",
       "conservation_status": {
         "status": "least-concern",
         "label": "Least Concern",
         "description": "Successfully recovered from near extinction",
         "currentThreats": ["Habitat loss", "Illegal hunting"]
       },
       "quick_facts": [
         {
           "label": "Wingspan",
           "value": "89-120 cm",
           "icon": "ruler-horizontal"
         }
       ],
       "tags": [
         {
           "text": "Migratory",
           "icon": "plane"
         }
       ],
       "images": {
         "main": [],
         "gallery": []
       },
       "overview": {},
       "habitat_and_distribution": {},
       "diet_and_behavior": {},
       "sounds": {},
       "related_birds": [],
       "metadata": {
         "lastUpdated": "2025-01-01T00:00:00Z",
         "contributors": ["Dr. Jane Smith"],
         "sources": ["Cornell Lab"],
         "tags": ["raptor", "falcon"]
       }
     }'
```

### Getting a Bird

```bash
curl "http://localhost:8000/api/v1/birds/peregrine-falcon"
```

### Searching Birds

```bash
curl "http://localhost:8000/api/v1/birds/search/name?name=falcon"
```

## Testing

Run the test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=app
```

Run specific test files:

```bash
pytest tests/test_api/test_birds.py
pytest tests/test_crud/test_bird.py
```

## Database

The application uses SQLite by default. The database file (`birdnest.db`) will be created automatically when you first run the application.

### Database Schema

The Bird model includes:
- Basic information (ID, name, scientific name)
- Conservation status and threats
- Physical characteristics and taxonomy
- Habitat and distribution data
- Diet and behavior information
- Sounds and vocalizations
- Related species
- Metadata and sources

## Configuration

Environment variables can be set in the `.env` file:

- `DATABASE_URL`: Database connection string
- `API_V1_STR`: API version prefix (default: `/api/v1`)
- `PROJECT_NAME`: Project name for documentation
- `DEBUG`: Enable debug mode

## Development

### Adding New Fields

1. Update the `Bird` model in `app/models/bird.py`
2. Update the Pydantic schemas in `app/schemas/bird.py`
3. Create and run database migrations if needed
4. Update tests accordingly

### Adding New Endpoints

1. Add the endpoint function in `app/api/v1/endpoints/birds.py`
2. Add corresponding CRUD operations in `app/crud/bird.py`
3. Write tests in `tests/test_api/test_birds.py`

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in your environment
2. Configure proper CORS origins in `app/main.py`
3. Use a production WSGI server like Gunicorn
4. Consider using PostgreSQL/Django/MySQL instead of SQLite
5. Set up proper logging and monitoring

