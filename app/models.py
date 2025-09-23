from datetime import datetime
from . import db
from flask_login import UserMixin

# -------------------------
# User Model (Admin, Teacher, Student, Parent)
# -------------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="student")  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    notifications = db.relationship("Notification", backref="user", lazy=True)

    def is_admin(self):
        return self.role == "admin"

    def is_teacher(self):
        return self.role == "teacher"


# -------------------------
# Subject Model
# -------------------------
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("user.id"))  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# -------------------------
# Student Progress Model
# -------------------------
class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    score = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


# -------------------------
# Notifications
# -------------------------
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
