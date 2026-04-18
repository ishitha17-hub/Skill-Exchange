from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
import uuid, os

# ── Hardcoded curated language courses ────────────────────────────────────────
COURSES = [
    {
        'course_id': 'python-basics',
        'title': 'Python Programming',
        'subtitle': 'Learn Python from scratch – variables, loops, functions, OOP & more.',
        'icon': 'bi-filetype-py',
        'color': '#3776AB',
        'gradient': 'linear-gradient(135deg,#3776AB,#FFD43B)',
        'level': 'Beginner',
        'duration': '6 hrs',
        'videos': [
            {'title': 'Python Full Course for Beginners', 'youtube_id': 'rfscVS0vtbw', 'duration': '4h 26m'},
            {'title': 'Python OOP Tutorial', 'youtube_id': 'ZDa-Z5JzLYM', 'duration': '1h 30m'},
            {'title': 'Python Projects for Beginners', 'youtube_id': 'DLn3jOsNRVE', 'duration': '1h'},
        ],
        'questions': [
            {'q': 'Which keyword is used to define a function in Python?', 'a': 'A', 'opts': ['def', 'function', 'fun', 'define']},
            {'q': 'What is the output of print(type([]))?', 'a': 'B', 'opts': ["<class 'dict'>", "<class 'list'>", "<class 'tuple'>", "<class 'set'>"]},
            {'q': 'Which of the following is a mutable data type in Python?', 'a': 'C', 'opts': ['tuple', 'string', 'list', 'int']},
            {'q': 'What does `len("hello")` return?', 'a': 'B', 'opts': ['4', '5', '6', 'Error']},
            {'q': 'Which operator is used for floor division in Python?', 'a': 'D', 'opts': ['/', '%', '^', '//']},
            {'q': 'How do you start a comment in Python?', 'a': 'A', 'opts': ['#', '//', '/*', '--']},
            {'q': 'What does `range(3)` produce?', 'a': 'B', 'opts': ['[1,2,3]', '[0,1,2]', '[0,1,2,3]', '(0,1,2)']},
            {'q': 'Which method adds an element to the end of a list?', 'a': 'C', 'opts': ['add()', 'insert()', 'append()', 'push()']},
            {'q': 'What is the correct way to create a dictionary?', 'a': 'A', 'opts': ['{"key": "val"}', '["key":"val"]', '("key","val")', '{key=val}']},
            {'q': 'Which statement is used to handle exceptions in Python?', 'a': 'D', 'opts': ['catch', 'rescue', 'handle', 'try/except']},
        ]
    },
    {
        'course_id': 'javascript-basics',
        'title': 'JavaScript',
        'subtitle': 'Master JS fundamentals, DOM manipulation, ES6+ and async programming.',
        'icon': 'bi-filetype-js',
        'color': '#F7DF1E',
        'gradient': 'linear-gradient(135deg,#323330,#F7DF1E)',
        'level': 'Beginner',
        'duration': '5 hrs',
        'videos': [
            {'title': 'JavaScript Full Course for Beginners', 'youtube_id': 'PkZNo7MFNFg', 'duration': '3h 26m'},
            {'title': 'JavaScript ES6 Tutorial', 'youtube_id': 'NCwa_xi0Uuc', 'duration': '1h 10m'},
            {'title': 'Async JavaScript – Promises & Fetch', 'youtube_id': 'PoRJizFvM7s', 'duration': '28m'},
        ],
        'questions': [
            {'q': 'Which keyword declares a block-scoped variable in ES6?', 'a': 'B', 'opts': ['var', 'let', 'def', 'dim']},
            {'q': 'What does `===` check in JavaScript?', 'a': 'C', 'opts': ['Only value', 'Only type', 'Value and type', 'Neither']},
            {'q': 'How do you write a comment in JavaScript?', 'a': 'A', 'opts': ['// comment', '# comment', '<!-- comment -->', '** comment']},
            {'q': 'Which method converts a JSON string to an object?', 'a': 'D', 'opts': ['JSON.stringify()', 'JSON.convert()', 'JSON.read()', 'JSON.parse()']},
            {'q': 'What is the output of `typeof null`?', 'a': 'B', 'opts': ['"null"', '"object"', '"undefined"', '"boolean"']},
            {'q': 'Which array method creates a new filtered array?', 'a': 'C', 'opts': ['forEach()', 'map()', 'filter()', 'reduce()']},
            {'q': 'How do you select an element by ID in the DOM?', 'a': 'A', 'opts': ['document.getElementById()', 'document.querySelector()', 'document.getElement()', 'document.findById()']},
            {'q': 'What does `async/await` help with?', 'a': 'D', 'opts': ['Styling', 'Loops', 'Object creation', 'Asynchronous operations']},
            {'q': 'Which keyword is used to create a class in JS?', 'a': 'B', 'opts': ['object', 'class', 'struct', 'type']},
            {'q': 'What does `Array.isArray([])` return?', 'a': 'A', 'opts': ['true', 'false', '"array"', 'undefined']},
        ]
    },
    {
        'course_id': 'java-basics',
        'title': 'Java Programming',
        'subtitle': 'Core Java concepts: OOP, classes, interfaces, collections, and exceptions.',
        'icon': 'bi-cup-hot-fill',
        'color': '#ED8B00',
        'gradient': 'linear-gradient(135deg,#007396,#ED8B00)',
        'level': 'Intermediate',
        'duration': '7 hrs',
        'videos': [
            {'title': 'Java Full Course for Beginners', 'youtube_id': 'eIrMbAQSU34', 'duration': '3h 44m'},
            {'title': 'Java OOP Concepts', 'youtube_id': 'WkZMv45qM1k', 'duration': '2h'},
            {'title': 'Java Collections Framework', 'youtube_id': 'GdAon80-0KA', 'duration': '1h 15m'},
        ],
        'questions': [
            {'q': 'Which keyword is used to inherit a class in Java?', 'a': 'C', 'opts': ['implements', 'inherits', 'extends', 'super']},
            {'q': 'What is the parent class of all Java classes?', 'a': 'A', 'opts': ['Object', 'Base', 'Root', 'Main']},
            {'q': 'Which access modifier makes a member visible only within the class?', 'a': 'D', 'opts': ['public', 'protected', 'default', 'private']},
            {'q': 'What does JVM stand for?', 'a': 'B', 'opts': ['Java Variable Machine', 'Java Virtual Machine', 'Java Version Manager', 'Java Verified Module']},
            {'q': 'Which collection does not allow duplicate values?', 'a': 'C', 'opts': ['List', 'ArrayList', 'Set', 'Queue']},
            {'q': 'What is the correct entry point for a Java program?', 'a': 'A', 'opts': ['public static void main(String[] args)', 'static void main()', 'void start()', 'int main()']},
            {'q': 'Which keyword handles exceptions in Java?', 'a': 'D', 'opts': ['handle', 'rescue', 'catch only', 'try-catch']},
            {'q': 'What does the `final` keyword do to a variable?', 'a': 'B', 'opts': ['Makes it global', 'Makes it constant', 'Deletes it after use', 'Makes it static']},
            {'q': 'Which interface allows iterating over a collection?', 'a': 'C', 'opts': ['Serializable', 'Comparable', 'Iterator', 'Iterable']},
            {'q': 'What is autoboxing in Java?', 'a': 'A', 'opts': ['Auto-converting primitives to wrapper objects', 'Packaging JAR files', 'Memory compression', 'Garbage collection']},
        ]
    },
    {
        'course_id': 'cpp-basics',
        'title': 'C++ Programming',
        'subtitle': 'Systems programming with C++: pointers, memory, STL, and OOP.',
        'icon': 'bi-code-slash',
        'color': '#00599C',
        'gradient': 'linear-gradient(135deg,#00599C,#004482)',
        'level': 'Intermediate',
        'duration': '6 hrs',
        'videos': [
            {'title': 'C++ Full Course for Beginners', 'youtube_id': 'vLnPwxZdW4Y', 'duration': '4h'},
            {'title': 'C++ OOP Tutorial', 'youtube_id': 'wN0x9eZLix4', 'duration': '1h 30m'},
            {'title': 'C++ STL Tutorial', 'youtube_id': '8jLOx1hD3_o', 'duration': '1h'},
        ],
        'questions': [
            {'q': 'Which symbol is used for pointer declaration in C++?', 'a': 'B', 'opts': ['&', '*', '@', '$']},
            {'q': 'What is the correct way to declare a constant in C++?', 'a': 'A', 'opts': ['const int x = 5;', 'constant int x = 5;', 'final int x = 5;', 'static int x = 5;']},
            {'q': 'Which keyword allocates dynamic memory in C++?', 'a': 'C', 'opts': ['malloc', 'alloc', 'new', 'make']},
            {'q': 'What does `cout` do in C++?', 'a': 'D', 'opts': ['Reads input', 'Defines a class', 'Loops output', 'Prints output to console']},
            {'q': 'Which C++ feature allows functions with the same name but different parameters?', 'a': 'B', 'opts': ['Inheritance', 'Function overloading', 'Polymorphism', 'Templates']},
            {'q': 'What is the purpose of a destructor?', 'a': 'A', 'opts': ['Free resources when object is destroyed', 'Construct the object', 'Copy the object', 'Initialize members']},
            {'q': 'Which STL container stores key-value pairs?', 'a': 'C', 'opts': ['vector', 'list', 'map', 'set']},
            {'q': 'What header file is needed for cout and cin?', 'a': 'D', 'opts': ['<stdlib.h>', '<string>', '<cmath>', '<iostream>']},
            {'q': 'Which operator is used to access members of a class via pointer?', 'a': 'B', 'opts': ['.', '->', '::', '::>']},
            {'q': 'What is a virtual function in C++?', 'a': 'A', 'opts': ['A function overridden in derived class at runtime', 'A function that never executes', 'A static function', 'An inline function']},
        ]
    },
    {
        'course_id': 'sql-basics',
        'title': 'SQL & Databases',
        'subtitle': 'Database fundamentals: SELECT, JOIN, GROUP BY, indexes, and transactions.',
        'icon': 'bi-database-fill',
        'color': '#336791',
        'gradient': 'linear-gradient(135deg,#336791,#00aab5)',
        'level': 'Beginner',
        'duration': '4 hrs',
        'videos': [
            {'title': 'SQL Full Course for Beginners', 'youtube_id': 'HXV3zeQKqGY', 'duration': '4h 20m'},
            {'title': 'SQL Joins Explained', 'youtube_id': '9yeOJ0ZMUYw', 'duration': '40m'},
            {'title': 'SQL Indexes & Optimization', 'youtube_id': 'BHwzDmr6d7s', 'duration': '30m'},
        ],
        'questions': [
            {'q': 'Which SQL statement retrieves data from a table?', 'a': 'A', 'opts': ['SELECT', 'FETCH', 'GET', 'RETRIEVE']},
            {'q': 'Which clause filters rows after grouping?', 'a': 'C', 'opts': ['WHERE', 'FILTER', 'HAVING', 'GROUP']},
            {'q': 'Which JOIN returns all rows from both tables?', 'a': 'D', 'opts': ['INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'FULL OUTER JOIN']},
            {'q': 'Which keyword removes duplicate rows from a result?', 'a': 'B', 'opts': ['UNIQUE', 'DISTINCT', 'DIFFERENT', 'NODUPLICATE']},
            {'q': 'What does PRIMARY KEY enforce?', 'a': 'A', 'opts': ['Unique, non-null values', 'Foreign references', 'Indexed columns', 'Default values']},
            {'q': 'Which SQL function counts rows?', 'a': 'C', 'opts': ['SUM()', 'TOTAL()', 'COUNT()', 'NUM()']},
            {'q': 'Which statement adds a new record?', 'a': 'D', 'opts': ['ADD', 'CREATE', 'APPEND', 'INSERT INTO']},
            {'q': 'Which clause sorts the result set?', 'a': 'B', 'opts': ['GROUP BY', 'ORDER BY', 'SORT BY', 'ARRANGE BY']},
            {'q': 'What does NULL represent in SQL?', 'a': 'A', 'opts': ['Missing/unknown value', 'Zero', 'Empty string', 'False']},
            {'q': 'Which command permanently removes a table?', 'a': 'C', 'opts': ['DELETE TABLE', 'REMOVE TABLE', 'DROP TABLE', 'ERASE TABLE']},
        ]
    },
]

COURSE_MAP = {c['course_id']: c for c in COURSES}

def create_course_blueprint(db):
    course_bp = Blueprint('course', __name__, url_prefix='/user/courses')

    @course_bp.route('/')
    @login_required
    def courses_list():
        if current_user.role != 'user':
            return redirect(url_for('auth.login'))
        # Mark which courses the user already has a cert for
        earned = {c['course_id'] for c in db.certificates.find(
            {'user_id': current_user.id, 'source': 'course'}
        )}
        return render_template('Courses_list.html', courses=COURSES, earned=earned)

    @course_bp.route('/<course_id>')
    @login_required
    def course_detail(course_id):
        if current_user.role != 'user':
            return redirect(url_for('auth.login'))
        course = COURSE_MAP.get(course_id)
        if not course:
            flash('Course not found.', 'danger')
            return redirect(url_for('course.courses_list'))
        # Check if already passed
        cert = db.certificates.find_one({
            'user_id': current_user.id,
            'course_id': course_id,
            'source': 'course'
        })
        return render_template('Course_detail.html', course=course, cert=cert)

    @course_bp.route('/<course_id>/submit', methods=['POST'])
    @login_required
    def submit_course_test(course_id):
        if current_user.role != 'user':
            return redirect(url_for('auth.login'))
        course = COURSE_MAP.get(course_id)
        if not course:
            flash('Course not found.', 'danger')
            return redirect(url_for('course.courses_list'))

        questions = course['questions']
        score = 0
        total = len(questions)
        for i, q in enumerate(questions):
            selected = request.form.get(f'q_{i}')
            if selected == q['a']:
                score += 1

        passed = (score / total) >= 0.7 if total > 0 else False
        cert_id = None

        if passed:
            existing = db.certificates.find_one({
                'user_id': current_user.id,
                'course_id': course_id,
                'source': 'course'
            })
            if existing:
                cert_id = existing['cert_id']
            else:
                cert_id = str(uuid.uuid4())
                date_str = datetime.utcnow().strftime('%B %d, %Y')

                from utils.pdf_generator import generate_certificate_pdf
                base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
                cert_dir = os.path.join(base_dir, 'static', 'certificates')
                os.makedirs(cert_dir, exist_ok=True)
                pdf_path = os.path.join(cert_dir, f'{cert_id}.pdf')
                generate_certificate_pdf(current_user.name, course['title'], date_str, pdf_path)

                db.certificates.insert_one({
                    'cert_id': cert_id,
                    'user_id': current_user.id,
                    'user_name': current_user.name,
                    'course_id': course_id,
                    'skill_name': course['title'],
                    'skill_id': '',
                    'source': 'course',
                    'date': datetime.utcnow(),
                    'file_path': f'/static/certificates/{cert_id}.pdf'
                })

        return render_template('course_result.html',
                               course=course, score=score, total=total,
                               passed=passed, cert_id=cert_id)

    @course_bp.route('/certificate/<cert_id>/download')
    @login_required
    def download_course_cert(cert_id):
        if current_user.role != 'user':
            return redirect(url_for('auth.login'))
        cert = db.certificates.find_one({'cert_id': cert_id, 'user_id': current_user.id})
        if not cert:
            flash('Certificate not found.', 'danger')
            return redirect(url_for('course.courses_list'))

        from flask import send_file
        from utils.pdf_generator import generate_certificate_pdf
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        cert_dir = os.path.join(base_dir, 'static', 'certificates')
        os.makedirs(cert_dir, exist_ok=True)
        pdf_path = os.path.join(cert_dir, f'{cert_id}.pdf')

        if not os.path.exists(pdf_path):
            date_str = cert['date'].strftime('%B %d, %Y')
            generate_certificate_pdf(cert.get('user_name', current_user.name),
                                     cert.get('skill_name', 'Course'), date_str, pdf_path)

        safe = current_user.name.replace(' ', '_')
        return send_file(pdf_path, as_attachment=True,
                         download_name=f'{safe}_{cert.get("skill_name","Course").replace(" ","_")}_Certificate.pdf')

    return course_bp
