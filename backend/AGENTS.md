# Thermodyne CRM — Backend Agent Instructions

## What is this project?

Thermodyne CRM ka backend API hai jo FastAPI (Python 3.13) pe bana hai. Yeh Thermodyne Engineering System ke liye ek Customer Relationship Management system ka server-side handle karta hai.

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.13
- **ORM**: SQLAlchemy (async mode with asyncpg driver)
- **Migrations**: Alembic
- **Auth**: JWT tokens (python-jose) + bcrypt password hashing (passlib)
- **Config**: Pydantic Settings (env vars) + settings.toml (logging)
- **Package Manager**: uv (pip nahi, `uv sync` / `uv run` use karo)
- **Database**: PostgreSQL 16
- **Logging**: Daily rotating file logs + console output

## Kya padho pehle

Koi bhi kaam shuru karne se pehle yeh files zaroor padho:

1. **`app/main.py`** — FastAPI app entry point, lifespan events, middleware, background health check
2. **`app/core/config.py`** — saari env variables aur settings.toml se config yahan load hoti hai
3. **`app/core/database.py`** — SQLAlchemy engine, session factory, `get_db` dependency
4. **`app/api/v1/router.py`** — saare module routers yahan aggregate hote hain
5. **`settings.toml`** — logging configuration (max bytes, rotation, format)
6. **`pyproject.toml`** — project dependencies (uv se manage hoti hain)

## Directory Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app, lifespan, middleware
│   ├── api/                 # API routes (versioned, module-based)
│   │   └── v1/
│   │       ├── router.py    # v1 route aggregator
│   │       ├── user/        # user module (register, login, logout, me)
│   │       │   ├── router.py
│   │       │   ├── dependencies.py
│   │       │   └── AGENTS.md
│   │       └── health/      # health module (system status)
│   │           ├── router.py
│   │           └── AGENTS.md
│   ├── core/                # shared infrastructure
│   │   ├── config.py        # env + toml config loader
│   │   ├── database.py      # async SQLAlchemy setup
│   │   ├── security.py      # JWT + password hashing
│   │   └── logger.py        # daily rotating logger
│   ├── models/              # SQLAlchemy ORM models
│   └── schemas/             # Pydantic request/response schemas
├── alembic/                 # database migrations
├── settings.toml            # logging config
└── pyproject.toml           # dependencies (uv)
```

## Module-wise AGENTS.md

Har module ke andar ek `AGENTS.md` file hai. Jab us module me kaam karo toh uski AGENTS.md zaroor padho:

| Module | Path | Purpose |
|--------|------|---------|
| Core | `app/core/AGENTS.md` | Config, DB, Auth, Logger — shared infra |
| API v1 | `app/api/v1/AGENTS.md` | Module-based routing overview |
| User | `app/api/v1/user/AGENTS.md` | Register, login, logout, profile |
| Health | `app/api/v1/health/AGENTS.md` | System + DB health check |
| Models | `app/models/AGENTS.md` | SQLAlchemy ORM models |
| Schemas | `app/schemas/AGENTS.md` | Pydantic validation schemas |
| Alembic | `alembic/AGENTS.md` | Database migrations |

## Rules for Agent

1. **Naya module banane ka flow**: `api/v1/` me folder banao → `router.py`, `dependencies.py`, `AGENTS.md` banao → schema define karo (`schemas/`) → model banao ya existing use karo (`models/`) → main `api/v1/router.py` me register karo
2. **Module structure**: har feature ka apna folder hota hai `api/v1/` me — flat files mat banao
3. **Logger use karo**: har module me `from app.core.logger import get_logger` use karo, `print()` mat use karo
4. **Config env vars**: nayi env variable chahiye toh `app/core/config.py` me `Settings` class me add karo, `.env.dev` aur `.env.prod.example` dono me daalo
5. **Dependencies**: `pyproject.toml` me add karo, `requirements.txt` nahi hai — `uv add <package>` use karo
6. **Migrations**: model change karne ke baad `uv run alembic revision --autogenerate -m "description"` run karo
7. **Protected endpoints**: `from app.api.v1.user.dependencies import get_current_user` — yeh shared dependency hai
8. **Production me Swagger band hai**: `ENVIRONMENT=production` set hone par `/docs`, `/redoc`, `/openapi.json` disable ho jaate hain
9. **Background health check**: har 2 min me DB ping hota hai, `HEALTH_CHECK_INTERVAL_SECONDS` se control hota hai
10. **AGENTS.md zaroor likho**: har naye module me AGENTS.md file banao jo bataye ki module kyu bana hai, endpoints kya hain, related files kaunse hain
