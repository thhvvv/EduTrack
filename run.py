from app import create_app, db
from app.models import User, Subject, Student, Grade, Notification

app = create_app()

# optional shell context for flask shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Subject': Subject, 'Student': Student, 'Grade': Grade, 'Notification': Notification}

if __name__ == '__main__':
    app.run(debug=True)
