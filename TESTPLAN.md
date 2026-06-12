# TESTPLAN.md

## 1. Test Strategy
Our testing strategy focuses on layered testing aligned with the application's architecture: unit tests for individual functions and models, integration tests for endpoints and services, and end-to-end (E2E) tests simulating real user flows. We will leverage pytest for all testing levels, utilizing fastapi's TestClient for API testing, mocking Redis connections for isolation, and verifying JWT authentication flows comprehensively. Tests will run in isolated environments with environment variables for configuration, ensuring no leakage of secrets. Coverage will be maintained at >80%, with continuous integration pipelines executing tests on pull requests.

## 2. Test Levels

### Unit Tests
- **Models**:
  - `User` model: test creation, validation errors.
  - `Note` model: test data serialization and validation.
- **Utility Functions**:
  - JWT token encode/decode functions (`create_jwt_token`, `decode_jwt_token`).
  - Redis utility methods for key-value operations (`save_note`, `fetch_note`).

**Example**:
- Test `create_jwt_token()` generates a valid JWT with correct claims.
- Test `save_note()` correctly saves and retrieves data from Redis mock.

### Integration Tests
- **API Endpoints**:
  - `POST /auth/login` with valid/invalid credentials.
  - `GET /notes/` retrieves all notes for the authenticated user.
  - `POST /notes/` creates a new note.
  - `GET /notes/{note_id}` fetches specific note.
  - `DELETE /notes/{note_id}` deletes a note.
- **Redis Operations**:
  - Verify note data stored with `save_note()` is retrievable via API.
- **JWT Authentication**:
  - Ensure token validation middleware correctly grants/denies access.

### E2E Tests
- User registration and login flow.
- Creating, fetching, and deleting notes end-to-end.
- Handling invalid JWT tokens during calls.
- Multiple users accessing their own notes.
- Error scenarios (e.g., expired token, redis downtime).

## 3. Test Cases Table

| ID   | Test Case                                                 | Type          | Priority | Expected Result                                              |
|-------|-----------------------------------------------------------|--------------|----------|--------------------------------------------------------------|
| TC001 | POST /auth/login with valid credentials                     | API          | High     | 200 OK with JWT token in response                            |
| TC002 | POST /auth/login with invalid credentials                   | API          | High     | 401 Unauthorized                                              |
| TC003 | GET /notes/ (with valid JWT)                                | API          | High     | 200 OK with list of notes                                    |
| TC004 | POST /notes/ with valid note data                           | API          | High     | 201 Created with note data in response                        |
| TC005 | GET /notes/{note_id} with existing note                     | API          | High     | 200 OK with note details                                       |
| TC006 | GET /notes/{note_id} with non-existing note                 | API          | Medium   | 404 Not Found                                                |
| TC007 | DELETE /notes/{note_id} (existing note)                     | API          | High     | 204 No Content                                                 |
| TC008 | DELETE /notes/{note_id} with non-existing note             | API          | Medium   | 404 Not Found                                                |
| TC009 | JWT token expiration during request                         | API          | High     | 401 Unauthorized due to expired token                        |
| TC010 | Redis server down during note save                          | API/Redis    | High     | 503 Service Unavailable response                              |

## 4. Edge Cases
- Use empty string or overly long strings when creating notes.
- Attempt to access notes with invalid or tampered JWT tokens.
- Concurrent creation/deletion of notes for the same user.
- Redis server restart during ongoing requests.
- Attempt to create notes when Redis connection is disrupted.

## 5. Test Data Requirements
- User fixtures:
  - Valid user: `{"username": "testuser", "password": "TestPassword123"}`
  - Invalid user credentials for auth failure testing.
- Note fixtures:
  - Sample note: `{"title": "Test Note", "content": "This is a test note."}`
- Environment variables:
  - `JWT_SECRET`: secret key for JWT.
  - Redis connection details: `REDIS_URL`.
- Seed data:
  - Pre-created user in test database.
  - Redis mock data for notes linked to test users.

## 6. Tools & Setup

### Tools
- pytest: `pip install pytest`
- fastapi TestClient: `from fastapi.testclient import TestClient`
- pytest-mock for mocking Redis: `pip install pytest-mock`
- redis-py for Redis interactions: `pip install redis`
- JWT for token handling: `pyjwt`

### Setup Commands
# Install dependencies
pip install pytest fastapi pytest-mock redis pyjwt

# Run tests locally
pytest --capture=log -v

# Run specific test module
pytest tests/test_api.py

# Setup environment variables
export JWT_SECRET='your-secret-key'
export REDIS_URL='redis://localhost:6379'