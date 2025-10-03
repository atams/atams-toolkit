"""
Test imports untuk ATAMS package
Run this after: pip install -e .
"""

print("Testing ATAMS imports...")

# Test main imports
try:
    from atams import (
        __version__,
        AtamsBaseSettings,
        Base,
        get_db,
        init_database,
        BaseRepository,
        AppException,
        BadRequestException,
        NotFoundException,
        setup_exception_handlers,
        DataResponse,
        PaginationResponse,
        setup_logging,
        get_logger,
    )
    print("✅ Core imports successful!")
    print(f"✅ ATAMS version: {__version__}")
except Exception as e:
    print(f"❌ Core imports failed: {e}")

# Test SSO imports
try:
    from atams.sso import AtlasClient, create_atlas_client_from_settings, create_auth_dependencies
    print("✅ SSO imports successful!")
except Exception as e:
    print(f"❌ SSO imports failed: {e}")

# Test encryption imports
try:
    from atams.encryption import ResponseEncryption, create_response_encryption
    print("✅ Encryption imports successful!")
except Exception as e:
    print(f"❌ Encryption imports failed: {e}")

# Test middleware imports
try:
    from atams.middleware import RequestIDMiddleware, create_rate_limit_middleware
    print("✅ Middleware imports successful!")
except Exception as e:
    print(f"❌ Middleware imports failed: {e}")

# Test transaction imports
try:
    from atams.transaction import Transaction, transaction, savepoint
    print("✅ Transaction imports successful!")
except Exception as e:
    print(f"❌ Transaction imports failed: {e}")

print("\n✅ All import tests completed!")
print("\nNext steps:")
print("1. Create virtual environment: python -m venv venv")
print("2. Activate venv: venv\\Scripts\\activate (Windows) or source venv/bin/activate (Unix)")
print("3. Install dependencies: pip install -e .")
print("4. Run this test again: python test_imports.py")
