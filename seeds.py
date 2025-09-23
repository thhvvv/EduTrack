from app import create_app, db
from app.models import User, Subject, Student, Notification
app = create_app()
app.app_context().push()

# create DB
db.create_all()

# create admin if not exists
if not User.query.filter_by(email='admin@edutrack.local').first():
    admin = User(name='Administrator', email='admin@edutrack.local', role='Administrator')
    admin.set_password('password123')
    db.session.add(admin)

# sample subjects
subjects = [
    ('Mathematics','Mr. Smith'), ('English','Ms. Johnson'), ('Science','Dr. Lee')
]
for name, teacher in subjects:
    if not Subject.query.filter_by(name=name).first():
        db.session.add(Subject(name=name, teacher=teacher, students_count=30))

# sample students
for i in range(1,6):
    if not Student.query.filter_by(full_name=f'Student {i}').first():
        db.session.add(Student(full_name=f'Student {i}', grade_level='Grade 10'))

# sample notification for admin
admin = User.query.filter_by(email='admin@edutrack.local').first()
if admin and not Notification.query.filter_by(user_id=admin.id).first():
    db.session.add(Notification(user_id=admin.id, message='Welcome to EduTrack!'))

db.session.commit()
print('Seeded DB with admin@edutrack.local / password123')
