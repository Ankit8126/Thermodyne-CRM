# API v1

## Yeh module kyu bana hai?

Yeh module saare HTTP endpoints handle karta hai. API versioning (`v1`) isliye hai taaki future me `v2` bana sake bina purane clients todhe. Saare endpoints `/api/v1/` prefix ke under aate hain.

## Structure

Har feature ek alag module directory hai — apna router, dependencies, aur AGENTS.md:

```
api/v1/
├── router.py              # saare modules ko aggregate karta hai
├── AGENTS.md              # yeh file
├── user/                  # user module
│   ├── router.py          # register, login, logout, me
│   ├── dependencies.py    # get_current_user (shared dependency)
│   └── AGENTS.md
└── health/                # health module
    ├── router.py          # system health check
    └── AGENTS.md
```

## `router.py` — Main Route Aggregator

Saare module routers yahan register hote hain:

```python
api_router.include_router(health_router, tags=["health"])
api_router.include_router(user_router, prefix="/user", tags=["user"])
```

## Registered Modules

| Module | Prefix | AGENTS.md | Description |
|--------|--------|-----------|-------------|
| user | `/api/v1/user` | `user/AGENTS.md` | Registration, login, logout, profile |
| health | `/api/v1/health` | `health/AGENTS.md` | System + DB health check |

## Naya module kaise banaye?

1. `api/v1/` me naya folder banao, e.g. `leads/`
2. Folder me yeh files banao:
   - `__init__.py` (empty)
   - `router.py` — `APIRouter()` with endpoints
   - `dependencies.py` — module-specific dependencies (optional)
   - `AGENTS.md` — module ka description, endpoints, related files
3. `router.py` (main aggregator) me register karo:
   ```python
   from app.api.v1.leads.router import router as leads_router
   api_router.include_router(leads_router, prefix="/leads", tags=["leads"])
   ```
4. Agar protected endpoint chahiye toh user module se dependency import karo:
   ```python
   from app.api.v1.user.dependencies import get_current_user
   ```

## Rules

- Har module ka apna folder hona chahiye — flat files `api/v1/` me mat daalo
- Har module me `AGENTS.md` zaroor likho
- Business logic agar complex ho toh module me `service.py` bana lo
- `print()` mat use karo, `logger` use karo
- Response me raw SQLAlchemy model mat do, Pydantic schema se serialize karo
