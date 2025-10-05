# Changelog

All notable changes to the ATAMS toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[1.1.0]: https://github.com/atams/atams-toolkit/releases/tag/v1.1.0
[1.0.0]: https://github.com/atams/atams-toolkit/releases/tag/v1.0.0
