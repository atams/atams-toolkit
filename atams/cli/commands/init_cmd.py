"""
ATAMS Init Command
Initialize new AURA project
"""
import typer
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from atams.utils import write_file, ensure_dir

console = Console()


def init_project(
    project_name: str = typer.Argument(..., help="Project name"),
    app_name: str = typer.Option(None, "--app-name", "-a", help="Application name (default: project_name)"),
    app_version: str = typer.Option("1.0.0", "--version", "-v", help="Application version"),
    db_schema: str = typer.Option("aura", "--schema", "-s", help="Database schema name"),
):
    """
    Initialize a new AURA project with proper structure

    Example:
        atams init my-aura-app
        atams init my-app --app-name "My Application" --schema myapp
    """
    if app_name is None:
        app_name = project_name.replace('-', '_').replace(' ', '_')

    console.print(f"\n[bold cyan]Initializing AURA project:[/bold cyan] {project_name}")
    console.print(f"[dim]App Name:[/dim] {app_name}")
    console.print(f"[dim]Version:[/dim] {app_version}")
    console.print(f"[dim]Schema:[/dim] {db_schema}")
    console.print()

    # Project root
    project_dir = Path.cwd() / project_name

    if project_dir.exists():
        console.print(f"[red]❌ Error: Directory '{project_name}' already exists[/red]")
        raise typer.Exit(1)

    # Create directory structure
    directories = [
        project_dir / "app",
        project_dir / "app" / "core",
        project_dir / "app" / "db",
        project_dir / "app" / "models",
        project_dir / "app" / "schemas",
        project_dir / "app" / "repositories",
        project_dir / "app" / "services",
        project_dir / "app" / "api",
        project_dir / "app" / "api" / "v1",
        project_dir / "app" / "api" / "v1" / "endpoints",
        project_dir / "tests",
    ]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Creating directory structure...", total=len(directories))

        for directory in directories:
            ensure_dir(directory)
            progress.advance(task)

    console.print("[green]Created directory structure[/green]")

    # Create files
    files_created = []

    # main.py
    main_content = f'''"""
{app_name} - AURA Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.models import SecuritySchemeType, HTTPBearer
from atams.db import init_database
from atams.logging import setup_logging_from_settings
from atams.middleware import RequestIDMiddleware
from atams.exceptions import setup_exception_handlers

from app.core.config import settings
from app.api.v1.api import api_router

# Setup logging
setup_logging_from_settings(settings)

# Initialize database
init_database(settings.DATABASE_URL, settings.DEBUG)

# Create FastAPI app with Bearer token security
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    swagger_ui_parameters={{
        "persistAuthorization": True,
    }},
)

# Add security scheme for Swagger UI
app.openapi_schema = None  # Reset to regenerate with security


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    from fastapi.openapi.utils import get_openapi

    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        routes=app.routes,
    )

    # Add Bearer token security scheme
    openapi_schema["components"]["securitySchemes"] = {{
        "BearerAuth": {{
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your Atlas SSO JWT token"
        }}
    }}

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.cors_methods_list,
    allow_headers=settings.cors_headers_list,
)

# Request ID middleware
app.add_middleware(RequestIDMiddleware)

# Exception handlers
setup_exception_handlers(app)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {{"name": settings.APP_NAME, "version": settings.APP_VERSION}}


@app.get("/health")
async def health():
    return {{"status": "ok"}}
'''
    write_file(project_dir / "app" / "main.py", main_content)
    files_created.append("app/main.py")

    # config.py
    config_content = f'''from atams import AtamsBaseSettings


class Settings(AtamsBaseSettings):
    """
    Application Settings

    Inherits from AtamsBaseSettings which includes:
    - DATABASE_URL (required)
    - ATLAS_SSO_URL, ATLAS_APP_CODE, ATLAS_ENCRYPTION_KEY, ATLAS_ENCRYPTION_IV
    - ENCRYPTION_ENABLED, ENCRYPTION_KEY, ENCRYPTION_IV (response encryption)
    - LOGGING_ENABLED, LOG_LEVEL, LOG_TO_FILE, LOG_FILE_PATH
    - CORS_ORIGINS, CORS_ALLOW_CREDENTIALS, CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS
    - RATE_LIMIT_ENABLED, RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW
    - DEBUG

    All settings can be overridden via .env file or by redefining them here.
    """
    APP_NAME: str = "{app_name}"
    APP_VERSION: str = "{app_version}"


settings = Settings()
'''
    write_file(project_dir / "app" / "core" / "config.py", config_content)
    files_created.append("app/core/config.py")

    # __init__.py files
    write_file(project_dir / "app" / "__init__.py", "")
    write_file(project_dir / "app" / "core" / "__init__.py", "")
    write_file(project_dir / "app" / "db" / "__init__.py", "")
    write_file(project_dir / "app" / "models" / "__init__.py", "")
    write_file(project_dir / "app" / "schemas" / "__init__.py", "")
    write_file(project_dir / "app" / "repositories" / "__init__.py", "")
    write_file(project_dir / "app" / "services" / "__init__.py", "")
    write_file(project_dir / "app" / "api" / "__init__.py", "")
    write_file(project_dir / "app" / "api" / "v1" / "__init__.py", "")
    write_file(project_dir / "app" / "api" / "v1" / "endpoints" / "__init__.py", "")
    write_file(project_dir / "tests" / "__init__.py", "")

    # api.py
    api_content = '''from fastapi import APIRouter

api_router = APIRouter()

# Import and register routers here
# Example:
# from app.api.v1.endpoints import users
# api_router.include_router(users.router, prefix="/users", tags=["Users"])
'''
    write_file(project_dir / "app" / "api" / "v1" / "api.py", api_content)
    files_created.append("app/api/v1/api.py")

    # .env.example
    env_content = f'''# Application
APP_NAME={app_name}
APP_VERSION={app_version}
DEBUG=true

# Database
DATABASE_URL=postgresql://user:password@localhost/{project_name.replace('-', '_')}

# Atlas SSO
ATLAS_SSO_URL=https://atlas.atamsindonesia.com
ATLAS_APP_CODE={app_name.upper().replace(' ', '_')}

# Response Encryption
# IMPORTANT: Generate secure keys using:
#   Key (32 chars): openssl rand -hex 16
#   IV (16 chars):  openssl rand -hex 8
ENCRYPTION_ENABLED=true
ENCRYPTION_KEY=change_me_32_characters_long!!
ENCRYPTION_IV=change_me_16char

# Logging
LOGGING_ENABLED=true
LOG_LEVEL=INFO
LOG_TO_FILE=false

# CORS (optional - defaults to *.atamsindonesia.com)
# CORS_ORIGINS=["*"]

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
'''
    write_file(project_dir / ".env.example", env_content)
    files_created.append(".env.example")

    # requirements.txt
    requirements = '''# ATAMS Toolkit (includes fastapi, sqlalchemy, pydantic, email-validator, etc.)
atams>=1.0.0

# Database Driver (choose based on your database)
psycopg2-binary>=2.9.0  # PostgreSQL
# mysqlclient>=2.2.0    # MySQL
# cx_Oracle>=8.3.0      # Oracle

# FastAPI Server
uvicorn[standard]>=0.24.0

# Environment variables
python-dotenv>=1.0.0
'''
    write_file(project_dir / "requirements.txt", requirements)
    files_created.append("requirements.txt")

    # .gitignore
    gitignore = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
