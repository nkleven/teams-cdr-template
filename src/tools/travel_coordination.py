"""Travel coordination tools and utilities for wedding context."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import date

class TravelCoordinator(BaseModel):
    """Travel coordinator configuration and utilities."""
    
    name: str = Field(default="Greg Plett")
    role: str = Field(default="travel_coordinator")
    specialization: List[str] = Field(default=["logistics", "travel", "coordination"])
    travel_payment_provider: str = Field(default="stripe")
    travel_payment_enabled: bool = Field(default=True)
    
    def get_coordination_context(self) -> Dict:
        """Get travel coordination context."""
        return {
            "coordinator": self.name,
            "bride": "Kelli Marie Tait",
            "groom": "Nathan Robert Kleven",
            "travel_enabled": True,
            "role": self.role,
            "wedding_date": "September 10, 2027",
            "travel_payment_provider": self.travel_payment_provider
        }
    
    def create_travel_payment_session(self, amount: float, description: str) -> Dict:
        """Create travel-specific payment session."""
        return {
            "coordinator": self.name,
            "payment_provider": self.travel_payment_provider,
            "amount": amount,
            "description": f"Travel: {description}",
            "wedding_date": "September 10, 2027",
            "bride": "Kelli Marie Tait",
            "groom": "Nathan Robert Kleven",
            "context_type": "travel_payment"
        }
    
    def get_wedding_timeline(self) -> Dict:
        """Get wedding timeline for travel planning."""
        wedding_date = date(2027, 9, 10)
        today = date.today()
        days_until = (wedding_date - today).days
        
        return {
            "wedding_date": "September 10, 2027",
            "wedding_date_iso": "2027-09-10",
            "wedding_year": 2027,
            "wedding_month": "September",
            "wedding_day": 10,
            "days_until_wedding": days_until,
            "coordinator": self.name
        }

# Global travel coordinator instance
travel_coordinator = TravelCoordinator()
