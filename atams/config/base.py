from pydantic_settings import BaseSettings
from typing import List, ClassVar
import json


class AtamsBaseSettings(BaseSettings):
    """
    Base settings untuk semua AURA applications
    Inherit class ini di project-specific settings

    ATLAS SSO CONSTANTS:
    - ATLAS_SSO_URL, ATLAS_ENCRYPTION_KEY, ATLAS_ENCRYPTION_IV are system constants
    - These CANNOT be overridden via .env file for security and consistency
    - Only ATLAS_APP_CODE is user-configurable
    """

    # Database (required per app)
    DATABASE_URL: str

    # Atlas SSO - User Configuration (only this is configurable!)
    ATLAS_APP_CODE: str

    # Atlas SSO - System Constants (FINAL - cannot be overridden!)
    # Using ClassVar to prevent Pydantic from allowing .env override
    ATLAS_SSO_URL: ClassVar[str] = "https://api.atlas-microapi.atamsindonesia.com/api/v1"
    ATLAS_ENCRYPTION_KEY: ClassVar[str] = "7c5f7132ba1a6e566bccc56416039bea"
    ATLAS_ENCRYPTION_IV: ClassVar[str] = "ce84582d0e6d2591"

    # Response Encryption (app-specific)
    ENCRYPTION_ENABLED: bool = False
    ENCRYPTION_KEY: str = "change_me_32_characters_long!!"  # Must be 32 chars
    ENCRYPTION_IV: str = "change_me_16char"  # Must be 16 chars

    # Logging (common pattern dengan defaults)
    LOGGING_ENABLED: bool = True
    LOG_LEVEL: str = "INFO"
    LOG_TO_FILE: bool = False
    LOG_FILE_PATH: str = "logs/app.log"

    # Debug mode
    DEBUG: bool = False

    # CORS Configuration (dengan default ATAMS ecosystem)
    CORS_ORIGINS: str = '["*"]'
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: str = '["*"]'
    CORS_ALLOW_HEADERS: str = '["*"]'

    # Rate Limiting (common pattern dengan defaults)
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60

    @property
    def cors_origins_list(self) -> List[str]:
        """
        Parse CORS_ORIGINS dengan default ATAMS security

        DEFAULT: Hanya *.atamsindonesia.com + localhost dev
        """
        try:
            origins = json.loads(self.CORS_ORIGINS)

            # Jika ["*"], apply default ATAMS security
            if origins == ["*"]:
                return [
                    "https://*.atamsindonesia.com",
                    "http://localhost:3000",
                    "http://localhost:8000",
                ]

            return origins
        except:
            return [
                "https://*.atamsindonesia.com",
                "http://localhost:3000",
                "http://localhost:8000",
            ]

    @property
    def cors_methods_list(self) -> List[str]:
        try:
            return json.loads(self.CORS_ALLOW_METHODS)
        except:
            return ["*"]

    @property
    def cors_headers_list(self) -> List[str]:
        try:
            return json.loads(self.CORS_ALLOW_HEADERS)
        except:
            return ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


def get_database_url():
    """Helper untuk get DATABASE_URL dari environment"""
    from os import getenv
    db_url = getenv("DATABASE_URL", "")
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)
    return db_url