logs/
*.log

# OS
.DS_Store
Thumbs.db

# Database
*.db
*.sqlite3
'''
    write_file(project_dir / ".gitignore", gitignore)
    files_created.append(".gitignore")

    # README.md
    readme = f'''# {app_name}

AURA Application built with ATAMS toolkit.

## Setup

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Run application:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Access API:
   - Docs: http://localhost:8000/docs
   - Health: http://localhost:8000/health
   - Example Users API: http://localhost:8000/api/v1/users

## Example Endpoints

This project includes a complete working example (Users CRUD) that demonstrates:
- Two-level authorization (Route + Service)
- Atlas SSO authentication
- Response encryption
- ORM usage with BaseRepository
- Proper error handling

**Available endpoints:**
- GET /api/v1/users - List all users (requires role level >= 50)
- GET /api/v1/users/{{id}} - Get single user (requires role level >= 10)
- POST /api/v1/users - Create user (requires role level >= 50)

## Generate CRUD

```bash
atams generate <resource_name>
```

Example:
```bash
atams generate department
```

## Project Structure

```
{project_name}/
├── app/
│   ├── core/           # Configuration
│   ├── db/             # Database setup
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   ├── repositories/   # Data access layer
│   ├── services/       # Business logic layer
│   └── api/            # API endpoints
├── tests/              # Test files
├── .env.example        # Environment template
└── requirements.txt    # Dependencies
```

