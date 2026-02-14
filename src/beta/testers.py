"""Beta registry for wedding team management."""

from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

class BetaRole(Enum):
    """Beta roles for wedding team context."""
    BRIDGE = "bridge"                      # Nathan - Project lead/groom
    WITNESS = "witness"                    # Kelli - Beta tester/bride  
    BRIDE = "bride"                        # Kelli - Bride role
    GROOM = "groom"                        # Nathan - Groom role
    TRAVEL_COORDINATOR = "travel_coordinator"  # Greg - Travel coordination
    PAYMENT_PROCESSOR = "payment_processor"    # Stripe - Payment processing
    DEVELOPER = "developer"
    TESTER = "tester"

@dataclass
class BetaUser:
    """Beta user representation."""
    name: str
    email: str
    role: BetaRole
    metadata: Dict

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "email": self.email,
            "role": self.role.value,
            "metadata": self.metadata,
        }

class BetaRegistry:
    """Beta user registry."""
    
    def __init__(self):
        self.users: Dict[str, BetaUser] = {}
    
    def register(self, name: str, email: str, role: BetaRole, metadata: Dict) -> BetaUser:
        """Register a beta user."""
        user = BetaUser(name=name, email=email, role=role, metadata=metadata)
        self.users[name.lower().replace(" ", "_")] = user
        return user
    
    def get_user(self, name: str) -> Optional[BetaUser]:
        """Get user by name."""
        return self.users.get(name.lower().replace(" ", "_"))

    def list_testers(self) -> List[BetaUser]:
        """Return all registered beta users."""
        return list(self.users.values())

    def get_stats(self) -> Dict:
        """Return summary statistics for the registry."""
        role_counts: Dict[str, int] = {}
        for user in self.users.values():
            role_counts[user.role.value] = role_counts.get(user.role.value, 0) + 1
        return {
            "total_testers": len(self.users),
            "roles": role_counts,
        }

# Global beta registry
beta_registry = BetaRegistry()

def initialize_wedding_team() -> Tuple[BetaUser, BetaUser, BetaUser, BetaUser]:
    """Initialize the complete wedding team including travel and payment coordination."""
    
    # Nathan as Groom/Bridge
    nathan = beta_registry.register(
        name="Nathan Robert Kleven",
        email="nkleven@example.com",
        role=BetaRole.GROOM,
        metadata={
            "title": "The Bridge / Groom",
            "secondary_role": "bridge",
            "relationship_role": "groom",
            "partner": "kelli_marie_tait",
            "wedding_context": True,
            "admin_privileges": True,
            "wedding_date": "September 10, 2027",
            "wedding_date_iso": "2027-09-10",
            "stanza": "The Bridge speaks his true name. Nathan Robert Kleven builds tomorrow.",
        }
    )
    
    # Kelli as Bride/Witness  
    kelli = beta_registry.register(
        name="Kelli Marie Tait",
        email="ktait@example.com", 
        role=BetaRole.BRIDE,
        metadata={
            "title": "Witness / Bride",
            "secondary_role": "witness",
            "relationship_role": "bride", 
            "partner": "nathan_robert_kleven",
            "wedding_context": True,
            "full_access": True,
            "wedding_date": "September 10, 2027",
            "wedding_date_iso": "2027-09-10",
            "stanza": "The gate prepares. Eden steadies. Kelli Marie Tait walks with grace.",
        }
    )
    
    # Greg as Travel Coordinator
    greg = beta_registry.register(
        name="Greg Plett",
        email="gplett@example.com",
        role=BetaRole.TRAVEL_COORDINATOR,
        metadata={
            "title": "Travel Coordinator",
            "coordination_role": "travel_coordinator",
            "wedding_context": True,
            "specialization": "logistics_and_travel",
            "supports": ["nathan_robert_kleven", "kelli_marie_tait"],
            "wedding_date": "September 10, 2027",
            "wedding_date_iso": "2027-09-10",
            "travel_payment_provider": "stripe",
            "stanza": "Greg charts the course. Paths align. Journeys begin with purpose.",
        }
    )
    
    # Stripe as Payment Processor
    stripe = beta_registry.register(
        name="Stripe",
        email="payment@stripe.com",
        role=BetaRole.PAYMENT_PROCESSOR,
        metadata={
            "title": "Payment Processor",
            "processor_type": "stripe",
            "wedding_context": True,
            "payment_enabled": True,
            "travel_payment_enabled": True,
            "supports": ["nathan_robert_kleven", "kelli_marie_tait", "greg_plett"],
            "wedding_date": "September 10, 2027",
            "wedding_date_iso": "2027-09-10",
            "stanza": "Stripe secures the flow. Transactions align. Trust builds the foundation.",
        }
    )
    
    return nathan, kelli, greg, stripe

# Initialize wedding team on module load
wedding_team = initialize_wedding_team()
