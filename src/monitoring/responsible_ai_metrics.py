"""Responsible AI metrics tracking and monitoring."""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timezone
from collections import defaultdict
import json

from ..tracing.tracer import tracer


@dataclass
class InteractionMetrics:
    """Metrics for a single interaction."""
    timestamp: datetime
    user_input_length: int
    response_length: int
    response_time_ms: float
    safety_level: str
    tokens_used: Optional[int] = None
    tool_calls: List[str] = field(default_factory=list)
    error_occurred: bool = False
    error_type: Optional[str] = None
    sensitive_data_detected: List[str] = field(default_factory=list)


@dataclass
class ResponsibleAIMetrics:
    """
    Comprehensive metrics for responsible AI monitoring.
    Tracks fairness, reliability, safety, and transparency metrics.
    """
    
    def __init__(self):
        """Initialize metrics tracker."""
        self.interactions: List[InteractionMetrics] = []
        self.safety_blocks: int = 0
        self.total_requests: int = 0
        self.failed_requests: int = 0
        self.tool_usage_counts: Dict[str, int] = defaultdict(int)
        self.error_types: Dict[str, int] = defaultdict(int)
        self.sensitive_data_detections: Dict[str, int] = defaultdict(int)
        
    def record_interaction(self, metrics: InteractionMetrics):
        """Record metrics from an interaction."""
        attributes = {
            "safety_level": metrics.safety_level,
            "response_time_ms": metrics.response_time_ms,
            "has_error": str(metrics.error_occurred),
            "tool_calls": len(metrics.tool_calls),
        }

        with tracer.trace_operation(
            "metrics.record_interaction",
            attributes,
        ) as span:
            self.interactions.append(metrics)
            self.total_requests += 1

            if metrics.error_occurred:
                self.failed_requests += 1
                if metrics.error_type:
                    self.error_types[metrics.error_type] += 1
                    span.set_attribute("error_type", metrics.error_type)

            if metrics.safety_level == "blocked":
                self.safety_blocks += 1

            if metrics.tool_calls:
                tool_list = ", ".join(metrics.tool_calls)
                span.set_attribute("tool_calls", tool_list)
                for tool in metrics.tool_calls:
                    self.tool_usage_counts[tool] += 1

            for data_type in metrics.sensitive_data_detected:
                self.sensitive_data_detections[data_type] += 1

            if metrics.sensitive_data_detected:
                detected = ", ".join(metrics.sensitive_data_detected)
                span.set_attribute("sensitive_data", detected)
    
    def get_reliability_metrics(self) -> Dict[str, Any]:
        """Calculate reliability metrics."""
        with tracer.trace_operation("metrics.get_reliability", None) as span:
            if self.total_requests == 0:
                span.set_attribute("total_requests", 0)
                return {
                    "success_rate": 0.0,
                    "failure_rate": 0.0,
                    "total_requests": 0,
                }

            success_rate = (
                self.total_requests - self.failed_requests
            ) / self.total_requests

            response_times = [
                item.response_time_ms for item in self.interactions
            ]
            if response_times:
                avg_response_time = sum(response_times) / len(response_times)
            else:
                avg_response_time = 0.0

            span.set_attribute("success_rate", round(success_rate, 4))
            span.set_attribute("failed_requests", self.failed_requests)

            return {
                "success_rate": round(success_rate, 4),
                "failure_rate": round(1 - success_rate, 4),
                "total_requests": self.total_requests,
                "failed_requests": self.failed_requests,
                "avg_response_time_ms": round(avg_response_time, 2),
                "error_breakdown": dict(self.error_types),
            }
    
    def get_safety_metrics(self) -> Dict[str, Any]:
        """Calculate safety metrics."""
        with tracer.trace_operation("metrics.get_safety", None) as span:
            safety_level_counts: Dict[str, int] = defaultdict(int)
            for interaction in self.interactions:
                safety_level_counts[interaction.safety_level] += 1

            block_rate = 0.0
            if self.total_requests:
                block_rate = self.safety_blocks / self.total_requests

            span.set_attribute("total_blocks", self.safety_blocks)
            span.set_attribute("block_rate", round(block_rate, 4))

            return {
                "total_blocks": self.safety_blocks,
                "block_rate": round(block_rate, 4),
                "safety_level_distribution": dict(safety_level_counts),
                "sensitive_data_detections": dict(
                    self.sensitive_data_detections
                ),
            }

    def get_transparency_metrics(self) -> Dict[str, Any]:
        """Calculate transparency and explainability metrics."""
        with tracer.trace_operation("metrics.get_transparency", None) as span:
            total_tool_calls = sum(self.tool_usage_counts.values())
            denominator = self.total_requests or 1
            avg_tools = total_tool_calls / denominator

            span.set_attribute("total_tool_calls", total_tool_calls)
            span.set_attribute("avg_tools", round(avg_tools, 2))

            return {
                "tool_usage": dict(self.tool_usage_counts),
                "total_tool_calls": total_tool_calls,
                "avg_tools_per_request": round(avg_tools, 2),
            }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Calculate performance metrics."""
        with tracer.trace_operation("metrics.get_performance", None) as span:
            if not self.interactions:
                span.set_attribute("interaction_count", 0)
                return {
                    "avg_input_length": 0,
                    "avg_output_length": 0,
                    "avg_tokens_used": 0,
                }

            interaction_count = len(self.interactions)
            total_input = sum(
                item.user_input_length for item in self.interactions
            )
            total_output = sum(
                item.response_length for item in self.interactions
            )

            token_counts = [
                item.tokens_used
                for item in self.interactions
                if item.tokens_used is not None
            ]
            avg_tokens = 0.0
            if token_counts:
                avg_tokens = sum(token_counts) / len(token_counts)

            span.set_attribute("interaction_count", interaction_count)

            return {
                "avg_input_length": round(total_input / interaction_count, 2),
                "avg_output_length": round(
                    total_output / interaction_count,
                    2,
                ),
                "avg_tokens_used": round(avg_tokens, 2),
            }
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive responsible AI metrics report."""
        with tracer.trace_operation("metrics.generate_report", None):
            start_timestamp = None
            end_timestamp = None
            if self.interactions:
                start_timestamp = self.interactions[0].timestamp.isoformat()
                end_timestamp = self.interactions[-1].timestamp.isoformat()

            return {
                "report_generated_at": datetime.now(timezone.utc).isoformat(),
                "reliability": self.get_reliability_metrics(),
                "safety": self.get_safety_metrics(),
                "transparency": self.get_transparency_metrics(),
                "performance": self.get_performance_metrics(),
                "summary": {
                    "total_interactions": len(self.interactions),
                    "monitoring_period": {
                        "start": start_timestamp,
                        "end": end_timestamp,
                    },
                },
            }
    
    def export_to_json(self, filepath: str):
        """Export metrics report to JSON file."""
        with tracer.trace_operation(
            "metrics.export_to_json",
            {"filepath": filepath},
        ):
            report = self.generate_report()
            with open(filepath, "w", encoding="utf-8") as handle:
                json.dump(report, handle, indent=2)
    
    def reset(self):
        """Reset all metrics."""
        with tracer.trace_operation("metrics.reset", None):
            self.interactions.clear()
            self.safety_blocks = 0
            self.total_requests = 0
            self.failed_requests = 0
            self.tool_usage_counts.clear()
            self.error_types.clear()
            self.sensitive_data_detections.clear()


# Global metrics instance
metrics_tracker = ResponsibleAIMetrics()
