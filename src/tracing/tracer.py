"""Distributed tracing for AI agent operations."""

from contextlib import contextmanager
from typing import Any, Dict, Optional
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.trace import Status, StatusCode

from ..config import settings


class AgentTracer:
    """Tracer for AI agent operations."""
    
    def __init__(self, service_name: str = "eden-agent"):
        """Initialize the tracer."""
        if settings.enable_tracing:
            resource = Resource.create({"service.name": service_name})
            provider = TracerProvider(resource=resource)
            
            if settings.trace_exporter == "console":
                exporter = ConsoleSpanExporter()
                provider.add_span_processor(BatchSpanProcessor(exporter))
            
            trace.set_tracer_provider(provider)
        
        self.tracer = trace.get_tracer(__name__)
    
    @contextmanager
    def trace_operation(
        self,
        operation_name: str,
        attributes: Optional[Dict[str, Any]] = None
    ):
        """Trace an operation with optional attributes."""
        with self.tracer.start_as_current_span(operation_name) as span:
            if attributes:
                for key, value in attributes.items():
                    span.set_attribute(key, str(value))
            
            try:
                yield span
            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise


# Global tracer instance
tracer = AgentTracer()
