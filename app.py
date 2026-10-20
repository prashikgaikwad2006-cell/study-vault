import os
import sqlite3
from flask import Flask, render_template, request, jsonify, send_from_directory, session, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db, DB_PATH, init_db

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'studyvault-super-secret-key-cs-dept-2026'

if os.environ.get('VERCEL'):
    UPLOADS_DIR = '/tmp/uploads'
    bundled_uploads = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    if not os.path.exists(UPLOADS_DIR):
        try:
            if os.path.exists(bundled_uploads):
                import shutil
                shutil.copytree(bundled_uploads, UPLOADS_DIR)
            else:
                os.makedirs(UPLOADS_DIR, exist_ok=True)
        except Exception:
            os.makedirs(UPLOADS_DIR, exist_ok=True)
else:
    UPLOADS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    os.makedirs(UPLOADS_DIR, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOADS_DIR
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32 MB limit as per requirements

# Auto-bootstrap database and sample materials for cloud deployment
if not os.path.exists(DB_PATH):
    try:
        from seed_data import seed_database
        seed_database()
    except Exception as e:
        init_db()
else:
    init_db()

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'pptx', 'txt', 'zip', 'png', 'jpg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_size(bytes_num):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_num < 1024.0:
            return f"{bytes_num:.1f} {unit}"
        bytes_num /= 1024.0
    return f"{bytes_num:.1f} GB"

def get_current_user():
    if 'user_id' in session:
        conn = get_db()
        user = conn.execute("SELECT user_id, full_name, email, role, created_at FROM users WHERE user_id = ?", (session['user_id'],)).fetchone()
        conn.close()
        if user:
            return dict(user)
    return None

# ==================== MAIN PAGE ROUTE ====================
@app.route('/')
def index():
    user = get_current_user()
    return render_template('index.html', user=user)

# ==================== AUTHENTICATION APIS ====================
@app.route('/api/auth/me')
def api_me():
    user = get_current_user()
    return jsonify({'user': user})

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE LOWER(email) = ?", (email,)).fetchone()
    conn.close()

    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Invalid email or password.'}), 401

    session['user_id'] = user['user_id']
    session['role'] = user['role']
    return jsonify({
        'message': 'Logged in successfully.',
        'user': {
            'user_id': user['user_id'],
            'full_name': user['full_name'],
            'email': user['email'],
            'role': user['role']
        }
    })

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    data = request.get_json() or {}
    full_name = data.get('full_name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    # Public registration is strictly for students; admin accounts are reserved
    role = 'student'

    if not full_name or not email or not password:
        return jsonify({'error': 'All fields are required.'}), 400

    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters.'}), 400

    conn = get_db()
    try:
        pw_hash = generate_password_hash(password)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (full_name, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (full_name, email, pw_hash, role)
        )
        conn.commit()
        user_id = cursor.lastrowid
        session['user_id'] = user_id
        session['role'] = role
        conn.close()
        return jsonify({
            'message': 'Registration successful.',
            'user': {
                'user_id': user_id,
                'full_name': full_name,
                'email': email,
                'role': role
            }
        }), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'An account with this email already exists.'}), 409

@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully.'})


# ==================== COURSES APIS ====================
@app.route('/api/courses', methods=['GET'])
def get_courses():
    conn = get_db()
    courses = conn.execute('''
        SELECT c.*, 
               (SELECT COUNT(*) FROM subjects s WHERE s.course_id = c.course_id) AS subject_count,
               (SELECT COUNT(*) FROM study_materials m JOIN subjects s ON m.subject_id = s.subject_id WHERE s.course_id = c.course_id) AS material_count
        FROM courses c
        ORDER BY c.course_name ASC
    ''').fetchall()
    conn.close()
    return jsonify([dict(c) for c in courses])

