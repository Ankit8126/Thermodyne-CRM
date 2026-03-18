# Health Module

## Yeh module kyu bana hai?

Health module system ki status check karta hai — API live hai ya nahi, DB connected hai ya nahi. Docker healthcheck aur monitoring tools isko call karte hain.

## Structure

```
api/v1/health/
├── __init__.py
├── router.py      # health check endpoint
└── AGENTS.md      # yeh file
```

## Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/v1/health` | No | API + DB status return karta hai |

## Response Format

```json
{
  "status": "healthy",
  "database": "up"
}
```

Agar DB down ho:
```json
{
  "status": "degraded",
  "database": "down"
}
```

## Notes

- Yeh endpoint public hai (no auth required) — Docker healthcheck aur load balancers isko use karte hain
- Background health check bhi separately har 2 min me chalta hai (`app/main.py` me) — woh logs me likhta hai
- Agar naya dependency add ho (e.g. Redis, S3) toh yahan uska check bhi add karo
