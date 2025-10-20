"""
Configurações da aplicação usando Pydantic Settings
"""
from typing import Optional, List

from pydantic import model_validator
from pydantic_settings import BaseSettings


def _csv_to_list(value: Optional[str]) -> List[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


class Settings(BaseSettings):
    """Configurações da aplicação"""

    # Application
    APP_NAME: str = "Facebook Ads AI Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # Facebook (optional for testing)
    FACEBOOK_APP_ID: Optional[str] = "your_facebook_app_id"
    FACEBOOK_APP_SECRET: Optional[str] = "your_facebook_app_secret"
    FACEBOOK_ACCESS_TOKEN: Optional[str] = "your_facebook_access_token"
    FACEBOOK_AD_ACCOUNT_ID: Optional[str] = "act_your_account_id"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/facebook_ads_ai"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    # n8n
    N8N_WEBHOOK_URL: str = "http://localhost:5678/webhook"
    N8N_API_URL: str = "http://localhost:5678/api/v1"
    N8N_API_KEY: Optional[str] = None
    N8N_BASIC_AUTH_USER: str = "admin"
    N8N_BASIC_AUTH_PASSWORD: str = "admin"

    # External Integrations
    SLACK_WEBHOOK_URL: Optional[str] = None
    SENDGRID_API_KEY: Optional[str] = None
    GOOGLE_CALENDAR_CREDENTIALS_PATH: Optional[str] = None
    
    # Notion Integration (P0 #4)
    NOTION_API_TOKEN: Optional[str] = None
    NOTION_DATABASE_ID: Optional[str] = None

    # AI/NLP
    OPENAI_API_KEY: Optional[str] = None

    # Security
    SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ANALYTICS_API_KEY: str = "change-me-in-production"
    JWT_EXPIRATION_MINUTES: int = 1440
    ALLOWED_ORIGINS: Optional[str] = None
    TRUSTED_HOSTS: Optional[str] = None

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "/app/logs/app.log"

    @model_validator(mode="after")
    def validate_production_secrets(self) -> "Settings":
        """Block startup when running in production with insecure defaults"""
        if self.ENVIRONMENT.lower() == "production":
            insecure_defaults = {
                "SECRET_KEY": "change-me-in-production",
                "ANALYTICS_API_KEY": "change-me-in-production",
                "N8N_BASIC_AUTH_PASSWORD": "admin",
            }
            for field_name, default_value in insecure_defaults.items():
                current_value = getattr(self, field_name)
                if current_value == default_value or not current_value:
                    raise ValueError(
                        f"{field_name} must be set with a secure value in production environment"
                    )

            if not self.get_allowed_origins():
                raise ValueError(
                    "ALLOWED_ORIGINS must define at least one origin in production"
                )

        return self

    def get_allowed_origins(self) -> List[str]:
        explicit = _csv_to_list(self.ALLOWED_ORIGINS)
        if explicit:
            return explicit

        if self.ENVIRONMENT == "development":
            return [
                "http://localhost:3000",
                "http://localhost:8000",
                "http://127.0.0.1:3000",
                "http://127.0.0.1:8000",
            ]

        if self.ENVIRONMENT == "production":
            return [
                "https://fbads.macspark.dev",
                "https://api.fbads.macspark.dev",
            ]

        return []

    def get_trusted_hosts(self) -> List[str]:
        explicit = _csv_to_list(self.TRUSTED_HOSTS)
        if explicit:
            return explicit

        if self.ENVIRONMENT == "production":
            return ["fbads.macspark.dev", "api.fbads.macspark.dev", "*.macspark.dev"]

        return ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env


# Singleton instance
settings = Settings()
