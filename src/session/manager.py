"""Session management for wedding context."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime, timezone


class SessionConfig(BaseModel):
    """Session configuration with wedding context support."""
    
    # Wedding team context
    wedding_context: bool = Field(default=False)
    relationship_role: Optional[str] = Field(default=None)
    partner_session_id: Optional[str] = Field(default=None)
    shared_context: bool = Field(default=False)
    
    # Travel coordination context
    travel_coordination: bool = Field(default=False)
    travel_coordinator: Optional[str] = Field(default=None)
    logistics_context: bool = Field(default=False)
    
    # Payment context
    payment_processing: bool = Field(default=False)
    payment_provider: Optional[str] = Field(default=None)
    stripe_enabled: bool = Field(default=False)
    
    # Wedding date context
    wedding_date: Optional[str] = Field(default=None)
    wedding_date_formatted: Optional[str] = Field(default=None)
    wedding_year: Optional[int] = Field(default=None)


class Session(BaseModel):
    """Session representation."""
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    config: SessionConfig
    metadata: Dict = Field(default_factory=dict)
    status: str = Field(default="active")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_accessed: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metrics: Optional[object] = Field(default=None, exclude=True)

    model_config = {"arbitrary_types_allowed": True}

    def touch(self) -> None:
        """Update last accessed timestamp."""
        self.last_accessed = datetime.now(timezone.utc)

    def to_dict(self) -> Dict:
        """Convert session to dictionary."""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat(),
            "config": self.config.model_dump(),
            "metadata": self.metadata,
        }

    def get_info(self) -> Dict:
        """Return display-friendly session info."""
        age = (datetime.now(timezone.utc) - self.created_at).total_seconds()
        idle = (datetime.now(timezone.utc) - self.last_accessed).total_seconds()
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat(),
            "age_seconds": round(age, 1),
            "idle_seconds": round(idle, 1),
            "config": self.config.model_dump(),
            "metadata": self.metadata,
        }


class SessionManager:
    """Wedding context session manager."""
    
    # Sessions older than this (seconds) are considered expired
    SESSION_TTL = 3600  # 1 hour

    def __init__(self):
        self.sessions: Dict[str, Session] = {}
    
    def create_session(self, user_id: str, config: SessionConfig = None, metadata: Dict = None) -> Session:
        """Create a new session."""
        if config is None:
            config = SessionConfig()
        if metadata is None:
            metadata = {}
            
        session = Session(user_id=user_id, config=config, metadata=metadata)
        self.sessions[session.session_id] = session
        return session

    # ---- CRUD helpers expected by dashboard endpoints ----

    def get_all_sessions(self) -> Dict[str, Session]:
        """Return all active sessions."""
        return dict(self.sessions)

    def get_session(self, session_id: str) -> Optional[Session]:
        """Get a session by ID, updating its access timestamp."""
        session = self.sessions.get(session_id)
        if session:
            session.touch()
        return session

    def delete_session(self, session_id: str) -> bool:
        """Remove a session. Returns True if it existed."""
        return self.sessions.pop(session_id, None) is not None

    def cleanup_expired_sessions(self) -> int:
        """Remove sessions that have exceeded the TTL. Returns deletion count."""
        now = datetime.now(timezone.utc)
        expired = [
            sid for sid, s in self.sessions.items()
            if (now - s.last_accessed).total_seconds() > self.SESSION_TTL
        ]
        for sid in expired:
            del self.sessions[sid]
        return len(expired)

    def get_stats(self) -> Dict:
        """Return aggregate session statistics."""
        now = datetime.now(timezone.utc)
        total = len(self.sessions)
        if total == 0:
            return {
                "total_sessions": 0,
                "active_sessions": 0,
                "expired_sessions": 0,
                "avg_age_seconds": 0,
                "avg_idle_seconds": 0,
            }

        ages = [(now - s.created_at).total_seconds() for s in self.sessions.values()]
        idles = [(now - s.last_accessed).total_seconds() for s in self.sessions.values()]
        expired = sum(1 for i in idles if i > self.SESSION_TTL)

        return {
            "total_sessions": total,
            "active_sessions": total - expired,
            "expired_sessions": expired,
            "avg_age_seconds": round(sum(ages) / total, 1),
            "avg_idle_seconds": round(sum(idles) / total, 1),
        }
    
    def create_wedding_team_session(self, user_id: str, role: str) -> Session:
        """Create a session for any wedding team member."""
        
        team_metadata = {
            "wedding_context": True,
            "team_role": role,
            "bride_name": "Kelli Marie Tait",
            "groom_name": "Nathan Robert Kleven", 
            "travel_coordinator": "Greg Plett",
            "payment_provider": "stripe",
            "wedding_date": "September 10, 2027",
            "wedding_date_iso": "2027-09-10",
            "wedding_year": 2027,
            "context_type": "wedding_team"
        }
        
        config = SessionConfig(
            wedding_context=True,
            wedding_date="2027-09-10",
            wedding_date_formatted="September 10, 2027",
            wedding_year=2027
        )
        
        if role == "travel_coordinator":
            config.travel_coordination = True
            config.logistics_context = True
            team_metadata.update({
                "travel_coordination": True,
                "logistics_access": True,
                "coordinator_name": "Greg Plett",
                "travel_payment_provider": "stripe"
            })
        elif role == "payment_processor":
            config.payment_processing = True
            config.stripe_enabled = True
            team_metadata.update({
                "payment_processing": True,
                "stripe_enabled": True,
                "provider_name": "stripe",
                "travel_payments_enabled": True
            })
        
        return self.create_session(user_id=user_id, config=config, metadata=team_metadata)


# Global session manager
session_manager = SessionManager()
