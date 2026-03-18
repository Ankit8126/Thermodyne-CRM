# Schemas Module

## Yeh module kyu bana hai?

Yeh module Pydantic schemas rakhta hai jo API request validation aur response serialization ke liye use hote hain. Models (SQLAlchemy) se alag hain — schemas define karte hain ki API pe kya data aayega aur kya jaayega.

## Files

### `user.py` — User Schemas

- `UserCreate` — registration request body (email, password, full_name)
- `UserResponse` — API response me user data (id, email, full_name, is_active, created_at). Password kabhi response me nahi jaata.
- `Token` — login response (access_token, token_type)
- `TokenData` — decoded JWT token ka internal schema

## Naya schema kaise banaye?

1. `schemas/` me naya file banao, e.g. `lead.py`
2. Pydantic `BaseModel` se inherit karo
3. Har endpoint ke liye alag schemas banao:

```python
from pydantic import BaseModel

class LeadCreate(BaseModel):
    name: str
    email: str
    phone: str | None = None

class LeadUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None

class LeadResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
```

## Rules

- Response schemas me `model_config = {"from_attributes": True}` zaroor daalo (SQLAlchemy model se convert hone ke liye)
- Password, hashed_password, internal IDs jaise sensitive fields response schema me mat daalo
- `Create` schema me required fields rakho, `Update` schema me sab optional (`None` default)
- Email fields ke liye `EmailStr` use karo (`from pydantic import EmailStr`) — auto-validation hoti hai
- Naming convention: `{Model}Create`, `{Model}Update`, `{Model}Response`
