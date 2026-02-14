"""Wedding countdown and date utilities."""

from datetime import date, datetime
from typing import Dict

class WeddingCountdown:
    """Wedding countdown and date management."""
    
    WEDDING_DATE = date(2027, 9, 10)
    WEDDING_DATE_FORMATTED = "September 10, 2027"
    
    @classmethod
    def days_until_wedding(cls) -> int:
        """Calculate days until wedding."""
        today = date.today()
        return (cls.WEDDING_DATE - today).days
    
    @classmethod
    def months_until_wedding(cls) -> float:
        """Calculate months until wedding (approximate)."""
        return cls.days_until_wedding() / 30.44
    
    @classmethod
    def years_until_wedding(cls) -> float:
        """Calculate years until wedding."""
        return cls.days_until_wedding() / 365.25
    
    @classmethod
    def get_countdown_context(cls) -> Dict:
        """Get complete countdown context."""
        days = cls.days_until_wedding()
        
        return {
            "wedding_date": "2027-09-10",
            "wedding_date_formatted": cls.WEDDING_DATE_FORMATTED,
            "days_until": days,
            "months_until": round(cls.months_until_wedding(), 1),
            "years_until": round(cls.years_until_wedding(), 2),
            "countdown_active": days > 0,
            "bride": "Kelli Marie Tait",
            "groom": "Nathan Robert Kleven",
            "travel_coordinator": "Greg Plett",
            "payment_provider": "stripe"
        }

# Global countdown instance
wedding_countdown = WeddingCountdown()