## Documentation

See ATAMS documentation for more information.
'''
    write_file(project_dir / "README.md", readme)
    files_created.append("README.md")

    # deps.py - API dependencies with SSO
    deps_content = '''"""
API Dependencies
Provides authentication and authorization dependencies
"""
from fastapi import Depends, Header, HTTPException, status
from typing import Dict, Any

from atams.sso import AtlasClient
from app.core.config import settings

# Initialize Atlas SSO client
atlas_client = AtlasClient(
    base_url=settings.ATLAS_SSO_URL,
    app_code=settings.ATLAS_APP_CODE,
    encryption_key=settings.ATLAS_ENCRYPTION_KEY,
    encryption_iv=settings.ATLAS_ENCRYPTION_IV
)


async def require_auth(authorization: str = Header(None)) -> Dict[str, Any]:
    """
    Require authentication via Atlas SSO

    Usage:
        @router.get("/protected")
        async def protected_route(current_user: dict = Depends(require_auth)):
            return {"user": current_user}

    Returns:
        Dict containing user info: {
            "user_id": int,
            "username": str,
            "role_level": int,
            "organization_id": int
        }

    Raises:
        HTTPException 401 if token invalid/missing
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header"
        )

    token = authorization.replace("Bearer ", "")

    # Verify token dengan Atlas SSO
    user_data = await atlas_client.verify_token(token)

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return user_data


def require_min_role_level(min_level: int):
    """
    Require minimum role level

    Usage:
        @router.get("/admin", dependencies=[Depends(require_min_role_level(50))])
        async def admin_route():
            return {"message": "Admin only"}

    Role Levels:
        10 = User
        50 = Admin
        100 = Super Admin
    """
    async def role_checker(current_user: Dict = Depends(require_auth)):
        if current_user.get("role_level", 0) < min_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required level: {{min_level}}"
            )
        return current_user

    return role_checker
'''
    write_file(project_dir / "app" / "api" / "deps.py", deps_content)
    files_created.append("app/api/deps.py")

    # db/session.py
    session_content = '''"""
