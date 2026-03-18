# Core Module

## Yeh module kyu bana hai?

Core module backend ki foundation hai — saari shared infrastructure yahan hai jo baaki saare modules use karte hain. Koi bhi endpoint, model ya service directly ya indirectly core pe depend karti hai.

## Files

### `config.py` — Configuration Loader

- `settings.toml` se logging config load karta hai (TOML format, `tomllib`)
- Environment variables se baaki config load hoti hai via Pydantic `BaseSettings`
- `Settings` class me saare env vars defined hain: `DATABASE_URL`, `JWT_SECRET_KEY`, `ENVIRONMENT`, etc.
- `LogSettings` class `settings.toml` ke `[logging]` section se values read karti hai
- `settings.is_production` property se check hota hai ki production mode hai ya nahi
- Nayi env var chahiye? `Settings` class me field add karo, `.env.dev` aur `.env.prod.example` me bhi daalo

### `database.py` — Async SQLAlchemy Setup

- `create_async_engine` se PostgreSQL connection banta hai (`asyncpg` driver)
- `async_sessionmaker` se session factory banti hai
- `Base` class — saare ORM models isse inherit karte hain
- `get_db()` — FastAPI dependency jo endpoint ko DB session deta hai, auto-commit on success, auto-rollback on error

### `security.py` — JWT + Password Hashing

- `hash_password(plain)` — bcrypt se password hash karta hai
- `verify_password(plain, hashed)` — password match check karta hai
- `create_access_token(data, expires_delta)` — JWT token generate karta hai, `sub` field me user ID daalo
- `decode_access_token(token)` — JWT verify + decode karta hai, invalid token pe `None` return karta hai
- Algorithm aur secret `Settings` se aate hain (`JWT_ALGORITHM`, `JWT_SECRET_KEY`)

### `logger.py` — Daily Rotating Logger

- `get_logger(name)` — configured logger return karta hai with file + console handlers
- Log files daily rotate hote hain: `logs/backend_2026-03-18.log` format
- Same day me agar file `max_bytes` (settings.toml) se badi ho jaye toh size-based rotation bhi hoti hai
- `backup_count` purani rotated files rakhta hai
- **Important**: Har jagah `get_logger("module_name")` use karo, `print()` ya `logging.getLogger()` directly mat use karo

## Kab modify karna hai?

- Nayi shared utility chahiye (e.g. email sender, cache) → naya file banao `core/` me
- Nayi env variable → `config.py` me `Settings` class me add karo
- Logging config change → `settings.toml` edit karo, code change ki zarurat nahi
- Naya auth method (e.g. API keys) → `security.py` me add karo
