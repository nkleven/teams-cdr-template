"""Health check and system status monitoring."""

import logging
import sys
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from dataclasses import dataclass, asdict

logger = logging.getLogger("eden_agent.health")


@dataclass
class HealthStatus:
    """Health check status information."""
    status: str  # "healthy", "degraded", "unhealthy"
    timestamp: str
    version: str
    python_version: str
    checks: Dict[str, Any]
    errors: list[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class HealthChecker:
    """System health checker."""
    
    def __init__(self, version: str = "0.1.0-beta.1"):
        """Initialize health checker."""
        self.version = version
        self.startup_time = datetime.now(timezone.utc)
        
    def check_configuration(self) -> tuple[bool, Optional[str]]:
        """Check if configuration is valid."""
        try:
            from .config import settings
            
            # Check API key is set
            if not settings.anthropic_api_key:
                return False, "ANTHROPIC_API_KEY not configured"
            
            if settings.anthropic_api_key == "your_anthropic_api_key_here":
                return False, "ANTHROPIC_API_KEY still set to placeholder"
            
            # Check model name is set
            if not settings.model_name:
                return False, "MODEL_NAME not configured"
            
            return True, None
            
        except Exception as e:
            return False, f"Configuration error: {str(e)}"
    
    def check_dependencies(self) -> tuple[bool, Optional[str]]:
        """Check if required dependencies are available."""
        try:
            import anthropic  # noqa: F401
            import opentelemetry  # noqa: F401
            import pydantic  # noqa: F401
            return True, None
        except ImportError as e:
            return False, f"Missing dependency: {str(e)}"
    
    def check_tracing(self) -> tuple[bool, Optional[str]]:
        """Check if tracing is configured properly."""
        try:
            from .config import settings
            from .tracing.tracer import tracer
            
            if not settings.enable_tracing:
                return True, "Tracing disabled"
            
            if tracer is None:
                return False, "Tracer not initialized"
            
            return True, None
            
        except Exception as e:
            return False, f"Tracing error: {str(e)}"
    
    def check_tools(self) -> tuple[bool, Optional[str]]:
        """Check if tools are available."""
        try:
            from .tools.calculator import CalculatorTool
            
            # Try to instantiate
            _ = CalculatorTool()
            return True, None
            
        except Exception as e:
            return False, f"Tool initialization error: {str(e)}"
    
    def check_safety(self) -> tuple[bool, Optional[str]]:
        """Check if safety filters are available."""
        try:
            from .safety.content_filter import ContentFilter
            
            # Try to instantiate
            filter_instance = ContentFilter()
            
            # Quick sanity test
            level, _, _ = filter_instance.check_input("test")
            if level is None:
                return False, "Safety filter returned None"
            
            return True, None
            
        except Exception as e:
            return False, f"Safety filter error: {str(e)}"
    
    def check_monitoring(self) -> tuple[bool, Optional[str]]:
        """Check if monitoring is available."""
        try:
            from .monitoring.responsible_ai_metrics import (
                ResponsibleAIMetrics
            )
            
            # Try to instantiate
            _ = ResponsibleAIMetrics()
            return True, None
            
        except Exception as e:
            return False, f"Monitoring error: {str(e)}"
    
    def get_uptime(self) -> float:
        """Get system uptime in seconds."""
        now = datetime.now(timezone.utc)
        delta = now - self.startup_time
        return delta.total_seconds()
    
    def perform_health_check(self) -> HealthStatus:
        """Perform comprehensive health check."""
        logger.info("Performing health check...")
        
        checks = {}
        errors = []
        
        # Configuration check
        config_ok, config_error = self.check_configuration()
        checks["configuration"] = {
            "status": "pass" if config_ok else "fail",
            "message": config_error
        }
        if not config_ok and config_error:
            errors.append(config_error)

        # Dependencies check
        deps_ok, deps_error = self.check_dependencies()
        checks["dependencies"] = {
            "status": "pass" if deps_ok else "fail",
            "message": deps_error
        }
        if not deps_ok and deps_error:
            errors.append(deps_error)
        
        # Tracing check
        trace_ok, trace_error = self.check_tracing()
        checks["tracing"] = {
            "status": "pass" if trace_ok else "fail",
            "message": trace_error
        }
        if not trace_ok and trace_error:
            errors.append(trace_error)
        
        # Tools check
        tools_ok, tools_error = self.check_tools()
        checks["tools"] = {
            "status": "pass" if tools_ok else "fail",
            "message": tools_error
        }
        if not tools_ok and tools_error:
            errors.append(tools_error)
        
        # Safety check
        safety_ok, safety_error = self.check_safety()
        checks["safety"] = {
            "status": "pass" if safety_ok else "fail",
            "message": safety_error
        }
        if not safety_ok and safety_error:
            errors.append(safety_error)
        
        # Monitoring check
        monitor_ok, monitor_error = self.check_monitoring()
        checks["monitoring"] = {
            "status": "pass" if monitor_ok else "fail",
            "message": monitor_error
        }
        if not monitor_ok and monitor_error:
            errors.append(monitor_error)
        
        # System info
        checks["system"] = {
            "uptime_seconds": round(self.get_uptime(), 2),
            "python_version": sys.version,
        }
        
        # Determine overall status
        critical_checks = [config_ok, deps_ok, tools_ok, safety_ok]
        if all(critical_checks):
            overall_status = "healthy"
        elif any(critical_checks):
            overall_status = "degraded"
        else:
            overall_status = "unhealthy"
        
        status = HealthStatus(
            status=overall_status,
            timestamp=datetime.now(timezone.utc).isoformat(),
            version=self.version,
            python_version=sys.version.split()[0],
            checks=checks,
            errors=errors
        )
        
        logger.info("Health check complete: %s", overall_status)
        return status


# Global health checker instance
health_checker = HealthChecker()
