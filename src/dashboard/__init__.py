"""Dashboard API for monitoring and metrics visualization."""

from .server import create_dashboard_app, DashboardConfig

__all__ = ["create_dashboard_app", "DashboardConfig"]
