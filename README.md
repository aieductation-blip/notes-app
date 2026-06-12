# notes-app

## Description
notes-app is a FastAPI-based web API for managing notes. It leverages Redis for fast in-memory storage and uses JWT for secure authentication. Designed with a layered architecture, the project ensures clear separation of concerns between routes, services, and models. It emphasizes test-driven development with pytest, utilizes environment variables for configuration, and includes handy make commands for development workflows.

## Tech Stack
- Python 3.x
- FastAPI
- Redis
- JWT (PyJWT)
- pytest

## Folder Structure
notes-app/
│
├── app/
│   ├── api/                  # API route definitions
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   └── notes.py
│   │   └── __init__.py
│   ├── core/                 # Configuration and constants
│   │   ├── config.py
│   │   └── security.py
│   ├── models/               # Data models (Pydantic)
│   │   ├── note.py
│   │   └── user.py
│   ├── services/             # Business logic
│   │   ├── auth_service.py
│   │   └── notes_service.py
│   ├── main.py               # Application entry point
│   └── dependencies.py       # Dependency overrides and common dependencies
│
├── tests/                    # Test suite
│   ├── test_auth.py
│   ├── test_notes.py
│   └── conftest.py
│
├── .env                      # Environment variables (example)
├── Makefile                  # Development commands
├── README.md                 # Project documentation
└── requirements.txt          # Python dependencies

## How to Run Locally
1. Clone the repository:
   git clone https://github.com/yourusername/notes-app.git
2. Create and activate a virtual environment:
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
3. Install dependencies:
   pip install -r requirements.txt
4. Set environment variables (see below)
5. Launch Redis server locally (if not already running):
   docker run -d -p 6379:6379 redis
6. Run the application:
   make run
7. Access the API at http://127.0.0.1:8000

## Environment Variables
Create a `.env` file at the root with the following variables:
- `SECRET_KEY`: Your secret JWT key
- `REDIS_URL`: Redis connection URL (default: redis://localhost:6379)
- `API_PREFIX`: URL prefix for API routes (default: /api)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration in minutes (default: 30)

Example `.env`:
SECRET_KEY=your_secret_key
REDIS_URL=redis://localhost:6379
API_PREFIX=/api
ACCESS_TOKEN_EXPIRE_MINUTES=30

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch:
   git checkout -b feature/your-feature-name
3. Implement your feature or fix.
4. Write tests for your changes.
5. Run tests to ensure stability:
   pytest
6. Push your branch:
   git push origin feature/your-feature-name
7. Submit a pull request describing your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.