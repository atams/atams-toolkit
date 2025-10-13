# Changelog

All notable changes to the ATAMS toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.4] - 2025-01-13

### Added
- **Configurable Database Connection Pool Settings** to prevent "remaining connection slots" errors:
  - Added `DB_POOL_SIZE` (default: 3) - Number of persistent connections
  - Added `DB_MAX_OVERFLOW` (default: 5) - Additional overflow connections
  - Added `DB_POOL_RECYCLE` (default: 3600) - Recycle connections after N seconds
  - Added `DB_POOL_TIMEOUT` (default: 30) - Timeout waiting for connection
  - Added `DB_POOL_PRE_PING` (default: True) - Health check before using connection
  - All settings configurable via `.env` for flexibility across environments

- **Connection Pool Monitoring Utilities**:
  - `get_pool_status()` - Get real-time connection pool statistics
  - `dispose_pool()` - Clean up all connections in pool
  - `check_connection_health()` - Verify database connection health
  - `get_connection_url_info()` - Get sanitized connection info (without password)

- **Built-in Health Check Endpoints** (`atams.api.health_router`):
  - `GET /health` - Basic application health check
  - `GET /health/db` - Database health with connection pool statistics
  - `GET /health/full` - Full system health check (app + database)
  - Auto-mountable router for easy integration: `app.include_router(health_router, prefix="/health")`
  - Returns proper HTTP status codes (200 OK, 503 Service Unavailable)

### Changed
- **BREAKING**: `init_database()` now accepts optional pool configuration parameters
  - Backward compatible: existing code works with new conservative defaults
  - Old hardcoded values (`pool_size=10, max_overflow=20`) replaced with configurable defaults
  - `create_engine_from_settings()` now reads pool settings from `AtamsBaseSettings`

- **Project Template Updates** (`atams init`):
  - `.env.example` now includes all 5 DB pool settings with explanations
  - `main.py` template auto-configures pool settings from `.env`
  - Health check endpoints auto-mounted by default
  - Apps created with `atams init` now have built-in monitoring out-of-the-box

### Fixed
- **Critical**: Fixed default pool settings causing connection exhaustion on free-tier databases
  - Previous: `pool_size=10, max_overflow=20` (30 max per app) - too aggressive
  - Current: `pool_size=3, max_overflow=5` (8 max per app) - safe for Aiven free tier (20 limit)
  - Added `pool_recycle` to prevent stale connections
  - Added `pool_timeout` to prevent indefinite waiting

### Documentation
- Added comprehensive "Database Connection Pool Configuration" section to README
- Included formula for calculating pool settings based on database limits
- Added examples for Aiven free tier and production environments
- Added "Built-in Health Check Endpoints" section with 3 endpoint examples
- Documented health router integration and response formats
- Updated core components list to include health monitoring
- Updated with connection pool monitoring best practices

## [1.1.3] - 2025-01-10

## [1.1.2] - 2025-01-10

## [1.1.1] - 2025-01-10

### Fixed
- Fixed undefined `LoggerAdapter` reference in `atams/middleware/request_id.py` causing flake8 F821 errors
- Simplified logger usage by removing unnecessary LoggerAdapter wrapper

## [1.1.0] - 2025-01-10

### Added
- **12 new BaseRepository methods** for advanced database operations:
  - `exists(db, id)` - Fast existence check without fetching entire record
  - `filter(db, filters, skip, limit, order_by)` - Dynamic filtering with pagination and custom ordering
  - `first(db, filters, order_by)` - Get first matching record based on filters
  - `count_filtered(db, filters)` - Count records matching specific conditions
  - `bulk_create(db, objects)` - Batch insert multiple records (100x faster than loops)
  - `bulk_update(db, objects)` - Batch update multiple records at once
  - `delete_many(db, ids)` - Delete multiple records by their IDs
  - `partial_update(db, id, data)` - Update record fields without fetching first
  - `get_or_create(db, defaults, **filters)` - Atomic get existing or create new record
  - `update_or_create(db, filters, defaults)` - Update existing or create (upsert pattern)
  - `soft_delete(db, id, deleted_at_field)` - Logical deletion using timestamp field
  - `restore(db, id, deleted_at_field)` - Restore soft-deleted records

