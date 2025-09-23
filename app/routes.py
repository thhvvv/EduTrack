from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import User, Subject, Student, Grade, Notification
from .forms import LoginForm, SignupForm
from datetime import date

auth_bp = Blueprint('auth', __name__)
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

# ===== AUTH ROUTES =====
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.index'))
        flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'warning')
        else:
            u = User(name=form.name.data, email=form.email.data, role='Administrator')
            u.set_password(form.password.data)
            db.session.add(u)
            db.session.commit()
            flash('Account created. Please log in.', 'success')
            return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


# ===== MAIN VIEWS (rendering templates) =====
@main_bp.route('/')
@login_required
def index():
    subjects = Subject.query.all()
    students = Student.query.limit(6).all()
    unread_count = Notification.query.filter_by(is_read=False, user_id=current_user.id).count()
    return render_template('index.html',
                           user=current_user,
                           subjects=subjects,
                           students=students,
                           unread_count=unread_count)


@main_bp.route('/students')
@login_required
def students_view():
    students = Student.query.all()
    return render_template('students.html', user=current_user, students=students)


@main_bp.route('/subjects')
@login_required
def subjects_view():
    subjects = Subject.query.all()
    return render_template('subjects.html', user=current_user, subjects=subjects)


@main_bp.route('/grades')
@login_required
def grades_view():
    grades = Grade.query.order_by(Grade.date.desc()).limit(50).all()
    return render_template('grades.html', user=current_user, grades=grades)


@main_bp.route('/reports')
@login_required
def reports_view():
    return render_template('reports.html', user=current_user)


# ===== API endpoints for AJAX / CRUD =====
# Create subject
@api_bp.route('/subjects', methods=['POST'])
@login_required
def api_create_subject():
    data = request.get_json() or request.form
    name = data.get('name')
    teacher = data.get('teacher')
    if not name:
        return jsonify({'error': 'Name required'}), 400
    s = Subject(name=name, teacher=teacher, students_count=0)
    db.session.add(s)
    db.session.commit()
    return jsonify({'id': s.id, 'name': s.name, 'teacher': s.teacher}), 201

# Update subject
@api_bp.route('/subjects/<int:id>', methods=['PUT'])
@login_required
def api_update_subject(id):
    s = Subject.query.get_or_404(id)
    data = request.get_json() or request.form
    s.name = data.get('name', s.name)
    s.teacher = data.get('teacher', s.teacher)
    db.session.commit()
    return jsonify({'id': s.id, 'name': s.name, 'teacher': s.teacher})

# Delete subject
@api_bp.route('/subjects/<int:id>', methods=['DELETE'])
@login_required
def api_delete_subject(id):
    s = Subject.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    return jsonify({'result': 'deleted'})

# Notifications: fetch / mark read
@api_bp.route('/notifications', methods=['GET'])
@login_required
def api_get_notifications():
    notes = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).limit(50).all()
    data = [{'id': n.id, 'message': n.message, 'is_read': n.is_read, 'created_at': n.created_at.isoformat()} for n in notes]
    return jsonify(data)

@api_bp.route('/notifications/<int:id>/read', methods=['POST'])
@login_required
def api_mark_notification_read(id):
    n = Notification.query.get_or_404(id)
    n.is_read = True
    db.session.commit()
    return jsonify({'result': 'ok'})

# Simple student creation (example)
@api_bp.route('/students', methods=['POST'])
@login_required
def api_create_student():
    data = request.get_json() or request.form
    full_name = data.get('full_name')
    grade_level = data.get('grade_level')
    if not full_name:
        return jsonify({'error': 'name required'}), 400
    s = Student(full_name=full_name, grade_level=grade_level)
    db.session.add(s)
    db.session.commit()
    return jsonify({'id': s.id, 'full_name': s.full_name}), 201
