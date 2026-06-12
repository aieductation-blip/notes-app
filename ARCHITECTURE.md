# ARCHITECTURE.md

# Notes App Architecture

## Overview
Notes App is a RESTful web API developed with **FastAPI** (Python 3.11), employing **Redis** as the primary data store for notes, and **JWT** tokens for user authentication. The project adopts a layered architecture separating routing, business logic, and data access layers, ensuring maintainability and testability.

---

## Tech Stack and Rationale

| Component   | Technology | Reasons for Choice                                                |
|-------------|--------------|------------------------------------------------------------------|
| Web Framework | FastAPI | Chosen over Flask for native async support, faster performance, and automatic OpenAPI docs generation. |
| Data Storage | Redis | Selected for its in-memory speed, simplicity, and suitability for small-sized note data. Used via `redis-py` client. |
| Authentication | JWT | Lightweight, stateless token implementation with `pyjwt`, avoiding server-side session management. |
| Testing | pytest | Popular, flexible testing framework with easy test discovery and assertion introspection. |
| Environment Config | python-dotenv | Allows environment variable management, securing secrets like JWT SECRET_KEY. |

---

## System Components and Their Responsibilities

### 1. Routes Layer (`routes/`)
- Exposes HTTP endpoints.
- Handles request validation and response formatting.
- Example endpoints:
  - POST `/api/auth/register`: Register new user (if extended for user management).
  - POST `/api/auth/login`: Returns JWT token.
  - GET `/api/notes/`: List all notes for authenticated user.
  - POST `/api/notes/`: Create a new note.
  - GET `/api/notes/{note_id}`: Retrieve a specific note.
  - PUT `/api/notes/{note_id}`: Update a note.
  - DELETE `/api/notes/{note_id}`: Delete a note.
- Uses `FastAPI` routers, with route decorators for each endpoint.

### 2. Service Layer (`services/`)
- Contains core business logic separate from HTTP concerns.
- Handles:
  - User authentication & token issuance.
  - Note CRUD operations interacting with Redis.
  - Dependency injection for Redis client and JWT secret.
- Why separate? Ensures easier testing and code reuse.

### 3. Data Models (`models/`)
- Pydantic models for request validation, e.g., `NoteCreate`, `NoteUpdate`, `TokenResponse`.
- Redis data is stored as key-value pairs, e.g., user notes keyed by pattern: `notes:{user_id}:{note_id}`.

## Layered Architecture Diagram

[Client] <---> [Routes (`routes/`)] <---> [Services (`services/`)] <---> [Data Access (Redis)]
                ^                         |                        |
                |                         |                        |
           JWT Auth Middleware       Business Logic            Redis Client (`redis-py`)

---

## Data Flow and API Endpoints

| Method | Endpoint                                              | Description                            | Request Body                          | Response                                              |
|--------|--------------------------------------------------------|----------------------------------------|---------------------------------------|--------------------------------------------------------|
| POST   | `/api/auth/login`                                      | User logs in with credentials          | `{ "username": "user", "password": "pass" }` | `{ "access_token": "JWT_TOKEN", "token_type": "bearer" }` |
| GET    | `/api/notes/`                                          | List user's notes                     | Authorization: Bearer JWT            | `[{"note_id": "uuid", "content": "Note text", "created_at": "..."}]` |
| POST   | `/api/notes/`                                          | Create a new note                     | `{ "content": "My new note" }`       | `{ "note_id": "uuid", "content": "My new note", "created_at": "..." }` |
| GET    | `/api/notes/{note_id}`                                   | Get specific note                     | Authorization: Bearer JWT, path param | `{ "note_id": "uuid", "content": "...", "created_at": "..." }` |
| PUT    | `/api/notes/{note_id}`                                   | Update a note                         | `{ "content": "Updated note" }`       | `{ "note_id": "uuid", "content": "Updated note", "updated_at": "..." }` |
| DELETE | `/api/notes/{note_id}`                                   | Delete a note                         | Authorization: Bearer JWT, path param | `204 No Content` |

---

## Database/Table Structure
Since Redis is used directly:

- Notes stored with keys: `notes:{user_id}:{note_id}`
- Note data stored as JSON string: `{"content": "Note text", "created_at": "...", "updated_at": "..."}`

Example:
- Key: `notes:123e4567-e89b-12d3-a456-426614174000:001`
- Value: `{"content": "First note", "created_at": "2023-10-10T10:00:00Z", "updated_at": "2023-10-10T10:00:00Z"}`

---

## Environment Variables
- `REDIS_URL`: Redis server connection string (e.g., `redis://localhost:6379`)
- `JWT_SECRET_KEY`: Secret key used for signing JWT tokens.
- `JWT_ALGORITHM`: Algorithm, e.g., `HS256`.

All secrets are loaded via `python-dotenv` in a dedicated config module.

---

## Dev Commands (`Makefile`)
- `make run`: Start FastAPI server (`uvicorn main:app --reload`)
- `make test`: Run pytest tests.
- `make lint`: Run static analysis (`flake8 .`)
- `make format`: Format code with `black`.

---

## Testing Strategy
- Tests located in `tests/`
- Use pytest fixtures for Redis mocking.
- Separate tests for:
  - Authentication flow.
  - Note CRUD operations.
  - Middleware with invalid tokens.
- Example test:
  - `test_create_note`: Mocks valid JWT, calls POST `/api/notes/`, asserts Redis key exists.

---

## Documentation
- Auto-generated OpenAPI docs at `/docs`.
- Endpoints described with request/response models.
- Inline docstrings in route functions.

## README
Provides project setup instructions, environment variable configuration, and usage commands.

---