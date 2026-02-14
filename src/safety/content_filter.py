"""Content safety and filtering for responsible AI."""

from typing import Any, Dict, List, Tuple
from enum import Enum
import re

from ..tracing.tracer import tracer


class SafetyLevel(Enum):
    """Safety assessment levels."""
    SAFE = "safe"
    LOW_RISK = "low_risk"
    MEDIUM_RISK = "medium_risk"
    HIGH_RISK = "high_risk"
    BLOCKED = "blocked"


class ContentCategory(Enum):
    """Content safety categories aligned with Microsoft standards."""
    HATE_SPEECH = "hate_speech"
    VIOLENCE = "violence"
    SEXUAL_CONTENT = "sexual_content"
    SELF_HARM = "self_harm"
    HARASSMENT = "harassment"
    PROFANITY = "profanity"
    JAILBREAK_ATTEMPT = "jailbreak_attempt"
    PROMPT_INJECTION = "prompt_injection"


class ContentFilter:
    """Responsible AI content safety filter with tracing instrumentation."""

    def __init__(self, strict_mode: bool = True):
        """Initialize the content filter.

        Args:
            strict_mode: When True, block medium-risk content in addition to
                high-risk detections.
        """

        self.strict_mode = strict_mode

        # Pattern detection for common jailbreak or injection attempts.
        # Extend with Microsoft Content Safety or custom classifiers as needed.
        self._blocked_patterns = {
            ContentCategory.JAILBREAK_ATTEMPT: [
                r"ignore\s+(previous|all)\s+instructions",
                r"disregard\s+(your|the)\s+(guidelines|rules|instructions)",
                r"pretend\s+you\s+are\s+(not|no\s+longer)",
                r"you\s+are\s+now\s+in\s+developer\s+mode",
            ],
            ContentCategory.PROMPT_INJECTION: [
                r"<\s*script\s*>",
                r"system\s*:\s*new\s+role",
                r"ignore\s+safety\s+guidelines",
            ],
        }

    def check_input(
        self, text: str
    ) -> Tuple[SafetyLevel, List[ContentCategory], str]:
        """Evaluate user input for safety concerns."""

        attributes = {
            "strict_mode": str(self.strict_mode),
            "input_length": len(text),
        }

        with tracer.trace_operation(
            "content_filter.check_input",
            attributes,
        ) as span:
            normalized = self.sanitize_input(text)
            detections: List[ContentCategory] = []

            for category, patterns in self._blocked_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, normalized, re.IGNORECASE):
                        detections.append(category)

            if not detections:
                span.set_attribute("safety_level", SafetyLevel.SAFE.value)
                return SafetyLevel.SAFE, [], "No safety concerns detected"

            high_risk = {
                ContentCategory.JAILBREAK_ATTEMPT,
                ContentCategory.PROMPT_INJECTION,
            }

            detected_values = ", ".join(cat.value for cat in detections)
            span.set_attribute("detected_categories", detected_values)

            if any(cat in high_risk for cat in detections):
                span.set_attribute("safety_level", SafetyLevel.BLOCKED.value)
                explanation = (
                    "Blocked due to detected categories: "
                    f"{detected_values}"
                )
                return SafetyLevel.BLOCKED, detections, explanation

            span.set_attribute("safety_level", SafetyLevel.MEDIUM_RISK.value)
            explanation = (
                "Medium risk content detected: "
                f"{detected_values}"
            )
            return SafetyLevel.MEDIUM_RISK, detections, explanation

    def check_output(self, text: str) -> Tuple[SafetyLevel, Dict[str, Any]]:
        """Evaluate model responses for safety and completeness."""

        metadata = {
            "length": len(text),
            "contains_urls": bool(re.search(r"https?://", text)),
            "contains_code": bool(re.search(r"```", text)),
        }

        with tracer.trace_operation(
            "content_filter.check_output",
            {"response_length": len(text)},
        ) as span:
            span.set_attribute(
                "contains_urls",
                str(metadata["contains_urls"]),
            )
            span.set_attribute(
                "contains_code",
                str(metadata["contains_code"]),
            )

            if len(text) < 10:
                span.set_attribute("safety_level", SafetyLevel.LOW_RISK.value)
                rationale = "Very short response"
                short_metadata = {**metadata, "reason": rationale}
                return SafetyLevel.LOW_RISK, short_metadata

            span.set_attribute("safety_level", SafetyLevel.SAFE.value)
            return SafetyLevel.SAFE, metadata

    def sanitize_input(self, text: str, max_length: int = 10000) -> str:
        """Trim control characters and enforce maximum length constraints."""

        with tracer.trace_operation(
            "content_filter.sanitize_input",
            {"input_length": len(text), "max_length": max_length},
        ):
            truncated = text[:max_length]
            cleaned = re.sub(
                r"[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]",
                "",
                truncated,
            )
            normalized = " ".join(cleaned.split())
            return normalized

    def filter_sensitive_data(self, text: str) -> Tuple[str, List[str]]:
        """Mask sensitive data before logging or downstream processing."""

        detections: List[str] = []
        with tracer.trace_operation(
            "content_filter.filter_sensitive_data",
            {"input_length": len(text)},
        ) as span:
            filtered_text = text

            email_pattern = (
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
            )
            if re.search(email_pattern, filtered_text):
                filtered_text = re.sub(
                    email_pattern,
                    "[EMAIL_REDACTED]",
                    filtered_text,
                )
                detections.append("email")

            phone_pattern = r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"
            if re.search(phone_pattern, filtered_text):
                filtered_text = re.sub(
                    phone_pattern,
                    "[PHONE_REDACTED]",
                    filtered_text,
                )
                detections.append("phone")

            cc_pattern = r"\b(?:\d{4}[-\s]?){3}\d{4}\b"
            if re.search(cc_pattern, filtered_text):
                filtered_text = re.sub(
                    cc_pattern,
                    "[CC_REDACTED]",
                    filtered_text,
                )
                detections.append("credit_card")

            api_key_pattern = r"\b[A-Za-z0-9_-]{32,}\b"
            token_pattern = (
                r'(api[_-]?key|token|secret)(["\s:=]+)'
                + api_key_pattern
            )
            if re.search(token_pattern, filtered_text, re.IGNORECASE):
                filtered_text = re.sub(
                    token_pattern,
                    r"\1\2[KEY_REDACTED]",
                    filtered_text,
                    flags=re.IGNORECASE,
                )
                detections.append("api_key")

            if detections:
                span.set_attribute("sensitive_types", ", ".join(detections))

            return filtered_text, detections
