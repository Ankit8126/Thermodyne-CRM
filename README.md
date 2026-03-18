# Thermodyne CRM

CRM for Thermodyne Engineering System.

## Tech Stack

- **Frontend**: Next.js 15 (App Router), TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.13, SQLAlchemy (async), Alembic
- **Database**: PostgreSQL 16
- **Auth**: JWT (python-jose + passlib)
- **Infrastructure**: Docker, Docker Compose

## Prerequisites

- Docker & Docker Compose
- (Optional) Node.js 22+ and Python 3.13+ for local development without Docker

## Quick Start (Development)

```bash
# Clone the repo
git clone <repo-url>
cd Thermodyne-CRM

# Start all services (frontend + backend + db)
make dev
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs
- PostgreSQL: localhost:5432

## Quick Start (Production)

```bash
# Copy and configure production env
cp .env.prod.example .env.prod

# Start production stack
make prod
```

## Useful Commands

| Command | Description |
|---------|-------------|
| `make dev` | Start dev environment (attached) |
| `make dev-d` | Start dev environment (detached) |
| `make prod` | Start production environment |
| `make down` | Stop all containers |
| `make logs` | Tail dev logs |
| `make migrate` | Run Alembic migrations |
| `make makemigrations msg="description"` | Create new migration |
| `make shell-backend` | Shell into backend container |
| `make shell-frontend` | Shell into frontend container |
| `make shell-db` | Open psql in db container |
| `make clean` | Remove all containers, volumes, images |

## Project Structure

```
├── frontend/          # Next.js 15 application
├── backend/           # FastAPI application
├── docker-compose.dev.yml
├── docker-compose.prod.yml
├── .env.dev           # Dev environment variables
├── .env.prod.example  # Prod env template
└── Makefile           # Convenience commands
```



