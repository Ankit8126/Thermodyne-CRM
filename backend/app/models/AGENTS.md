# Models Module

## Yeh module kyu bana hai?

Yeh module SQLAlchemy ORM models rakhta hai — har model ek database table represent karta hai. Backend ka data layer yahan define hota hai.

## Files

### `user.py` — User Model

- Table name: `users`
- Fields: `id` (UUID string), `email` (unique, indexed), `hashed_password`, `full_name`, `is_active`, `created_at`, `updated_at`
- `Base` se inherit karta hai (`from app.core.database import Base`)
- `mapped_column` with type annotations use karta hai (SQLAlchemy 2.0 style)

## Naya model kaise banaye?

1. `models/` me naya file banao, e.g. `lead.py`
2. `Base` import karo: `from app.core.database import Base`
3. Class define karo:

```python
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    # ... baaki fields
```

4. `alembic/env.py` me model import karo taaki Alembic ko pata chale:
   `from app.models.lead import Lead  # noqa: F401`
5. Migration generate karo: `uv run alembic revision --autogenerate -m "add leads table"`
6. Migration apply karo: `uv run alembic upgrade head`

## Rules

- Hamesha `mapped_column` with type hints use karo (SQLAlchemy 2.0 declarative style)
- Primary key UUID string rakho (`uuid.uuid4()`)
- `created_at` aur `updated_at` timestamps har model me daalo
- Relationships ke liye `relationship()` use karo with `back_populates`
- Table name plural hona chahiye (e.g. `users`, `leads`, `contacts`)
- Sensitive data (passwords) kabhi plain text store mat karo
