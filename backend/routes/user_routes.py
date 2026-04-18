from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import uuid
from datetime import datetime

def create_user_blueprint(db):
    user_bp = Blueprint('user', __name__, url_prefix='/user')

    @user_bp.route('/dashboard')
    @login_required
    def dashboard():
        if current_user.role != 'user':
            flash('Access denied. Please login as a user.', 'danger')
            return redirect(url_for('auth.login'))
            
        user_skills = list(db.skills.find({'user_id': current_user.id}).sort('created_at', -1))
        
        stats = {
            'skills_uploaded': len(user_skills),
            'tests_passed': db.test_results.count_documents({'user_id': current_user.id, 'passed': True}),
            'certificates': db.certificates.count_documents({'user_id': current_user.id})
        }

        user_certs = list(db.certificates.find({'user_id': current_user.id}).sort('date', -1))
        for cert in user_certs:
            if not cert.get('skill_name'):
                skill = db.skills.find_one({'skill_id': cert.get('skill_id', '')})
                cert['skill_name'] = skill['title'] if skill else 'Unknown Skill'

        return render_template('dashboard.html', stats=stats, user_skills=user_skills, user_certs=user_certs)

    @user_bp.route('/upload-skill', methods=['GET', 'POST'])
    @login_required
    def upload_skill():
        if current_user.role != 'user':
            return redirect(url_for('auth.login'))
            
        if request.method == 'POST':
            title = request.form.get('title')
            description = request.form.get('description')
            resource_link = request.form.get('resource_link')
            
            skill_id = str(uuid.uuid4())
            
            skill_data = {
                'skill_id': skill_id,
                'user_id': current_user.id,
                'title': title,
                'description': description,
                'resources': [resource_link] if resource_link else [],
                'created_at': datetime.utcnow()
            }
            
            db.skills.insert_one(skill_data)
            flash('Skill and learning resources uploaded successfully!', 'success')
            return redirect(url_for('user.dashboard'))
            
        return render_template('upload_skill.html')

    @user_bp.route('/skills', methods=['GET'])
    @login_required
    def browse_skills():
        if current_user.role != 'user':
            return redirect(url_for('auth.login'))
            
        search_query = request.args.get('q', '')
        if search_query:
            skills = list(db.skills.find({
                '$or': [
                    {'title': {'$regex': search_query, '$options': 'i'}},
                    {'description': {'$regex': search_query, '$options': 'i'}}
                ]
            }).sort('created_at', -1))
        else:
            skills = list(db.skills.find().sort('created_at', -1))
            
        for skill in skills:
            user = db.users.find_one({'_id': skill['user_id']})
            skill['author_name'] = user['name'] if user else 'Unknown Student'
            
        return render_template('skills.html', skills=skills, search_query=search_query)

    @user_bp.route('/mock-tests')
    @user_bp.route('/mock-tests/<skill_id>')
    @login_required
    def mock_tests(skill_id=None):
        if current_user.role != 'user':
            return redirect(url_for('auth.login'))
            
        if skill_id:
            tests = list(db.mock_tests.find({'skill_id': skill_id}).sort('created_at', -1))
            skill = db.skills.find_one({'skill_id': skill_id})
            skill_title = skill['title'] if skill else 'Unknown Skill'
        else:
            tests = list(db.mock_tests.find().sort('created_at', -1))
            skill_title = 'All Skills'

        # Enrich each test with its skill name
        for test in tests:
            sk = db.skills.find_one({'skill_id': test.get('skill_id', '')})
            test['skill_name'] = sk['title'] if sk else 'General'

        return render_template('mock_tests_list.html', tests=tests, skill_title=skill_title, skill_id=skill_id)

    @user_bp.route('/take-test/<test_id>', methods=['GET', 'POST'])
    @login_required
    def take_test(test_id):
        if current_user.role != 'user':
            return redirect(url_for('auth.login'))
            
        test = db.mock_tests.find_one({'_id': test_id}) or db.mock_tests.find_one({'test_id': test_id})
        # If test_id isn't UUID but ObjectId string, handle it gracefully
        from bson.objectid import ObjectId
        if not test:
            try:
                test = db.mock_tests.find_one({'_id': ObjectId(test_id)})
            except:
                pass
                
        if not test:
            flash('Test not found.', 'danger')
            return redirect(url_for('user.dashboard'))
            
        questions = list(db.questions.find({'test_id': str(test['_id'])}))
        if not questions:
            # Fallback for how admin might create tests
            questions = list(db.questions.find({'test_id': test.get('test_id', str(test['_id']))}))
            
        if request.method == 'POST':
            score = 0
            total = len(questions)
            
            for q in questions:
                q_id = str(q['_id'])
                selected_option = request.form.get(f'question_{q_id}')
                if selected_option and selected_option == q['correct_answer']:
                    score += 1
                    
            passed = (score / total) >= 0.7 if total > 0 else False
            
            result_data = {
                'user_id': current_user.id,
                'test_id': str(test['_id']),
                'score': score,
                'total': total,
                'passed': passed,
                'date_taken': datetime.utcnow()
            }
            db.test_results.insert_one(result_data)
            
            skill_id = test.get('skill_id', '')
            cert_id = None

            # Automatically generate certificate if passed
            if passed:
                # Check if certificate already exists for this user+test
                existing_cert = db.certificates.find_one({
                    'user_id': current_user.id,
                    'test_id': str(test['_id'])
                })
                if existing_cert:
                    cert_id = existing_cert['cert_id']
                else:
                    cert_id = str(uuid.uuid4())
                    skill = db.skills.find_one({'skill_id': skill_id})
                    skill_name = skill['title'] if skill else test.get('title', 'Skill')
                    date_str = datetime.utcnow().strftime('%B %d, %Y')

                    # Generate the PDF immediately
                    import os
                    from utils.pdf_generator import generate_certificate_pdf
                    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
                    cert_dir = os.path.join(base_dir, 'static', 'certificates')
                    os.makedirs(cert_dir, exist_ok=True)
                    pdf_path = os.path.join(cert_dir, f'{cert_id}.pdf')
                    generate_certificate_pdf(current_user.name, skill_name, date_str, pdf_path)

                    cert_data = {
                        'cert_id': cert_id,
                        'user_id': current_user.id,
                        'user_name': current_user.name,
                        'skill_id': skill_id,
                        'skill_name': skill_name,
                        'test_id': str(test['_id']),
                        'date': datetime.utcnow(),
                        'file_path': f'/static/certificates/{cert_id}.pdf'
                    }
                    db.certificates.insert_one(cert_data)

            return render_template('result.html', score=score, total=total, passed=passed, test=test, cert_id=cert_id)
            
        return render_template('mock_test.html', test=test, questions=questions)

    @user_bp.route('/download-certificate/<cert_id>')
    @login_required
    def download_certificate(cert_id):
        if current_user.role != 'user':
            return redirect(url_for('auth.login'))

        cert = db.certificates.find_one({'cert_id': cert_id, 'user_id': current_user.id})
        if not cert:
            flash('Certificate not found or access denied.', 'danger')
            return redirect(url_for('user.dashboard'))

        import os
        from utils.pdf_generator import generate_certificate_pdf
        from flask import send_file

        base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        cert_dir = os.path.join(base_dir, 'static', 'certificates')
        os.makedirs(cert_dir, exist_ok=True)
        pdf_path = os.path.join(cert_dir, f'{cert_id}.pdf')

        # Re-generate if PDF was lost (e.g. server restart clearing tmp)
        if not os.path.exists(pdf_path):
            skill_name = cert.get('skill_name') or 'Unknown Skill'
            if not skill_name or skill_name == 'Unknown Skill':
                skill = db.skills.find_one({'skill_id': cert['skill_id']})
                skill_name = skill['title'] if skill else 'Unknown Skill'
            user_name = cert.get('user_name', current_user.name)
            date_str = cert['date'].strftime('%B %d, %Y')
            generate_certificate_pdf(user_name, skill_name, date_str, pdf_path)

        safe_name = current_user.name.replace(' ', '_')
        return send_file(pdf_path, as_attachment=True, download_name=f'{safe_name}_Certificate.pdf')

    return user_bp
