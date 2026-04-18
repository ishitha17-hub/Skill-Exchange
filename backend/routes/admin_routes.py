from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import uuid
from datetime import datetime
from bson.objectid import ObjectId

def create_admin_blueprint(db):
    admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

    @admin_bp.before_request
    @login_required
    def require_admin():
        if current_user.role != 'admin':
            flash('Access denied. Admin only.', 'danger')
            return redirect(url_for('auth.login'))

    @admin_bp.route('/dashboard')
    def dashboard():
        stats = {
            'total_users': db.users.count_documents({}),
            'total_skills': db.skills.count_documents({}),
            'total_tests': db.mock_tests.count_documents({}),
            'total_certificates': db.certificates.count_documents({})
        }
        return render_template('admin_dashboard.html', stats=stats)

    @admin_bp.route('/users')
    def manage_users():
        users = list(db.users.find())
        return render_template('manage_users.html', users=users)
        
    @admin_bp.route('/suspend-user/<user_id>')
    def suspend_user(user_id):
        user = db.users.find_one({'_id': ObjectId(user_id)})
        new_status = not user.get('is_suspended', False)
        db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'is_suspended': new_status}})
        flash('User status updated.', 'success')
        return redirect(url_for('admin.manage_users'))
        
    @admin_bp.route('/delete-user/<user_id>')
    def delete_user(user_id):
        db.users.delete_one({'_id': ObjectId(user_id)})
        flash('User deleted.', 'success')
        return redirect(url_for('admin.manage_users'))

    @admin_bp.route('/content')
    def manage_content():
        skills = list(db.skills.find().sort('created_at', -1))
        for skill in skills:
            user = db.users.find_one({'_id': skill['user_id']})
            skill['author_name'] = user['name'] if user else 'Unknown'
        return render_template('manage_content.html', skills=skills)
        
    @admin_bp.route('/delete-skill/<skill_id>')
    def delete_skill(skill_id):
        # We find by the custom string skill_id
        db.skills.delete_one({'skill_id': skill_id})
        flash('Skill deleted.', 'success')
        return redirect(url_for('admin.manage_content'))

    @admin_bp.route('/tests')
    def manage_tests():
        tests = list(db.mock_tests.find().sort('created_at', -1))
        for test in tests:
            skill = db.skills.find_one({'skill_id': test.get('skill_id')})
            test['skill_name'] = skill['title'] if skill else 'General'
        skills = list(db.skills.find())
        # Populate author names for skills
        for skill in skills:
            user = db.users.find_one({'_id': skill['user_id']})
            skill['author_name'] = user['name'] if user else 'Unknown'
        return render_template('manage_tests.html', tests=tests, skills=skills)
        
    @admin_bp.route('/create-test', methods=['POST'])
    def create_test():
        title = request.form.get('title')
        skill_id = request.form.get('skill_id')
        test_data = {
            'test_id': str(uuid.uuid4()),
            'title': title,
            'skill_id': skill_id,
            'created_at': datetime.utcnow()
        }
        db.mock_tests.insert_one(test_data)
        flash('Mock test created successfully!', 'success')
        return redirect(url_for('admin.manage_tests'))
        
    @admin_bp.route('/delete-test/<test_id>')
    def delete_test(test_id):
        # Handle both ObjectId and string test_ids
        try:
            db.mock_tests.delete_one({'_id': ObjectId(test_id)})
        except:
            db.mock_tests.delete_one({'test_id': test_id})
        flash('Mock test deleted.', 'success')
        return redirect(url_for('admin.manage_tests'))
        
    @admin_bp.route('/test/<test_id>/questions', methods=['GET', 'POST'])
    def manage_questions(test_id):
        # Handle both ObjectId and string test_ids
        test = None
        try:
            test = db.mock_tests.find_one({'_id': ObjectId(test_id)})
        except:
            test = db.mock_tests.find_one({'test_id': test_id})
            
        if not test:
            flash('Test not found.', 'danger')
            return redirect(url_for('admin.manage_tests'))
            
        if request.method == 'POST':
            # Validate all required fields are present and not empty
            question_text = request.form.get('question_text', '').strip()
            optionA = request.form.get('optionA', '').strip()
            optionB = request.form.get('optionB', '').strip()
            optionC = request.form.get('optionC', '').strip()
            optionD = request.form.get('optionD', '').strip()
            correct_answer = request.form.get('correct_answer', '').strip()
            
            # Check for empty fields
            if not question_text:
                flash('Question text is required.', 'warning')
                return redirect(url_for('admin.manage_questions', test_id=test_id))
            if not all([optionA, optionB, optionC, optionD]):
                flash('All four options are required.', 'warning')
                return redirect(url_for('admin.manage_questions', test_id=test_id))
            if not correct_answer or correct_answer not in ['A', 'B', 'C', 'D']:
                flash('Please select a valid correct answer (A, B, C, or D).', 'warning')
                return redirect(url_for('admin.manage_questions', test_id=test_id))
            
            question_data = {
                'test_id': str(test['_id']),
                'question_text': question_text,
                'optionA': optionA,
                'optionB': optionB,
                'optionC': optionC,
                'optionD': optionD,
                'correct_answer': correct_answer,
                'created_at': datetime.utcnow()
            }
            db.questions.insert_one(question_data)
            flash('✓ Question added successfully!', 'success')
            return redirect(url_for('admin.manage_questions', test_id=test_id))
            
        questions = list(db.questions.find({'test_id': str(test['_id'])}).sort('created_at', 1))
        
        # Get skill name for header
        skill = db.skills.find_one({'skill_id': test.get('skill_id')})
        skill_name = skill['title'] if skill else 'Unknown Skill'
        
        return render_template('Manage_questions.html', test=test, questions=questions, skill_name=skill_name)
        
    @admin_bp.route('/delete-question/<question_id>')
    def delete_question(question_id):
        q = db.questions.find_one({'_id': ObjectId(question_id)})
        test_id = q['test_id'] if q else None
        db.questions.delete_one({'_id': ObjectId(question_id)})
        flash('Question deleted.', 'success')
        if test_id:
            return redirect(url_for('admin.manage_questions', test_id=test_id))
        return redirect(url_for('admin.manage_tests'))

    @admin_bp.route('/certificates')
    def manage_certificates():
        certs = list(db.certificates.find().sort('date', -1))
        return render_template('manage_certificates.html', certs=certs)

    @admin_bp.route('/view-certificate/<cert_id>')
    def view_certificate(cert_id):
        cert = db.certificates.find_one({'cert_id': cert_id})
        if not cert:
            flash('Certificate not found.', 'danger')
            return redirect(url_for('admin.manage_certificates'))
            
        import os
        from flask import send_file
        base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        pdf_path = os.path.join(base_dir, 'static', 'certificates', f'{cert_id}.pdf')
        
        if not os.path.exists(pdf_path):
            flash('Certificate PDF file not found on server.', 'warning')
            return redirect(url_for('admin.manage_certificates'))
            
        return send_file(pdf_path)

    return admin_bp
