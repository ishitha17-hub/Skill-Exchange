from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from models.admin import Admin
import re
import uuid
from datetime import datetime, timedelta


def create_auth_blueprint(db):
    auth_bp = Blueprint('auth', __name__)

    # ── REGISTER ───────────────────────────────────────────────────────────────
    @auth_bp.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('user.dashboard'))

        if request.method == 'POST':
            name             = request.form.get('name')
            email            = request.form.get('email')
            password         = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            skills_interests = request.form.get('skills_interests')

            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                flash('Invalid email address.', 'danger')
                return redirect(url_for('auth.register'))

            if password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return redirect(url_for('auth.register'))

            if db.users.find_one({'email': email}) or db.admins.find_one({'email': email}):
                flash('Email already registered.', 'danger')
                return redirect(url_for('auth.register'))

            db.users.insert_one({
                'name':             name,
                'email':            email,
                'password_hash':    generate_password_hash(password),
                'skills_interests': skills_interests.split(',') if skills_interests else [],
                'role':             'user',
                'is_suspended':     False,
                'created_at':       datetime.utcnow()
            })
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('auth.login'))

        return render_template('register.html')

    # ── LOGIN ──────────────────────────────────────────────────────────────────
    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            if current_user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('user.dashboard'))

        if request.method == 'POST':
            email    = request.form.get('login_user_email', request.form.get('email'))
            password = request.form.get('password')

            user = User.get_by_email(db, email)
            if user:
                if getattr(user, 'is_suspended', False):
                    flash('Account suspended. Contact admin.', 'danger')
                    return redirect(url_for('auth.login'))
                if check_password_hash(user.password_hash, password):
                    login_user(user)
                    return redirect(url_for('user.dashboard'))
            else:
                admin = Admin.get_by_email(db, email)
                if admin and check_password_hash(admin.password_hash, password):
                    login_user(admin)
                    return redirect(url_for('admin.dashboard'))

            flash('Invalid email or password.', 'danger')
            return redirect(url_for('auth.login'))

        return render_template('login.html', is_admin=False)

    # ── ADMIN LOGIN ────────────────────────────────────────────────────────────
    @auth_bp.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if current_user.is_authenticated:
            if current_user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('user.dashboard'))

        if request.method == 'POST':
            email    = request.form.get('login_user_email', request.form.get('email'))
            password = request.form.get('password')

            admin = Admin.get_by_email(db, email)
            if admin and check_password_hash(admin.password_hash, password):
                login_user(admin)
                return redirect(url_for('admin.dashboard'))

            flash('Invalid admin credentials.', 'danger')
            return redirect(url_for('auth.admin_login'))

        return render_template('login.html', is_admin=True)

    # ── LOGOUT ─────────────────────────────────────────────────────────────────
    @auth_bp.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('auth.login'))

    # ── FORGOT PASSWORD ────────────────────────────────────────────────────────
    @auth_bp.route('/forgot-password', methods=['GET', 'POST'])
    def forgot_password():
        """
        User submits email → a one-time reset token (valid 1 hr) is stored in
        MongoDB → the reset link is shown on-screen (no SMTP required).
        """
        if current_user.is_authenticated:
            return redirect(url_for('user.dashboard'))

        reset_link = None

        if request.method == 'POST':
            email = request.form.get('email', '').strip().lower()

            user_doc = db.users.find_one(
                {'email': {'$regex': f'^{re.escape(email)}$', '$options': 'i'}}
            )

            if not user_doc:
                flash('No account found with that email address.', 'danger')
                return redirect(url_for('auth.forgot_password'))

            # Remove any old unused tokens for this email
            db.password_resets.delete_many({'email': email})

            # Generate 64-char secure token
            token = uuid.uuid4().hex + uuid.uuid4().hex

            db.password_resets.insert_one({
                'email':      email,
                'token':      token,
                'created_at': datetime.utcnow(),
                'expires_at': datetime.utcnow() + timedelta(hours=1),
                'used':       False
            })

            reset_link = url_for('auth.reset_password', token=token, _external=True)

        return render_template('forgot_password.html', reset_link=reset_link)

    # ── RESET PASSWORD ─────────────────────────────────────────────────────────
    @auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
    def reset_password(token):
        """
        Token is validated (exists, unused, not expired).
        User sets a new password which is hashed and saved.
        """
        if current_user.is_authenticated:
            return redirect(url_for('user.dashboard'))

        reset_doc = db.password_resets.find_one({'token': token, 'used': False})

        if not reset_doc:
            flash('This reset link is invalid or has already been used.', 'danger')
            return redirect(url_for('auth.forgot_password'))

        if datetime.utcnow() > reset_doc['expires_at']:
            db.password_resets.delete_one({'token': token})
            flash('This reset link has expired. Please request a new one.', 'warning')
            return redirect(url_for('auth.forgot_password'))

        if request.method == 'POST':
            new_password     = request.form.get('new_password', '')
            confirm_password = request.form.get('confirm_password', '')

            if len(new_password) < 6:
                flash('Password must be at least 6 characters long.', 'danger')
                return redirect(url_for('auth.reset_password', token=token))

            if new_password != confirm_password:
                flash('Passwords do not match.', 'danger')
                return redirect(url_for('auth.reset_password', token=token))

            db.users.update_one(
                {'email': reset_doc['email']},
                {'$set': {'password_hash': generate_password_hash(new_password)}}
            )

            # Mark token consumed
            db.password_resets.update_one(
                {'token': token},
                {'$set': {'used': True}}
            )

            flash('✅ Password reset successfully! Please log in with your new password.', 'success')
            return redirect(url_for('auth.login'))

        return render_template('reset_password.html', token=token, email=reset_doc['email'])

    return auth_bp
