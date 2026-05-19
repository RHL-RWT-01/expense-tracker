# Personal Expense Tracker API

A production-grade backend API for personal expense tracking, built with FastAPI, MongoDB, and modern Python practices.

## Features

- **Authentication**: JWT-based auth with access/refresh token rotation
- **User Management**: Secure registration, login, password management
- **Transactions**: Full CRUD for income/expense tracking with filtering
- **Categories**: Default + custom categories per user
- **Analytics**: Financial summaries, category breakdowns, monthly trends
- **Security**: Rate limiting, CORS, secure headers, input validation

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| Database | MongoDB |
| Driver | Motor (async) |
| Validation | Pydantic v2 |
| Auth | JWT (python-jose) |
| Password | bcrypt (passlib) |
| Logging | structlog |
| Container | Docker |

## Architecture

```
app/
├── api/
│   ├── dependencies/    # DI for auth and services
│   ├── middleware/      # Logging, errors, security
│   ├── routes/          # HTTP endpoints
│   └── validators/      # Request validation
├── core/
│   ├── config/          # Settings management
│   ├── security/        # JWT & password handling
│   ├── database/        # MongoDB connection
│   ├── exceptions/      # Custom exceptions
│   ├── logging/         # Structured logging
│   ├── constants/       # Enums and defaults
│   └── utils/           # Helper functions
├── models/              # Database document models
├── schemas/             # Pydantic request/response schemas
├── repositories/        # Data access layer
├── services/            # Business logic layer
├── main.py              # Application entry point
└── lifespan.py          # Startup/shutdown management
```

### Design Patterns

- **Repository Pattern**: Database operations isolated in repositories
- **Service Layer**: Business logic separated from HTTP concerns
- **Dependency Injection**: FastAPI's DI for loose coupling
- **DTO Pattern**: Separate schemas for requests/responses

## Getting Started

### Prerequisites

- Python 3.13+
- MongoDB 7.0+
- Docker (optional)

### Local Development

1. **Clone and setup**:
```bash
cd python-practice
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your settings
```

3. **Start MongoDB**:
```bash
# Using Docker
docker run -d -p 27017:27017 --name mongodb mongo:7.0

# Or use local MongoDB installation
```

4. **Run the API**:
```bash
uvicorn app.main:app --reload
```

5. **Access**:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/api/v1/health

### Docker Deployment

```bash
# Start all services
docker compose up -d

# With MongoDB Express (database UI)
docker compose --profile tools up -d

# View logs
docker compose logs -f api

# Stop services
docker compose down
```

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register new user |
| POST | `/api/v1/auth/login` | Login and get tokens |
| POST | `/api/v1/auth/refresh` | Refresh tokens |
| POST | `/api/v1/auth/logout` | Logout (revoke token) |
| POST | `/api/v1/auth/logout-all` | Logout all sessions |
| GET | `/api/v1/auth/me` | Get current user |
| PATCH | `/api/v1/auth/change-password` | Change password |

### Transactions
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/transactions` | Create transaction |
| GET | `/api/v1/transactions` | List with filters |
| GET | `/api/v1/transactions/{id}` | Get single |
| PATCH | `/api/v1/transactions/{id}` | Update |
| DELETE | `/api/v1/transactions/{id}` | Delete (soft) |

### Categories
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/categories` | List all |
| POST | `/api/v1/categories` | Create custom |
| PATCH | `/api/v1/categories/{id}` | Update custom |
| DELETE | `/api/v1/categories/{id}` | Delete custom |

### Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/analytics/summary` | Income/expense totals |
| GET | `/api/v1/analytics/category-breakdown` | Expense by category |
| GET | `/api/v1/analytics/monthly-trends` | Monthly trends |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | Expense Tracker API | Application name |
| `ENVIRONMENT` | development | Environment mode |
| `MONGODB_URL` | mongodb://localhost:27017 | MongoDB connection |
| `MONGODB_DATABASE` | expense_tracker | Database name |
| `JWT_SECRET_KEY` | (required) | Secret for JWT signing |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 30 | Access token lifetime |
| `REFRESH_TOKEN_EXPIRE_DAYS` | 7 | Refresh token lifetime |
| `CORS_ORIGINS` | ["http://localhost:3000"] | Allowed origins |
| `LOG_LEVEL` | INFO | Logging level |

## Security

- **Password Hashing**: bcrypt with automatic salt
- **JWT Tokens**: Short-lived access + rotating refresh tokens
- **Token Revocation**: Database-backed token invalidation
- **Rate Limiting**: Per-IP rate limits on auth endpoints
- **Input Validation**: Strict Pydantic validation
- **Security Headers**: X-Frame-Options, CSP, HSTS
- **User Isolation**: All data queries scoped to user

## Database Indexes

Optimized indexes for common queries:

- `users.email` (unique)
- `transactions.user_id`
- `transactions.category_id`
- `transactions.(user_id, transaction_date)`
- `categories.(user_id, name)` (unique)
- `refresh_tokens.token` (unique)
- `refresh_tokens.expires_at` (TTL)

## Scalability Considerations

The architecture supports future scaling:

- **Caching**: Add Redis for session/data caching
- **Background Jobs**: Integrate Celery for async tasks
- **Microservices**: Modules can be extracted to services
- **Event-Driven**: Add message queues for decoupling
- **Horizontal Scaling**: Stateless design enables scaling

## Development

### Code Quality
```bash
# Format code
black app/

# Lint
ruff check app/

# Run tests
pytest
```

### Project Structure Rules

1. Routes handle HTTP only - no business logic
2. Services contain business logic
3. Repositories handle database operations
4. No direct DB calls from routes
5. Use dependency injection throughout

## License

MIT
