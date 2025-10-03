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

    console.print(f"\n[bold cyan]🚀 Initializing AURA project:[/bold cyan] {project_name}")
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

    console.print("[green]✅ Created directory structure[/green]")

    # Create files
    files_created = []

    # main.py
    main_content = f'''"""
{app_name} - AURA Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

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
    APP_NAME: str = "{app_name}"
    APP_VERSION: str = "{app_version}"
    DEBUG: bool = True

    # App-specific encryption (set in .env)
    ENCRYPTION_KEY: str = "change_me_32_characters_long!!"
    ENCRYPTION_IV: str = "change_me_16char"


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

# Response Encryption (GENERATE NEW KEYS!)
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
    requirements = '''# ATAMS Toolkit
atams>=0.2.0

# FastAPI
fastapi>=0.104.0
uvicorn[standard]>=0.24.0

# Database
sqlalchemy>=2.0.0
psycopg2-binary>=2.9.0

# Others
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

    # Success summary
    console.print()
    console.print("[bold green]🎉 Project created successfully![/bold green]")
    console.print()
    console.print("[bold]Files created:[/bold]")
    for file in files_created:
        console.print(f"  [green]✅[/green] {file}")

    console.print()
    console.print("[bold]Next steps:[/bold]")
    console.print(f"  1. [cyan]cd {project_name}[/cyan]")
    console.print(f"  2. [cyan]cp .env.example .env[/cyan]")
    console.print(f"  3. Edit .env with your configuration")
    console.print(f"  4. [cyan]python -m venv venv[/cyan]")
    console.print(f"  5. [cyan]venv\\Scripts\\activate[/cyan]  # On Windows")
    console.print(f"  6. [cyan]pip install -r requirements.txt[/cyan]")
    console.print(f"  7. [cyan]uvicorn app.main:app --reload[/cyan]")
    console.print()
