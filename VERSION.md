# Version History

## 1.1.0 (2025-01-10) - Enhanced Repository & Configuration

### Added
- ✅ **12 new BaseRepository methods** for advanced database operations:
  - `exists()` - Fast existence check without fetching record
  - `filter()` - Dynamic filtering with pagination and ordering
  - `first()` - Get first matching record
  - `count_filtered()` - Count records with conditions
  - `bulk_create()` - Batch insert (100x faster than loops)
  - `bulk_update()` - Batch update multiple records
  - `delete_many()` - Batch delete by IDs
  - `partial_update()` - Update without fetching first
  - `get_or_create()` - Atomic get or create pattern
  - `update_or_create()` - Upsert pattern
  - `soft_delete()` - Logical deletion with timestamp
  - `restore()` - Restore soft-deleted records

### Changed
- ✅ **Atlas SSO configuration** now fully customizable via .env
  - Removed `ClassVar` restriction on ATLAS_SSO_URL, ATLAS_ENCRYPTION_KEY, ATLAS_ENCRYPTION_IV
  - Generated projects can now configure Atlas for dev/staging/production environments
  - Updated `.env.example` template to include all Atlas configs

### Fixed
- ✅ LoggerAdapter type annotation errors in middleware and transaction modules
  - Fixed `atams/middleware/rate_limiter.py`
  - Fixed `atams/middleware/request_id.py`
  - Fixed `atams/transaction/manager.py`

### Breaking Changes
- None (all changes are backwards compatible)

### Documentation
- ✅ Comprehensive BaseRepository function reference in README
- ✅ Usage examples for all new methods
- ✅ Updated version badges

---

## 1.0.0 (2025-01-10) - Initial Release

### Features
- ✅ Core components (Database, SSO, Encryption, Exceptions, Middleware, Logging)
- ✅ CLI tool (`atams init`, `atams generate`)
- ✅ Jinja2 templates for code generation
- ✅ Auto-import injection
- ✅ CORS default security (*.atamsindonesia.com)
- ✅ Complete documentation
- ✅ CI/CD pipeline
- ✅ Published to PyPI

### Components
- Database layer with BaseRepository (ORM & Native SQL)
- Atlas SSO integration
- Response encryption (AES-256)
- Exception handling & global handlers
- Request ID middleware
- Rate limiting middleware
- Structured logging
- Transaction management
- Common schemas (Response, Pagination)

### CLI
- `atams init <project>` - Initialize new AURA project
- `atams generate <resource>` - Generate full CRUD boilerplate
- `atams --version` - Show version

### Breaking Changes
- None (initial release)

### Known Issues
- None

---

## Future Releases

### 1.2.0 (Planned)
- Redis caching support
- Database migration helper
- Auto-generate test cases
- CLI command for database seeding

### 2.0.0 (Planned)
- Multi-database support (MySQL, MongoDB)
- GraphQL support
- WebSocket support
- Admin panel generator
