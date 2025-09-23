from app import create_app, db
from flask.cli import FlaskGroup

# Create the app with your factory function
app = create_app()

# Attach Flask CLI to app
cli = FlaskGroup(app)


# -------------------------
# Custom commands
# -------------------------

# Initialize the database
@cli.command("create_db")
def create_db():
    """Create all database tables."""
    db.create_all()
    print("Database tables created!")


# Drop all tables (careful with this!)
@cli.command("drop_db")
def drop_db():
    """Drop all database tables."""
    db.drop_all()
    print("Database tables dropped!")


# Seed the database with sample data
@cli.command("seed_db")
def seed_db():
    """Seed the database with sample data."""
    from app.models import User, Subject

    admin = User(username="admin", email="admin@edutrack.com",
                 password="admin123", role="admin")
    teacher = User(username="teacher", email="teacher@edutrack.com",
                   password="teacher123", role="teacher")
    student = User(username="student", email="student@edutrack.com",
                   password="student123", role="student")

    math = Subject(name="Mathematics", teacher_id=2)
    science = Subject(name="Science", teacher_id=2)

    db.session.add(admin)
    db.session.add(teacher)
    db.session.add(student)
    db.session.add(math)
    db.session.add(science)

    db.session.commit()
    print("Database seeded with demo data!")


if __name__ == "__main__":
    cli()
