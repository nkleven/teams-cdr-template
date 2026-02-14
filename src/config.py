"""Configuration management for the Eden AI agent and wedding context."""

import logging
from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger("eden_agent.config")


class Settings(BaseSettings):
    """Application settings with validation.

    Combines AI agent configuration (API keys, model settings, rate limiting,
    retry logic) with wedding/relationship context fields used by the dashboard.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- AI / API Configuration ---
    anthropic_api_key: str = Field(
        default="",
        description="Anthropic API key (set via ANTHROPIC_API_KEY env var)",
    )

    # Model Configuration
    model_name: str = Field(
        default="claude-sonnet-4-5",
        description="Model to use",
    )
    max_tokens: int = Field(
        default=4096,
        description="Maximum tokens to generate",
        ge=1,
        le=200000,
    )
    temperature: float = Field(
        default=0.7,
        description="Temperature for generation",
        ge=0.0,
        le=2.0,
    )

    # Tracing Configuration
    enable_tracing: bool = Field(
        default=True,
        description="Enable distributed tracing",
    )
    trace_exporter: str = Field(
        default="console",
        description="Trace exporter type",
    )

    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    enable_rich_logging: bool = Field(
        default=True, description="Use rich console logging"
    )

    # Rate Limiting Configuration
    rate_limit_enabled: bool = Field(
        default=True, description="Enable API rate limiting"
    )
    rate_limit_max_calls: int = Field(
        default=50,
        description="Maximum API calls per time window",
        ge=1,
    )
    rate_limit_time_window: float = Field(
        default=60.0,
        description="Rate limit time window in seconds",
        ge=1.0,
    )

    # Retry Configuration
    retry_enabled: bool = Field(
        default=True, description="Enable retry logic for API failures"
    )
    retry_max_attempts: int = Field(
        default=3, description="Maximum retry attempts", ge=1, le=10
    )
    retry_base_delay: float = Field(
        default=1.0, description="Base delay for retries in seconds", ge=0.1
    )
    retry_max_delay: float = Field(
        default=60.0, description="Maximum retry delay in seconds", ge=1.0
    )

    # --- Wedding / Relationship Context ---
    debug: bool = Field(default=False, description="Debug mode")

    bride_name: str = Field(
        default="Kelli Marie Tait",
        description="Bride's full name for wedding context",
    )
    groom_name: str = Field(
        default="Nathan Robert Kleven",
        description="Groom's full name for wedding context",
    )
    wedding_context_enabled: bool = Field(
        default=True,
        description="Enable wedding/relationship context features",
    )
    relationship_type: str = Field(
        default="wedding_planning",
        description="Type of relationship context",
    )

    # Travel Coordination Context
    travel_coordinator_name: str = Field(
        default="Greg Plett",
        description="Travel coordinator's full name",
    )
    travel_coordination_enabled: bool = Field(
        default=True,
        description="Enable travel coordination features",
    )
    travel_context_role: str = Field(
        default="travel_coordinator",
        description="Role designation for travel coordination",
    )

    # Payment Context
    payment_provider: str = Field(
        default="stripe", description="Payment provider name"
    )
    payment_context_enabled: bool = Field(
        default=True, description="Enable payment processing features"
    )
    stripe_integration: bool = Field(
        default=True, description="Enable Stripe payment integration"
    )
    payment_processor: str = Field(
        default="stripe", description="Payment processor designation"
    )

    # Wedding Date Context
    wedding_date: str = Field(
        default="2027-09-10", description="Wedding date in YYYY-MM-DD format"
    )
    wedding_date_formatted: str = Field(
        default="September 10, 2027",
        description="Wedding date in readable format",
    )
    wedding_year: int = Field(default=2027, description="Wedding year")
    wedding_month: str = Field(
        default="September", description="Wedding month name"
    )
    wedding_day: int = Field(default=10, description="Wedding day of month")

    # Travel Payment Integration
    travel_payment_provider: str = Field(
        default="stripe", description="Travel payment provider"
    )
    travel_payment_enabled: bool = Field(
        default=True, description="Enable travel payment processing"
    )
    travel_stripe_integration: bool = Field(
        default=True,
        description="Enable Stripe integration for travel payments",
    )
    travel_payment_processor: str = Field(
        default="stripe", description="Travel payment processor designation"
    )

    # --- Validators ---
    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(
                f"Invalid log level: {v}. Must be one of {valid_levels}"
            )
        return v_upper

    @field_validator("trace_exporter")
    @classmethod
    def validate_trace_exporter(cls, v: str) -> str:
        """Validate trace exporter."""
        valid_exporters = ["console", "jaeger", "zipkin", "otlp"]
        if v.lower() not in valid_exporters:
            logger.warning(
                "Unknown trace exporter: %s. Valid options: %s",
                v,
                valid_exporters,
            )
        return v.lower()


# ---------------------------------------------------------------------------
# Global instances
# ---------------------------------------------------------------------------

def load_settings() -> Settings:
    """Load and validate settings with helpful error messages."""
    try:
        config = Settings()
        logger.info("✓ Configuration loaded successfully")
        return config
    except Exception as e:
        logger.error("✗ Configuration error: %s", e)
        raise


settings = load_settings()

# Backwards-compatible alias used by dashboard / wedding modules
# (`from ..config import get_config`)
_config: Optional[Settings] = None


def get_config() -> Settings:
    """Get global configuration instance (alias for settings)."""
    global _config
    if _config is None:
        _config = settings
    return _config
