# User Module

## Yeh module kyu bana hai?

User module saara user authentication aur user management ka logic handle karta hai — registration, login, logout, current user info. Yeh CRM ka core module hai kyunki har dusra module authenticated user pe depend karta hai.

## Structure

```
api/v1/user/
├── __init__.py
├── router.py          # saare user endpoints
├── dependencies.py    # get_current_user dependency (shared across modules)
└── AGENTS.md          # yeh file
```

## Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/v1/user/register` | No | Naya user create karta hai |
| POST | `/api/v1/user/login` | No | Email + password se JWT token deta hai |
| POST | `/api/v1/user/logout` | Yes | User logout (client-side token discard) |
| GET | `/api/v1/user/me` | Yes | Current logged-in user ki info |

## Files

### `router.py` — Endpoints

- **register**: Email duplicate check → password hash → DB save → return user
- **login**: OAuth2 password form → email lookup → password verify → JWT token return
- **logout**: Protected route, logs out (client token remove karna hota hai)
- **me**: Protected route, current user ka data return karta hai

### `dependencies.py` — Shared Dependencies

- `oauth2_scheme` — OAuth2PasswordBearer configured with this module's login URL
- `get_current_user(token, db)` — JWT token decode → DB se user fetch → return User object
- **Dusre modules me bhi isko import karo** jab protected endpoint banana ho:
  ```python
  from app.api.v1.user.dependencies import get_current_user
  ```

## Related Files

- Model: `app/models/user.py` — User table (id, email, hashed_password, full_name, is_active, timestamps)
- Schemas: `app/schemas/user.py` — UserCreate, UserResponse, Token, TokenData
- Security: `app/core/security.py` — JWT create/decode, password hash/verify

## Future Additions

Agar user module me naya feature chahiye (e.g. password reset, profile update, user list for admin), toh:

1. Schema add karo `app/schemas/user.py` me (e.g. `UserUpdate`, `PasswordReset`)
2. Endpoint add karo `router.py` me
3. Agar DB model change ho toh migration banao: `make makemigrations msg="add xyz to users"`
