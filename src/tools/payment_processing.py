"""Payment processing tools and utilities for wedding context."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class PaymentProcessor(BaseModel):
    """Payment processor configuration and utilities."""
    
    provider: str = Field(default="stripe")
    processor_type: str = Field(default="stripe")
    integration_enabled: bool = Field(default=True)
    travel_payments_enabled: bool = Field(default=True)
    
    def get_payment_context(self) -> Dict:
        """Get payment processing context."""
        return {
            "provider": self.provider,
            "processor": self.processor_type,
            "enabled": self.integration_enabled,
            "stripe_integration": True,
            "travel_payments": self.travel_payments_enabled,
            "wedding_context": True
        }
    
    def create_payment_session(self, amount: float, currency: str = "USD") -> Dict:
        """Create a payment session configuration."""
        return {
            "provider": self.provider,
            "amount": amount,
            "currency": currency,
            "wedding_context": True,
            "bride": "Kelli Marie Tait",
            "groom": "Nathan Robert Kleven",
            "travel_coordinator": "Greg Plett",
            "wedding_date": "September 10, 2027",
            "status": "initialized"
        }
    
    def get_wedding_payment_context(self) -> Dict:
        """Get wedding payment context with date information."""
        return {
            "wedding_date": "September 10, 2027",
            "wedding_date_iso": "2027-09-10",
            "wedding_year": 2027,
            "payment_provider": self.provider,
            "wedding_context": True,
            "travel_payments_enabled": self.travel_payments_enabled,
            "payment_timeline_available": True
        }

# Global payment processor instance
payment_processor = PaymentProcessor()