Database Session Management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.config import settings

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency

    Usage:
        @router.get("/")
        async def endpoint(db: Session = Depends(get_db)):
            # Use db here
            pass
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''
    write_file(project_dir / "app" / "db" / "session.py", session_content)
    files_created.append("app/db/session.py")

    # Example Model - User
    user_model = f'''"""
Example User Model
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from atams.db import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {{"schema": "{db_schema}"}}

    u_id = Column(Integer, primary_key=True, index=True)
    u_name = Column(String(100), nullable=False)
    u_email = Column(String(100), unique=True, index=True, nullable=False)
    u_is_active = Column(Boolean, default=True)
    u_created_at = Column(DateTime(timezone=True), server_default=func.now())
    u_updated_at = Column(DateTime(timezone=True), onupdate=func.now())
'''
    write_file(project_dir / "app" / "models" / "user.py", user_model)
    files_created.append("app/models/user.py")

    # Example Schema - User
    user_schema = '''"""
Example User Schemas
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    u_name: str
    u_email: EmailStr


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    u_name: Optional[str] = None
    u_email: Optional[EmailStr] = None
    u_is_active: Optional[bool] = None


class User(UserBase):
    u_id: int
    u_is_active: bool
    u_created_at: datetime
    u_updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
'''
    write_file(project_dir / "app" / "schemas" / "user.py", user_schema)
    files_created.append("app/schemas/user.py")

    # Common schemas
    common_schema = '''"""
Common Response Schemas
"""
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, List

T = TypeVar("T")


class ResponseBase(BaseModel):
    success: bool
    message: str


class DataResponse(ResponseBase, Generic[T]):
    data: Optional[T] = None


class PaginationResponse(ResponseBase, Generic[T]):
    data: List[T]
    total: int
    page: int
    size: int
    pages: int
'''
    write_file(project_dir / "app" / "schemas" / "common.py", common_schema)
    files_created.append("app/schemas/common.py")

    # Example Repository - User
    user_repo = '''"""
Example User Repository
"""
from atams.db import BaseRepository
from app.models.user import User


class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    # Add custom methods here
    def get_by_email(self, db, email: str):
        """Get user by email"""
        return db.query(User).filter(User.u_email == email).first()
'''
    write_file(project_dir / "app" / "repositories" / "user_repository.py", user_repo)
    files_created.append("app/repositories/user_repository.py")

    # Example Service - User
    user_service = '''"""
Example User Service
Implements business logic with two-level authorization
"""
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from atams.exceptions import NotFoundException, ForbiddenException, BadRequestException


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def get_users(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        current_user_role_level: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get users with authorization check

        Authorization:
        - Level 100: Can view all users
        - Level 50: Can view users in organization (not implemented in example)
        - Below 50: Forbidden
        """
        if current_user_role_level < 50:
            raise ForbiddenException("Insufficient permissions to view users")

        users = self.repo.get_multi(db, skip=skip, limit=limit)

        return [
            {{
                "id": user.u_id,
                "name": user.u_name,
                "email": user.u_email,
                "is_active": user.u_is_active,
                "created_at": str(user.u_created_at)
            }}
            for user in users
        ]

    def get_user(
        self,
        db: Session,
        user_id: int,
        current_user_role_level: int = 0,
        current_user_id: int = None
    ) -> Dict[str, Any]:
        """
        Get single user with authorization

        Authorization:
        - Level 100: Can view any user
        - Level 50: Can view users in organization
        - Level 10: Can only view own profile
        """
        user = self.repo.get(db, user_id)
        if not user:
            raise NotFoundException(f"User {{user_id}} not found")

        # Check permissions
        if current_user_role_level < 50:
            # User can only view own profile
            if user.u_id != current_user_id:
                raise ForbiddenException("Can only view own profile")

        return {{
            "id": user.u_id,
            "name": user.u_name,
            "email": user.u_email,
            "is_active": user.u_is_active,
            "created_at": str(user.u_created_at)
        }}

    def create_user(
        self,
        db: Session,
        user_in: UserCreate,
        current_user_role_level: int = 0
    ) -> Dict[str, Any]:
        """
        Create user

        Authorization:
        - Level 100: Can create any user
        - Level 50: Can create users with level < 50
        """
        if current_user_role_level < 50:
            raise ForbiddenException("Insufficient permissions to create users")

        # Check if email exists
        existing = self.repo.get_by_email(db, user_in.u_email)
        if existing:
            raise BadRequestException(f"Email {{user_in.u_email}} already exists")

        # Create user
        user = self.repo.create(db, obj_in=user_in)

        return {{
            "id": user.u_id,
            "name": user.u_name,
            "email": user.u_email,
            "is_active": user.u_is_active
        }}

    def get_total_users(self, db: Session) -> int:
        """Get total user count"""
        return self.repo.count(db)
'''
    write_file(project_dir / "app" / "services" / "user_service.py", user_service)
    files_created.append("app/services/user_service.py")

    # Example Endpoint - Users
    users_endpoint = '''"""
Example Users Endpoint
Demonstrates complete ATAMS patterns
"""
from fastapi import APIRouter, Depends, Query, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.services.user_service import UserService
from app.schemas.user import User, UserCreate, UserUpdate
from app.schemas.common import DataResponse, PaginationResponse
from app.api.deps import require_auth, require_min_role_level
from atams.encryption import create_response_encryption, create_encrypt_response_function

router = APIRouter()
user_service = UserService()
security = HTTPBearer()

# Setup response encryption
_encryption = create_response_encryption(settings.ENCRYPTION_KEY, settings.ENCRYPTION_IV)
encrypt_response = create_encrypt_response_function(settings.ENCRYPTION_ENABLED, _encryption)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_min_role_level(50)), Security(security)]  # FIRST LEVEL: Route
)
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_auth)
):
    """
    Get list of users with pagination

    **Two-Level Authorization:**
    - FIRST (Route): Requires role level >= 50
    - SECOND (Service): Level 100 sees all, Level 50 sees organization

    **Response**: Encrypted if ENCRYPTION_ENABLED=true
    """
    users = user_service.get_users(
        db,
        skip=skip,
        limit=limit,
        current_user_role_level=current_user["role_level"]
    )
    total = user_service.get_total_users(db)

    response = PaginationResponse(
        success=True,
        message="Users retrieved successfully",
        data=users,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )

    return encrypt_response(response)


@router.get(
    "/{{user_id}}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_min_role_level(10)), Security(security)]
)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_auth)
):
    """Get single user by ID"""
    user = user_service.get_user(
        db,
        user_id,
        current_user_role_level=current_user["role_level"],
        current_user_id=current_user["user_id"]
    )

    response = DataResponse(
        success=True,
        message="User retrieved successfully",
        data=user
    )

    return encrypt_response(response)


@router.post(
    "/",
    response_model=DataResponse[User],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_min_role_level(50)), Security(security)]
)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_auth)
):
    """Create new user"""
    new_user = user_service.create_user(
        db,
        user,
        current_user_role_level=current_user["role_level"]
    )

    return DataResponse(
        success=True,
        message="User created successfully",
        data=new_user
    )
'''
    write_file(project_dir / "app" / "api" / "v1" / "endpoints" / "users.py", users_endpoint)
    files_created.append("app/api/v1/endpoints/users.py")

    # Update api.py to include users
    api_update = '''from fastapi import APIRouter
from app.api.v1.endpoints import users

api_router = APIRouter()

# Register routes
api_router.include_router(users.router, prefix="/users", tags=["Users"])
'''
    write_file(project_dir / "app" / "api" / "v1" / "api.py", api_update)

    # Success summary
    console.print()
    console.print("[bold green]Project created successfully![/bold green]")
    console.print()
    console.print("[bold]Files created:[/bold]")
    for file in files_created:
        console.print(f"  [green]+[/green] {file}")

    console.print()
    console.print("[bold]Next steps:[/bold]")
    console.print(f"  1. [cyan]cd {project_name}[/cyan]")
    console.print(f"  2. [cyan]cp .env.example .env[/cyan]")
    console.print(f"  3. Generate encryption keys:")
    console.print(f"     [cyan]openssl rand -hex 16[/cyan]  # Copy to ENCRYPTION_KEY")
    console.print(f"     [cyan]openssl rand -hex 8[/cyan]   # Copy to ENCRYPTION_IV")
    console.print(f"  4. Edit .env with your configuration (database, keys, etc.)")
    console.print(f"  5. [cyan]python -m venv venv[/cyan]")
    console.print(f"  6. [cyan]venv\\Scripts\\activate[/cyan]  # On Windows")
    console.print(f"  7. [cyan]pip install -r requirements.txt[/cyan]")
    console.print(f"  8. [cyan]uvicorn app.main:app --reload[/cyan]")
    console.print()
