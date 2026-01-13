# 🐍 Calorie Tracker - Backend (FastAPI)

This is the core engine of the Calorie Tracker application. It is a high-performance REST API built with **FastAPI**, focusing on clean architecture (DDD), scalability, and robust security.

---

## 🏗 Architectural Overview: Domain-Driven Design (DDD)

The project follows a **Domain-Driven Design (DDD)** approach to ensure a clean separation of concerns and high maintainability:

1.  **Routers (API Layer):** Handles HTTP requests and utilizes **Pydantic Schemas** for strict input/output validation.
2.  **Services (Business Logic):** Coordinates data flow, applies business rules, and remains independent of the database implementation.
3.  **Repositories (Data Access):** Abstracts database operations using **SQLAlchemy 2.0 (Async)**.

### **Dependency Injection (DI)**
FastAPI's built-in DI system to maintain loosely coupled components, injecting database sessions, users, service/repository instances, and the Redis context.

---

## 🔒 Security & Authentication

* **JWT Strategy:** Implementation of a dual-token system (**Access + Refresh Tokens**).
* **Redis Store:** * Manages **Refresh Tokens** and user session associations.
    * Implements **Rate Limiting** for Login and Registration to prevent brute-force attacks.
* **Hashing:** Secure password storage using the **Argon2** algorithm.
* **Input/Output Validation:** Every endpoint uses dedicated **Pydantic Schemas** for:
    * **Input Validation:** Ensuring incoming data meets strict types and constraints.
    * **Output Serialization:** Filtering sensitive data and ensuring consistent API responses.

---

## 📂 Project Structure

```text
FastAPI/
├── app/
│   ├── auth/           # Authentication logic, JWT & Refresh Token management
│   ├── core/           # DB/Redis setup, Global Config, Logging & Exceptions
│   ├── fridge/         # Personal product database domain
│   ├── meal/           # Nutrition and daily logging domain
│   ├── measurements/   # Body progress & Weight tracking domain
│   ├── models/         # Centralized SQLAlchemy model imports
│   ├── user/           # User account management
│   ├── utils/          # Global Enums, constants, and helper functions
│   └── main.py         # App entry point & Middlewares
├── tests/              # Pytest suite with async support
├── migrations/         # Alembic database migration scripts
├── .env.example        # Template for environment variables
├── .env.test           # Environment variables for testing
├── alembic.ini         # Migration configuration
├── docker-compose.yml  # Infrastructure orchestration
├── Dockerfile          # Backend containerization
├── pyproject.toml      # Poetry dependencies and project metadata
└── poetry.lock         # Deterministic dependency lock file
```

## 🛠 Tech Stack

* **Framework:** FastAPI (Python 3.10+)
* **Package Manager:** Poetry
* **ORM:** SQLAlchemy 2.0 (Async)
* **Database:** PostgreSQL & Redis
* **Validation:** Pydantic V2 (BaseSettings & Schemas)
* **Migrations:** Alembic
* **Testing:** Pytest & Asyncio

---

## 🧪 Testing Strategy

The project features a robust testing suite focused on reliability:

* **Database Isolation:** Tests run on a dedicated PostgreSQL instance.
* **Transaction Rollback:** To ensure a "clean slate", each test is wrapped in a database transaction that is **automatically rolled back** after completion, preventing data pollution between test cases.
* **Coverage:** Integration tests for API contracts (Routers), Services and repositories and unit tests for helper functions.

## 🛠 Quality Control & CI/CD

To maintain high code standards, this project utilizes:

* **GitHub Actions:** Automatically runs the **Pytest** suite on every Pull Request to the `main` or `develop` branch to prevent regressions.
* **Ruff:** Used for lightning-fast linting and code formatting. It ensures compliance with Python best practices (replaces Flake8, Black, and Isort).

## 📝 Key Features for Developers
* **Centralized Logging:** Uses the standard Python logging module configured for simple consistent monitoring across all domains.

* **Global Exception Handling:** Custom exception handlers map domain-specific errors to standardize HTTP JSON responses.

* **N+1 Optimization:** Efficient data fetching using selectinload and joinedload in SQLAlchemy queries.

* **Environment Management:** Multi-stage configuration (Dev/Test/Prod) via pydantic-settings.

## 🚀 Getting Started
Install Dependencies:

```bash 
poetry install
poetry shell

```

Environment Setup:
```bash 
cp .env.example .env
# Edit .env with your local credentials

```

Run Infrastructure:
```bash 
docker-compose up -d  # Starts Postgres & Redis

```

Migrate & Start:
```bash 
alembic upgrade head
uvicorn app.main:app --reload
```

Run tests:
```bash
# Run the test suite
pytest
```

### **Running Checks Locally**
To check the code quality before pushing, you can run:
```bash
# Run linter
poetry run ruff check .

# Run formatter
poetry run ruff format .
```