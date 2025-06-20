# An Advanced, User-Centric Project Management Platform

A cutting-edge Project Management Platform built to streamline collaboration and enhance productivity between Project Managers, Consultants, Admins, and Finance teams. This platform prioritizes an intuitive user experience, robust features, and a scalable architecture for production readiness.

## Tech Stack (Initial - Backend)
- Backend: FastAPI (Python 3.11+)
- Database: PostgreSQL
- ORM: SQLAlchemy, Alembic
- Deployment: Docker, Docker Compose

## How to Run (Initial - Backend with Docker Compose)
1.  **Clone the repository (once available).**
2.  **Navigate to the project root directory (`project-management-app`).**
3.  **Create `backend/.env` file:**
    Create a file named `.env` inside the `project-management-app/backend/` directory.
    Its path relative to `docker-compose.yml` will be `./backend/.env`, but the `env_file` directive in `docker-compose.yml` should be `./project-management-app/backend/.env` if `docker-compose.yml` is in the root above `project-management-app`, OR if `docker-compose.yml` is inside `project-management-app`, then it should be `./backend/.env`.
    Assuming `docker-compose.yml` is in `project-management-app/`:
    Path for env_file: `./backend/.env`

    Content for `project-management-app/backend/.env`:
    ```env
    DATABASE_URL="postgresql://user:password@db:5432/dbname"
    SECRET_KEY="your-super-secret-key-for-jwt-local-env-generate-a-real-one"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    REFRESH_TOKEN_EXPIRE_DAYS=7
    # EMAIL_HOST="smtp.your_email_provider.com"
    # EMAIL_PORT=587
    # EMAIL_USERNAME="your_email@example.com"
    # EMAIL_PASSWORD="your_email_password"
    ```
    *Replace `user`, `password`, and `dbname` if you changed them in `docker-compose.yml`.*
    *Generate a strong `SECRET_KEY` using: `python -c "import os; print(os.urandom(24).hex())\"` and use it for `SECRET_KEY` in both the `.env` file and the `docker-compose.yml` if you choose to set it there directly.*

4.  **Build and start the services (from within `project-management-app` directory):**
    ```bash
    docker-compose up --build -d
    ```
5.  The backend API will be accessible at http://localhost:8000.
    The PostgreSQL database will be accessible on port 5432.

*(Further instructions for Alembic migrations and frontend setup will be added as the project progresses).*