### Changed
- **Atlas SSO configuration** made fully customizable via `.env` files:
  - Removed `ClassVar` restriction from `ATLAS_SSO_URL`, `ATLAS_ENCRYPTION_KEY`, `ATLAS_ENCRYPTION_IV`
  - Generated projects can now configure different Atlas environments (dev/staging/production)
  - Updated project template's `.env.example` to include all 4 Atlas configuration parameters
  - Developers can now override Atlas settings without modifying core code

### Fixed
- Fixed `LoggerAdapter` type annotation errors causing Pylance warnings:
  - `atams/middleware/rate_limiter.py` - Changed to `Optional[Any]` with proper TYPE_CHECKING guard
  - `atams/middleware/request_id.py` - Removed redundant variable in type expression
  - `atams/transaction/manager.py` - Changed to `Optional[Any]` with proper TYPE_CHECKING guard

### Documentation
- Added comprehensive BaseRepository function reference table in README
- Organized functions into 5 categories: Basic CRUD, Advanced Queries, Bulk Operations, Soft Delete, Native SQL
- Added practical usage examples for all new repository methods
- Updated version badges to reflect v1.1.0
- Enhanced code examples with real-world patterns (get_or_create, bulk operations, soft delete)

## [1.0.0] - 2025-01-10

### Added
- Initial release of ATAMS toolkit
- **Core Components**:
  - Database layer with `BaseRepository` (ORM & Native SQL support)
  - Atlas SSO integration for authentication and authorization
  - Response encryption using AES-256
  - Standardized exception handling with custom exception classes
  - Request ID tracking middleware
  - Rate limiting middleware
  - Structured JSON logging
  - Transaction management with context managers
  - Common Pydantic schemas (DataResponse, PaginationResponse, ErrorResponse)

- **CLI Tool**:
  - `atams init <project>` - Initialize new AURA project with complete structure
  - `atams generate <resource>` - Generate full CRUD boilerplate (model, schema, repository, service, endpoint)
  - `atams --version` - Display toolkit version
  - Auto-import injection for generated endpoints
  - Jinja2-based code generation templates

- **Configuration**:
  - `AtamsBaseSettings` base class for Pydantic settings
  - Database URL builder with schema support
  - CORS default security (*.atamsindonesia.com + localhost)
  - Environment-based configuration (.env support)

- **Security Features**:
  - Two-level authorization (route-level and service-level)
  - Encrypted response data for sensitive endpoints
  - Role-based access control (RBAC) via Atlas SSO
  - Factory pattern for dependency injection

### Documentation
- Complete README with usage examples
- Installation guide and quick start tutorial
- API reference for all core components
- Project structure documentation
- Contributing guidelines

### Infrastructure
- Python package structure with setuptools
- PyPI publishing configuration
- Git ignore configuration
- Development dependencies setup

---

## Future Releases

### [1.2.0] - Planned
- Redis caching layer for improved performance
- Database migration helper utilities
- Auto-generate test cases for CRUD operations
- CLI command for database seeding
- Performance monitoring middleware

### [2.0.0] - Planned
- Multi-database support (PostgreSQL, MySQL, MongoDB)
- GraphQL API generator
- WebSocket support for real-time features
- Admin panel generator
- Docker deployment templates
- OpenAPI schema auto-generation improvements

---

## Notes

### Version Numbering
- **MAJOR** (X.0.0): Breaking changes that require code modifications
- **MINOR** (0.X.0): New features added in backwards-compatible manner
- **PATCH** (0.0.X): Bug fixes and minor improvements

### Upgrade Guide
When upgrading between versions, check the "Changed" and "Breaking Changes" sections for any required modifications to your code.

[1.1.0]: https://github.com/GratiaManullang03/atams/releases/tag/v1.1.0
[1.0.0]: https://github.com/GratiaManullang03/atams/releases/tag/v1.0.0
