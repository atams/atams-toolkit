# ATAMS - Advanced Toolkit for Application Management System

Universal toolkit untuk semua AURA (Atams Universal Runtime Architecture) projects.

## Installation

```bash
pip install atams
```

## Quick Start

### Initialize New Project

```bash
atams init my-aura-app
cd my-aura-app
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Generate CRUD

```bash
cd my-aura-app
atams generate department
```

This creates:
- Model (SQLAlchemy)
- Schema (Pydantic)
- Repository (data access)
- Service (business logic)
- Endpoint (API routes)

And auto-registers the router to `api.py`!

## CLI Commands

### `atams init <project_name>`

Initialize a new AURA project with proper structure.

**Options:**
- `--app-name, -a`: Application name (default: project_name)
- `--version, -v`: Application version (default: 1.0.0)
- `--schema, -s`: Database schema name (default: aura)

**Example:**
```bash
atams init my-app --app-name "My Application" --schema myapp
```

### `atams generate <resource_name>`

Generate full CRUD boilerplate for a resource.

**Options:**
- `--schema, -s`: Database schema name (default: aura)
- `--skip-api`: Skip auto-registration to api.py

**Example:**
```bash
atams generate department
atams generate user_profile --schema myapp
```

**Generated files:**
- `app/models/{resource}.py`
- `app/schemas/{resource}.py`
- `app/repositories/{resource}_repository.py`
- `app/services/{resource}_service.py`
- `app/api/v1/endpoints/{resources}.py`

## Components

### 1. Database Layer

- BaseRepository (ORM + Native SQL)
- Session management
- Base declarative

### 2. Atlas SSO Integration

- AtlasClient
- Authentication dependencies
- Encryption/decryption

### 3. Response Encryption

- AES-256 encryption
- Auto-encryption untuk GET endpoints

### 4. Exception Handling

- Custom exceptions
- Global exception handlers

### 5. Middleware

- Request ID tracking
- Rate limiting

### 6. Logging

- Structured logging
- JSON formatter
- Colored console

### 7. Transaction Management

- Context managers
- Savepoints

### 8. Common Schemas

- Response schemas
- Pagination

## Development

For local development:

```bash
git clone <repo>
cd atams
python -m venv venv
venv\Scripts\activate  # Windows
pip install -e .
```

## Documentation

See `atams.md` for complete specification.

## Version

0.2.0 (Phase 2 - CLI Generator + Project Initializer)
