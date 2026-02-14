"""Data validation tool for AI agent."""

import re
from typing import Any, Dict
from .base import BaseTool, ToolDefinition


class DataValidationTool(BaseTool):
    """Tool for validating various types of data."""
    
    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="data_validation",
            description="Validate data like emails, URLs, phone numbers, and more",
            input_schema={
                "type": "object",
                "properties": {
                    "validation_type": {
                        "type": "string",
                        "enum": ["email", "url", "phone", "date", "json", "credit_card"],
                        "description": "Type of validation to perform"
                    },
                    "data": {
                        "type": "string",
                        "description": "The data to validate"
                    }
                },
                "required": ["validation_type", "data"]
            }
        )
    
    async def execute(self, validation_type: str, data: str) -> Dict[str, Any]:
        """Execute data validation.
        
        Args:
            validation_type: Type of validation
            data: Data to validate
            
        Returns:
            Validation result with details
        """
        validators = {
            "email": self._validate_email,
            "url": self._validate_url,
            "phone": self._validate_phone,
            "date": self._validate_date,
            "json": self._validate_json,
            "credit_card": self._validate_credit_card
        }
        
        validator = validators.get(validation_type)
        if not validator:
            return {
                "valid": False,
                "error": f"Unknown validation type: {validation_type}"
            }
        
        return validator(data)
    
    def _validate_email(self, email: str) -> Dict[str, Any]:
        """Validate email address."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        is_valid = bool(re.match(pattern, email))
        
        return {
            "valid": is_valid,
            "type": "email",
            "data": email,
            "message": "Valid email address" if is_valid else "Invalid email format"
        }
    
    def _validate_url(self, url: str) -> Dict[str, Any]:
        """Validate URL."""
        pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
        is_valid = bool(re.match(pattern, url))
        
        return {
            "valid": is_valid,
            "type": "url",
            "data": url,
            "message": "Valid URL" if is_valid else "Invalid URL format"
        }
    
    def _validate_phone(self, phone: str) -> Dict[str, Any]:
        """Validate phone number (US format)."""
        # Remove common formatting characters
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        pattern = r'^\+?1?[2-9]\d{9}$'
        is_valid = bool(re.match(pattern, cleaned))
        
        return {
            "valid": is_valid,
            "type": "phone",
            "data": phone,
            "cleaned": cleaned if is_valid else None,
            "message": "Valid phone number" if is_valid else "Invalid phone format"
        }
    
    def _validate_date(self, date: str) -> Dict[str, Any]:
        """Validate date format (YYYY-MM-DD)."""
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        is_valid = bool(re.match(pattern, date))
        
        if is_valid:
            try:
                year, month, day = map(int, date.split('-'))
                # Basic validation
                is_valid = (1 <= month <= 12) and (1 <= day <= 31) and (1900 <= year <= 2100)
            except ValueError:
                is_valid = False
        
        return {
            "valid": is_valid,
            "type": "date",
            "data": date,
            "message": "Valid date format" if is_valid else "Invalid date (use YYYY-MM-DD)"
        }
    
    def _validate_json(self, json_str: str) -> Dict[str, Any]:
        """Validate JSON string."""
        import json
        
        try:
            parsed = json.loads(json_str)
            return {
                "valid": True,
                "type": "json",
                "message": "Valid JSON",
                "parsed_type": type(parsed).__name__
            }
        except json.JSONDecodeError as e:
            return {
                "valid": False,
                "type": "json",
                "message": f"Invalid JSON: {str(e)}"
            }
    
    def _validate_credit_card(self, card_number: str) -> Dict[str, Any]:
        """Validate credit card using Luhn algorithm."""
        # Remove spaces and dashes
        cleaned = re.sub(r'[\s\-]', '', card_number)
        
        if not cleaned.isdigit() or len(cleaned) < 13 or len(cleaned) > 19:
            return {
                "valid": False,
                "type": "credit_card",
                "message": "Invalid card number format"
            }
        
        # Luhn algorithm
        def luhn_checksum(card: str) -> bool:
            digits = [int(d) for d in card]
            checksum = 0
            for i, digit in enumerate(reversed(digits)):
                if i % 2 == 1:
                    digit *= 2
                    if digit > 9:
                        digit -= 9
                checksum += digit
            return checksum % 10 == 0
        
        is_valid = luhn_checksum(cleaned)
        
        # Identify card type
        card_type = "Unknown"
        if cleaned.startswith('4'):
            card_type = "Visa"
        elif cleaned.startswith(('51', '52', '53', '54', '55')):
            card_type = "Mastercard"
        elif cleaned.startswith(('34', '37')):
            card_type = "American Express"
        
        return {
            "valid": is_valid,
            "type": "credit_card",
            "card_type": card_type,
            "message": f"Valid {card_type} card" if is_valid else "Invalid card number"
        }
