# Version History

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

### 1.1.0 (Planned)
- Redis caching support
- Database migration helper
- Auto-generate test cases
- CLI command for database seeding

### 2.0.0 (Planned)
- Multi-database support (MySQL, MongoDB)
- GraphQL support
- WebSocket support
- Admin panel generator
