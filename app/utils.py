from datetime import datetime
from . import db
from .models import Notification

def create_notification(user_id, message):
    """Create and save a notification for a user."""
    from flask_login import current_user

    note = Notification(user_id=user_id, message=message, is_read=False, created_at=datetime.utcnow())
    db.session.add(note)
    db.session.commit()
    return note


def format_datetime(dt):
    """Format a datetime object for display in templates."""
    if not dt:
        return ""
    return dt.strftime("%b %d, %Y %I:%M %p")


def seed_notifications_for_demo(user_id):
    """Quick helper to generate some demo notifications for testing UI."""
    messages = [
        "New student registered successfully.",
        "Math test results uploaded.",
        "Reminder: Parent-Teacher meeting tomorrow.",
    ]
    for msg in messages:
        create_notification(user_id, msg)