@app.route('/api/courses', methods=['POST'])
def create_course():
    user = get_current_user()
    if not user or user['role'] != 'admin':
        return jsonify({'error': 'Unauthorized. Admin privilege required.'}), 403

    data = request.get_json() or {}
    name = data.get('course_name', '').strip()
    code = data.get('course_code', '').strip().upper()
    desc = data.get('description', '').strip()

    if not name or not code:
        return jsonify({'error': 'Course name and code are required.'}), 400

    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO courses (course_name, course_code, description) VALUES (?, ?, ?)", (name, code, desc))
        conn.commit()
        new_id = cur.lastrowid
        conn.close()
        return jsonify({'message': 'Course added successfully.', 'course_id': new_id}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': f'Course code "{code}" already exists.'}), 409

@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    user = get_current_user()
    if not user or user['role'] != 'admin':
        return jsonify({'error': 'Unauthorized. Admin privilege required.'}), 403

    conn = get_db()
    conn.execute("DELETE FROM courses WHERE course_id = ?", (course_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Course and related subjects/materials deleted.'})

# ==================== SUBJECTS APIS ====================
@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    course_id = request.args.get('course_id')
    semester = request.args.get('semester')

    query = '''
        SELECT s.*, c.course_name, c.course_code,
               (SELECT COUNT(*) FROM study_materials m WHERE m.subject_id = s.subject_id) AS material_count
        FROM subjects s
        JOIN courses c ON s.course_id = c.course_id
        WHERE 1=1
    '''
    params = []
    if course_id:
        query += " AND s.course_id = ?"
        params.append(course_id)
    if semester:
        query += " AND s.semester = ?"
        params.append(semester)

    query += " ORDER BY s.semester ASC, s.subject_name ASC"

    conn = get_db()
    subjects = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(s) for s in subjects])

@app.route('/api/subjects', methods=['POST'])
def create_subject():
    user = get_current_user()
    if not user or user['role'] != 'admin':
        return jsonify({'error': 'Unauthorized. Admin privilege required.'}), 403

    data = request.get_json() or {}
    course_id = data.get('course_id')
    semester = data.get('semester')
    name = data.get('subject_name', '').strip()
    code = data.get('subject_code', '').strip().upper()

    if not course_id or not semester or not name or not code:
        return jsonify({'error': 'All subject fields are required.'}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO subjects (course_id, semester, subject_name, subject_code) VALUES (?, ?, ?, ?)",
        (course_id, semester, name, code)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return jsonify({'message': 'Subject added successfully.', 'subject_id': new_id}), 201

@app.route('/api/subjects/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    user = get_current_user()
    if not user or user['role'] != 'admin':
        return jsonify({'error': 'Unauthorized. Admin privilege required.'}), 403

    conn = get_db()
    conn.execute("DELETE FROM subjects WHERE subject_id = ?", (subject_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Subject and associated materials deleted.'})

# ==================== STUDY MATERIALS APIS ====================
@app.route('/api/materials', methods=['GET'])
def get_materials():
    course_id = request.args.get('course_id')
    semester = request.args.get('semester')
    subject_id = request.args.get('subject_id')
    category = request.args.get('category')
    search = request.args.get('q', '').strip()
    sort_by = request.args.get('sort', 'latest')

    query = '''
        SELECT m.*, s.subject_name, s.subject_code, s.semester, c.course_id, c.course_name, c.course_code,
               u.full_name AS uploader_name,
               (SELECT COUNT(*) FROM downloads d WHERE d.material_id = m.material_id) AS download_count
        FROM study_materials m
        JOIN subjects s ON m.subject_id = s.subject_id
        JOIN courses c ON s.course_id = c.course_id
        JOIN users u ON m.uploaded_by = u.user_id
        WHERE 1=1
    '''
    params = []

    if course_id and course_id != 'all':
        query += " AND c.course_id = ?"
        params.append(course_id)

    if semester and semester != 'all':
        query += " AND s.semester = ?"
        params.append(semester)

    if subject_id and subject_id != 'all':
        query += " AND s.subject_id = ?"
        params.append(subject_id)

    if category and category != 'all':
        query += " AND m.category = ?"
        params.append(category)

    if search:
        query += " AND (m.title LIKE ? OR m.description LIKE ? OR s.subject_name LIKE ? OR s.subject_code LIKE ?)"
        wildcard = f"%{search}%"
        params.extend([wildcard, wildcard, wildcard, wildcard])

    if sort_by == 'downloads':
        query += " ORDER BY download_count DESC, m.uploaded_at DESC"
    elif sort_by == 'title':
        query += " ORDER BY m.title ASC"
    else:
        query += " ORDER BY m.uploaded_at DESC"

    conn = get_db()
    materials = conn.execute(query, params).fetchall()
    
    # Check current user's bookmarks
    user = get_current_user()
    user_bookmarks = set()
    if user:
        bms = conn.execute("SELECT material_id FROM bookmarks WHERE user_id = ?", (user['user_id'],)).fetchall()
        user_bookmarks = {b[0] for b in bms}

    conn.close()

    results = []
    for m in materials:
        item = dict(m)
        item['is_bookmarked'] = item['material_id'] in user_bookmarks
        results.append(item)

    return jsonify(results)

@app.route('/api/materials/<int:material_id>', methods=['GET'])
def get_single_material(material_id):
    conn = get_db()
    m = conn.execute('''
        SELECT m.*, s.subject_name, s.subject_code, s.semester, c.course_id, c.course_name, c.course_code,
               u.full_name AS uploader_name,
               (SELECT COUNT(*) FROM downloads d WHERE d.material_id = m.material_id) AS download_count
        FROM study_materials m
        JOIN subjects s ON m.subject_id = s.subject_id
        JOIN courses c ON s.course_id = c.course_id
        JOIN users u ON m.uploaded_by = u.user_id
        WHERE m.material_id = ?
    ''', (material_id,)).fetchone()
    conn.close()

    if not m:
        return jsonify({'error': 'Material not found.'}), 404

    return jsonify(dict(m))

@app.route('/api/materials', methods=['POST'])
def upload_material():
    user = get_current_user()
    if not user or user['role'] != 'admin':
        return jsonify({'error': 'Unauthorized. Admin credentials required to upload study materials.'}), 403

    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded.'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File format not allowed. Supported formats: PDF, DOCX, PPTX, TXT, ZIP.'}), 400

    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    subject_id = request.form.get('subject_id')
    category = request.form.get('category', 'Lecture Notes').strip()

    if not title or not subject_id:
        return jsonify({'error': 'Title and Subject are required fields.'}), 400

    original_filename = secure_filename(file.filename)
    extension = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'pdf'
    
    # Unique stored filename
    import time
    timestamp = int(time.time())
    saved_filename = f"{timestamp}_{original_filename}"
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
    file.save(save_path)

    file_size_bytes = os.path.getsize(save_path)
    file_size_str = format_size(file_size_bytes)

    conn = get_db()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO study_materials 
        (subject_id, uploaded_by, title, description, file_name, file_path, file_type, file_size, category)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        subject_id,
        user['user_id'],
        title,
        description,
        original_filename,
        f'uploads/{saved_filename}',
        extension.upper(),
        file_size_str,
        category
    ))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()

    return jsonify({'message': 'Study material uploaded successfully!', 'material_id': new_id}), 201

@app.route('/api/materials/<int:material_id>', methods=['DELETE'])
def delete_material(material_id):
    user = get_current_user()
    if not user or user['role'] != 'admin':
        return jsonify({'error': 'Unauthorized. Admin privilege required.'}), 403

    conn = get_db()
    material = conn.execute("SELECT file_path FROM study_materials WHERE material_id = ?", (material_id,)).fetchone()
    if material:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), material['file_path'])
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception:
                pass
        conn.execute("DELETE FROM study_materials WHERE material_id = ?", (material_id,))
        conn.commit()
    conn.close()
    return jsonify({'message': 'Study material deleted.'})

