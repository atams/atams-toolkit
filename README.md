# ATAMS - Advanced Toolkit for Application Management System

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![License](https://img.shields.io/badge/license-MIT-blue)

Universal toolkit untuk semua **AURA (Atams Universal Runtime Architecture)** projects.

## Features

- 🚀 **Instant CRUD Generation** - Generate full boilerplate in seconds
- 🏗️ **Clean Architecture** - Enforced separation of concerns  
- 🔒 **Security by Default** - Atlas SSO, encryption, RBAC
- 📦 **Reusable Components** - Database, middleware, logging, etc.
- 🎨 **CLI Tool** - Project initialization & code generation
- 🌐 **CORS Protection** - Default to `*.atamsindonesia.com`

## Installation

```bash
pip install atams
```

## Quick Start

### 1. Initialize New Project

```bash
atams init my-app
cd my-app
cp .env.example .env
# Edit .env with your configuration
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2. Generate CRUD

```bash
atams generate department
```

Generates:
- ✅ Model (SQLAlchemy)
- ✅ Schema (Pydantic)
- ✅ Repository (data access)
- ✅ Service (business logic)
- ✅ Endpoint (API routes)
- ✅ Auto-registered to `api.py`

### 3. Customize & Run

Edit generated files to add custom logic, then test:

```bash
# Access API docs
http://localhost:8000/docs

# Test endpoints
GET  /api/v1/departments
GET  /api/v1/departments/{id}
POST /api/v1/departments
PUT  /api/v1/departments/{id}
DELETE /api/v1/departments/{id}
```

## Components

### Core Components

1. **Database Layer** - BaseRepository with ORM & Native SQL
2. **Atlas SSO** - Authentication & authorization
3. **Response Encryption** - AES-256 for GET endpoints
4. **Exception Handling** - Standardized error responses
5. **Middleware** - Request ID tracking, rate limiting
6. **Logging** - Structured logging with JSON format
7. **Transaction Management** - Context managers for complex operations
8. **Common Schemas** - Response & pagination schemas

### Configuration

ATAMS provides `AtamsBaseSettings` with sensible defaults:

```python
from atams import AtamsBaseSettings

class Settings(AtamsBaseSettings):
    APP_NAME: str = "MyApp"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # App-specific encryption
    ENCRYPTION_KEY: str = "your-key-32-chars"
    ENCRYPTION_IV: str = "your-iv-16-char"

settings = Settings()
```

**CORS Default:** Hanya `*.atamsindonesia.com` + localhost (development)

Override via `.env`:

```env
CORS_ORIGINS=["https://myapp.atamsindonesia.com"]
```

## CLI Commands

### `atams init <project_name>`

Initialize new AURA project with complete structure.

**Options:**
- `--app-name, -a` - Application name (default: project_name)
- `--version, -v` - Application version (default: 1.0.0)
- `--schema, -s` - Database schema (default: aura)

**Example:**

```bash
atams init my-new-app
```

### `atams generate <resource>`

Generate full CRUD boilerplate for a resource.

**Options:**
- `--schema, -s` - Database schema (default: aura)
- `--skip-api` - Skip auto-registration to api.py

**Example:**

```bash
atams generate department
atams generate user --schema=public
```

### `atams --version`

Show toolkit version.

## Project Structure

```
my-app/
├── app/
│   ├── core/              # Configuration
│   │   └── config.py
│   ├── db/                # Database
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   ├── repositories/      # Data access layer
│   ├── services/          # Business logic layer
│   └── api/               # API endpoints
│       └── v1/
│           ├── api.py
│           └── endpoints/
├── tests/                 # Test files
├── .env.example           # Environment template
├── requirements.txt       # Dependencies
└── README.md
```

## Usage Examples

### Using BaseRepository

```python
from atams import BaseRepository
from app.models.user import User

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)
    
    # ORM methods (inherited)
    # - get(db, id)
    # - get_multi(db, skip, limit)
    # - create(db, obj_in)
    # - update(db, db_obj, obj_in)
    # - delete(db, id)
    
    # Custom native SQL
    def get_active_users(self, db):
        query = "SELECT * FROM users WHERE status = :status"
        return self.execute_raw_sql_dict(db, query, {"status": "active"})
```

### Using Atlas SSO

```python
from atams.sso import require_auth, require_min_role_level

@router.get("/admin", dependencies=[Depends(require_min_role_level(50))])
async def admin_dashboard(current_user: dict = Depends(require_auth)):
    # Only users with role level >= 50 can access
    return {"user": current_user}
```

### Using Response Encryption

```python
from atams.encryption import encrypt_response_data
from atams.schemas import DataResponse

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    user = get_user_from_db(user_id)
    response = DataResponse(
        success=True,
        message="User retrieved",
        data=user
    )
    # Auto-encrypt if ENCRYPTION_ENABLED=true
    return encrypt_response_data(response)
```

## Development

### Setup

```bash
git clone https://github.com/atams/atams-toolkit
cd atams-toolkit
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest tests/ -v
pytest tests/ --cov=atams --cov-report=html
```

### Build Package

```bash
python -m build
```

## Versioning

ATAMS follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality (backwards compatible)
- **PATCH** version for bug fixes

Current version: **1.0.0**

## Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## License

MIT License - see LICENSE file for details.

## Links

- Documentation: [https://atams-toolkit.readthedocs.io](https://atams-toolkit.readthedocs.io/)
- GitHub: [https://github.com/atams/atams-toolkit](https://github.com/atams/atams-toolkit)
- PyPI: [https://pypi.org/project/atams](https://pypi.org/project/atams)
- Issues: [https://github.com/atams/atams-toolkit/issues](https://github.com/atams/atams-toolkit/issues)

## Support

For support, email [support@atamsindonesia.com](mailto:support@atamsindonesia.com) or open an issue on GitHub.
