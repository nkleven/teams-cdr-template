"""Wedding dashboard and welcome interface."""

from typing import Dict
from ..config import get_config
from ..tools.wedding_countdown import wedding_countdown

def get_wedding_team_context() -> Dict:
    """Get current wedding team context for display."""
    config = get_config()
    countdown_info = wedding_countdown.get_countdown_context()
    
    if config.wedding_context_enabled:
        return {
            "bride": {
                "name": config.bride_name,
                "role": "bride",
                "title": "Witness / Bride"
            },
            "groom": {
                "name": config.groom_name, 
                "role": "groom",
                "title": "The Bridge / Groom"
            },
            "travel_coordinator": {
                "name": config.travel_coordinator_name,
                "role": "travel_coordinator", 
                "title": "Travel Coordinator"
            },
            "payment_processor": {
                "name": "Stripe",
                "provider": config.payment_provider,
                "title": "Payment Processor"
            },
            "wedding_date": {
                "date": config.wedding_date,
                "formatted": config.wedding_date_formatted,
                "year": config.wedding_year,
                "month": config.wedding_month,
                "day": config.wedding_day
            },
            "countdown": countdown_info,
            "relationship_type": config.relationship_type,
            "travel_coordination_enabled": config.travel_coordination_enabled,
            "payment_context_enabled": config.payment_context_enabled,
            "travel_payment_enabled": config.travel_payment_enabled,
            "enabled": True
        }
    
    return {"enabled": False}

def get_welcome_data() -> Dict:
    """Get welcome dashboard data."""
    team = get_wedding_team_context()
    
    if team.get("enabled"):
        team_members = [
            f"{team['groom']['name']} ({team['groom']['title']})",
            f"{team['bride']['name']} ({team['bride']['title']})",
            f"{team['travel_coordinator']['name']} ({team['travel_coordinator']['title']})",
            f"{team['payment_processor']['name']} ({team['payment_processor']['title']})"
        ]
    else:
        team_members = [
            "Nathan Robert Kleven (The Bridge)",
            "Kelli Tait (Witness)"
        ]

    return {
        "message": "Welcome to Eden - Enterprise Development & Evaluation Network",
        "status": "operational",
        "wedding_team_context": team,
        "team_members": team_members,
    }