# ==================== DOWNLOAD & PREVIEW ROUTE ====================
@app.route('/api/materials/<int:material_id>/download')
def download_material(material_id):
    conn = get_db()
    material = conn.execute("SELECT * FROM study_materials WHERE material_id = ?", (material_id,)).fetchone()
    if not material:
        conn.close()
        return jsonify({'error': 'Material not found.'}), 404

    # Record download in database (PDF Section 3.3)
    user = get_current_user()
    user_id = user['user_id'] if user else None
    conn.execute("INSERT INTO downloads (material_id, user_id) VALUES (?, ?)", (material_id, user_id))
    conn.commit()
    conn.close()

    # Serve file
    filename = os.path.basename(material['file_path'])
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True,
        download_name=material['file_name']
    )

@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ==================== BOOKMARK TOGGLE API ====================
@app.route('/api/materials/<int:material_id>/bookmark', methods=['POST'])
def toggle_bookmark(material_id):
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Please log in to save bookmarks.'}), 401

    conn = get_db()
    existing = conn.execute("SELECT bookmark_id FROM bookmarks WHERE material_id = ? AND user_id = ?", (material_id, user['user_id'])).fetchone()
    if existing:
        conn.execute("DELETE FROM bookmarks WHERE bookmark_id = ?", (existing['bookmark_id'],))
        conn.commit()
        conn.close()
        return jsonify({'bookmarked': False, 'message': 'Removed from saved materials.'})
    else:
        conn.execute("INSERT INTO bookmarks (material_id, user_id) VALUES (?, ?)", (material_id, user['user_id']))
        conn.commit()
        conn.close()
        return jsonify({'bookmarked': True, 'message': 'Saved to your library!'})

# ==================== ANALYTICS & STATS API ====================
@app.route('/api/stats')
def get_stats():
    conn = get_db()
    total_materials = conn.execute("SELECT COUNT(*) FROM study_materials").fetchone()[0]
    total_courses = conn.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
    total_subjects = conn.execute("SELECT COUNT(*) FROM subjects").fetchone()[0]
    total_downloads = conn.execute("SELECT COUNT(*) FROM downloads").fetchone()[0]
    total_students = conn.execute("SELECT COUNT(*) FROM users WHERE role = 'student'").fetchone()[0]

    # Category breakdown
    categories = conn.execute('''
        SELECT category, COUNT(*) as count 
        FROM study_materials 
        GROUP BY category
    ''').fetchall()

    # Most popular downloads
    popular = conn.execute('''
        SELECT m.material_id, m.title, m.file_type, s.subject_name,
               COUNT(d.download_id) as dl_count
        FROM study_materials m
        LEFT JOIN downloads d ON m.material_id = d.material_id
        JOIN subjects s ON m.subject_id = s.subject_id
        GROUP BY m.material_id
        ORDER BY dl_count DESC
        LIMIT 5
    ''').fetchall()

    conn.close()
    return jsonify({
        'total_materials': total_materials,
        'total_courses': total_courses,
        'total_subjects': total_subjects,
        'total_downloads': total_downloads,
        'total_students': total_students,
        'categories': [dict(c) for c in categories],
        'popular': [dict(p) for p in popular]
    })

# ==================== RESEED DB API ====================
@app.route('/api/system/reset-demo', methods=['POST'])
def reset_demo():
    from seed_data import seed_database
    seed_database()
    return jsonify({'message': 'Demo database successfully restored with T.Y. B.Sc. CS curriculum.'})

if __name__ == '__main__':
    init_db()
    print("Starting StudyVault server on http://127.0.0.1:5000 ...")
    app.run(host='127.0.0.1', port=5000, debug=True)
