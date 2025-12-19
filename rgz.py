from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import sqlite3
from os import path
import os
import json
import uuid
import random
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

rgz = Blueprint('rgz', __name__, template_folder='templates', static_folder='static')

db_path = path.join(path.dirname(path.realpath(__file__)), "rgz.db")

CUR_DIR = path.dirname(path.realpath(__file__))
BASE_DIR = path.dirname(path.dirname(path.realpath(__file__)))
UPLOAD_FOLDER = path.join(CUR_DIR, 'static', 'uploads')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def db_connect():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def get_rgz_user():
    if 'rgz_user_id' in session:
        conn, cur = db_connect()
        cur.execute("SELECT * FROM rgz_users WHERE id = ?", (session['rgz_user_id'],))
        user = cur.fetchone()
        db_close(conn, cur)
        if user:
            return dict(user)
    return None

def init_db():
    conn, cur = db_connect()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS rgz_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            age INTEGER NOT NULL CHECK(age >= 18 AND age <= 100),
            gender TEXT NOT NULL CHECK(gender IN ('male', 'female')),
            search_gender TEXT NOT NULL CHECK(search_gender IN ('male', 'female')),
            about TEXT,
            photo_url TEXT DEFAULT '/static/rgz/default_avatar.png',
            is_hidden INTEGER DEFAULT 0,
            is_admin INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
  
    cur.execute("""
        CREATE TABLE IF NOT EXISTS rgz_search_sessions (
            session_id TEXT PRIMARY KEY,
            user_ids TEXT NOT NULL,
            search_params TEXT NOT NULL,
            current_offset INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("SELECT * FROM rgz_users WHERE login = 'admin'")
    admin = cur.fetchone()
    if not admin:
        hashed_password = generate_password_hash('admin123')
        cur.execute("""
            INSERT INTO rgz_users (login, password, name, age, gender, search_gender, about, is_admin)
            VALUES (?, ?, 'Администратор', 30, 'male', 'female', 'Администратор сайта', 1)
        """, ('admin', hashed_password))
 
    cur.execute("SELECT COUNT(*) as count FROM rgz_users WHERE login LIKE 'male%' OR login LIKE 'female%'")
    test_users_count = cur.fetchone()['count']

    if test_users_count < 20:  
        print(f"Creating test users... Current test users: {test_users_count}")

        male_names = ['Алексей', 'Дмитрий', 'Сергей', 'Андрей', 'Иван', 'Максим', 'Артем', 'Владимир', 'Павел', 'Константин']
        for i, name in enumerate(male_names):
            login = f'male{i+1}'

            cur.execute("SELECT id FROM rgz_users WHERE login = ?", (login,))
            if not cur.fetchone():
                hashed_password = generate_password_hash('password123')
                age = 20 + i
                about = f'{name}. Люблю активный отдых.'
                try:
                    cur.execute("""
                        INSERT INTO rgz_users (login, password, name, age, gender, search_gender, about)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (login, hashed_password, name, age, 'male', 'female', about))
                except sqlite3.IntegrityError:
                    pass  
    
        female_names = ['Анна', 'Елена', 'Мария', 'Ольга', 'Ирина', 'Наталья', 'Светлана', 'Татьяна', 'Юлия', 'Екатерина']
        for i, name in enumerate(female_names):
            login = f'female{i+1}'
           
            cur.execute("SELECT id FROM rgz_users WHERE login = ?", (login,))
            if not cur.fetchone():
                hashed_password = generate_password_hash('password123')
                age = 20 + i
                about = f'{name}. Ищу серьезные отношения.'
                try:
                    cur.execute("""
                        INSERT INTO rgz_users (login, password, name, age, gender, search_gender, about)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (login, hashed_password, name, age, 'female', 'male', about))
                except sqlite3.IntegrityError:
                    pass  
    
    db_close(conn, cur)


def add_rgz_info():
    return {
        'student_name': 'Ничипоренко Юлия Николаевна',
        'student_group': 'ФБИ-33',
        'rgz_user': get_rgz_user()
    }

@rgz.route('/')
def index():
    return render_template('rgz/index.html', **add_rgz_info())

@rgz.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('rgz/register.html', **add_rgz_info())
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    method = data.get('method')
    params = data.get('params', {})
    
    if method != 'register':
        return jsonify({'error': 'Method not found'}), 404
    
    login = params.get('login', '').strip()
    password = params.get('password', '').strip()
    name = params.get('name', '').strip()
    age = params.get('age', 0)
    gender = params.get('gender', '')
    search_gender = params.get('search_gender', '')
    
    errors = []
    if not login or len(login) < 3:
        errors.append('Логин должен быть не менее 3 символов')
    if not all(c.isalnum() or c in '._-@' for c in login):
        errors.append('Логин должен содержать только латинские буквы, цифры и символы ._-@')
    if not password or len(password) < 6:
        errors.append('Пароль должен быть не менее 6 символов')
    if not name:
        errors.append('Имя не может быть пустым')
    if not 18 <= age <= 100:
        errors.append('Возраст должен быть от 18 до 100 лет')
    if gender not in ['male', 'female']:
        errors.append('Укажите пол')
    if search_gender not in ['male', 'female']:
        errors.append('Укажите пол для поиска')
    
    if errors:
        return jsonify({'error': errors}), 400
    
    conn, cur = db_connect()
    
    cur.execute("SELECT id FROM rgz_users WHERE login = ?", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return jsonify({'error': ['Пользователь с таким логином уже существует']}), 400
    
    hashed_password = generate_password_hash(password)
    cur.execute("""
        INSERT INTO rgz_users (login, password, name, age, gender, search_gender)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (login, hashed_password, name, age, gender, search_gender))
    
    user_id = cur.lastrowid
    db_close(conn, cur)
    
    return jsonify({'result': {'user_id': user_id, 'message': 'Регистрация успешна'}})

@rgz.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html', **add_rgz_info())
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    method = data.get('method')
    params = data.get('params', {})
    
    if method != 'login':
        return jsonify({'error': 'Method not found'}), 404
    
    login = params.get('login', '').strip()
    password = params.get('password', '').strip()
    
    conn, cur = db_connect()
    cur.execute("SELECT * FROM rgz_users WHERE login = ?", (login,))
    user = cur.fetchone()
    db_close(conn, cur)
    
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'error': ['Неверный логин или пароль']}), 401
    
    session['rgz_user_id'] = user['id']
    return jsonify({'result': {
        'user_id': user['id'],
        'name': user['name'],
        'is_admin': bool(user['is_admin'])
    }})

@rgz.route('/logout', methods=['POST'])
def logout():
    session.pop('rgz_user_id', None)
    return jsonify({'result': 'success'})

@rgz.route('/profile')
def profile():
    user = get_rgz_user()
    if not user:
        return redirect(url_for('rgz.login'))
    return render_template('rgz/profile.html', **add_rgz_info())

@rgz.route('/api/profile', methods=['POST'])
def get_profile():
    user = get_rgz_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    method = data.get('method')
    if method != 'get_profile':
        return jsonify({'error': 'Method not found'}), 404
    
    user_data = dict(user)
    user_data.pop('password', None)
    user_data['is_admin'] = bool(user_data['is_admin'])
    user_data['is_hidden'] = bool(user_data['is_hidden'])
    
    return jsonify({'result': user_data})

@rgz.route('/edit_profile')
def edit_profile_page():
    user = get_rgz_user()
    if not user:
        return redirect(url_for('rgz.login'))
    return render_template('rgz/edit_profile.html', **add_rgz_info())

@rgz.route('/api/edit_profile', methods=['POST'])
def edit_profile():
    user = get_rgz_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    method = data.get('method')
    params = data.get('params', {})
    
    if method != 'edit_profile':
        return jsonify({'error': 'Method not found'}), 404
    
    name = params.get('name', '').strip()
    age = params.get('age', 0)
    gender = params.get('gender', '')
    search_gender = params.get('search_gender', '')
    about = params.get('about', '').strip()
    is_hidden = params.get('is_hidden', False)
    
    errors = []
    if not name:
        errors.append('Имя не может быть пустым')
    if not 18 <= age <= 100:
        errors.append('Возраст должен быть от 18 до 100 лет')
    if gender not in ['male', 'female']:
        errors.append('Укажите пол')
    if search_gender not in ['male', 'female']:
        errors.append('Укажите пол для поиска')
    
    if errors:
        return jsonify({'error': errors}), 400
    
    conn, cur = db_connect()
    cur.execute("""
        UPDATE rgz_users 
        SET name = ?, age = ?, gender = ?, search_gender = ?, about = ?, is_hidden = ?
        WHERE id = ?
    """, (name, age, gender, search_gender, about, 1 if is_hidden else 0, user['id']))
    db_close(conn, cur)
    
    session['rgz_user_id'] = user['id']
    return jsonify({'result': 'Профиль обновлен'})
    
@rgz.route('/api/upload_photo', methods=['POST'])
def upload_photo():
    user = get_rgz_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    print(f"=== DEBUG UPLOAD START ===")
    print(f"User ID: {user['id']}")
    print(f"Files in request: {list(request.files.keys())}")
    
    if 'photo' not in request.files:
        print("ERROR: No 'photo' in request.files")
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['photo']
    print(f"File received: {file.filename}, Size: {len(file.read()) if file else 0} bytes")

    if file:
        file.seek(0)
    
    if file.filename == '':
        print("ERROR: Empty filename")
        return jsonify({'error': 'No selected file'}), 400

    allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif'}
    filename_lower = file.filename.lower()
    file_ext = None
    
    for ext in allowed_extensions:
        if filename_lower.endswith(ext):
            file_ext = ext
            break
    
    if not file_ext:
        print(f"ERROR: Invalid file extension: {file.filename}")
        return jsonify({'error': f'Допустимы только изображения: {", ".join(allowed_extensions)}'}), 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"Folder exists: {os.path.exists(UPLOAD_FOLDER)}")

    import uuid
    unique_filename = f"{user['id']}_{uuid.uuid4().hex[:8]}{file_ext}"
    filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
    
    print(f"Saving to: {filepath}")
    
    try:

        file.save(filepath)
        print(f"File saved successfully")

        file_size = os.path.getsize(filepath)
        print(f"File size after saving: {file_size} bytes")
        
        if file_size == 0:
            print("ERROR: File is empty after saving!")
            os.remove(filepath)
            return jsonify({'error': 'Файл пустой после сохранения'}), 500
            
    except Exception as e:
        print(f"ERROR saving file: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Ошибка сохранения файла: {str(e)}'}), 500

    photo_url = f"/static/uploads/{unique_filename}"
    print(f"Photo URL: {photo_url}")

    conn, cur = db_connect()
    try:
        cur.execute("UPDATE rgz_users SET photo_url = ? WHERE id = ?", (photo_url, user['id']))
        db_close(conn, cur)
        print(f"Database updated")
    except Exception as e:
        db_close(conn, cur)
        print(f"ERROR updating database: {str(e)}")
        return jsonify({'error': f'Ошибка базы данных: {str(e)}'}), 500
    
    print(f"=== DEBUG UPLOAD END ===")
    return jsonify({'result': {'photo_url': photo_url}})

@rgz.route('/search')
def search_page():
    user = get_rgz_user()
    if not user:
        return redirect(url_for('rgz.login'))
    return render_template('rgz/search.html', **add_rgz_info())

@rgz.route('/api/search', methods=['POST'])
def search_users():
    user = get_rgz_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    method = data.get('method')
    params = data.get('params', {})
    
    if method != 'search':
        return jsonify({'error': 'Method not found'}), 404
    
    name_filter = params.get('name', '').strip()
    age_from = params.get('age_from')
    age_to = params.get('age_to')
    session_id = params.get('session_id')
    get_next = params.get('get_next', False)
    
    conn, cur = db_connect()
    
    if session_id and get_next:
        cur.execute("SELECT * FROM rgz_search_sessions WHERE session_id = ?", (session_id,))
        session_data = cur.fetchone()
        
        if not session_data:
            return jsonify({'error': 'Session expired'}), 400
        
        user_ids = json.loads(session_data['user_ids'])
        current_offset = session_data['current_offset']
        
        start_idx = current_offset
        end_idx = min(start_idx + 3, len(user_ids))
        
        if start_idx >= len(user_ids):
            return jsonify({'result': {'users': [], 'has_more': False}})
        
        next_user_ids = user_ids[start_idx:end_idx]
        placeholders = ','.join(['?'] * len(next_user_ids))
        
        cur.execute(f"""
            SELECT id, name, age, gender, about, photo_url 
            FROM rgz_users 
            WHERE id IN ({placeholders}) AND is_hidden = 0
        """, next_user_ids)
        
        users = [dict(row) for row in cur.fetchall()]
        
        new_offset = current_offset + 3
        has_more = new_offset < len(user_ids)
        
        cur.execute("UPDATE rgz_search_sessions SET current_offset = ? WHERE session_id = ?", (new_offset, session_id))
        db_close(conn, cur)
        
        return jsonify({
            'result': {
                'users': users,
                'has_more': has_more,
                'session_id': session_id
            }
        })
    
    query = """
        SELECT id, name, age, gender, about, photo_url 
        FROM rgz_users 
        WHERE id != ? AND is_hidden = 0 
          AND search_gender = ?
    """
    query_params = [user['id'], user['gender']]
    
    if name_filter:
        query += " AND name LIKE ?"
        query_params.append(f'%{name_filter}%')
    
    if age_from is not None:
        query += " AND age >= ?"
        query_params.append(age_from)
    
    if age_to is not None:
        query += " AND age <= ?"
        query_params.append(age_to)
    
    cur.execute(query, query_params)
    all_users = [dict(row) for row in cur.fetchall()]
    
    random.shuffle(all_users)
    user_ids = [u['id'] for u in all_users]
    first_users = all_users[:3]
    
    session_id = str(uuid.uuid4())
    search_params = json.dumps({'name': name_filter, 'age_from': age_from, 'age_to': age_to})
    
    cur.execute("""
        INSERT INTO rgz_search_sessions (session_id, user_ids, search_params, current_offset)
        VALUES (?, ?, ?, ?)
    """, (session_id, json.dumps(user_ids), search_params, 3))
    
    db_close(conn, cur)
    
    has_more = len(user_ids) > 3
    
    return jsonify({
        'result': {
            'users': first_users,
            'has_more': has_more,
            'session_id': session_id
        }
    })

@rgz.route('/api/delete_account', methods=['POST'])
def delete_account():
    user = get_rgz_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    method = data.get('method')
    if method != 'delete_account':
        return jsonify({'error': 'Method not found'}), 404
    
    conn, cur = db_connect()
    cur.execute("DELETE FROM rgz_users WHERE id = ?", (user['id'],))
    db_close(conn, cur)
    
    session.pop('rgz_user_id', None)
    return jsonify({'result': 'Аккаунт удален'})

@rgz.route('/admin')
def admin():
    user = get_rgz_user()
    if not user or not user['is_admin']:
        return redirect(url_for('rgz.login'))
    return render_template('rgz/admin.html', **add_rgz_info())

@rgz.route('/api/admin/users', methods=['POST'])
def admin_get_users():
    user = get_rgz_user()
    if not user or not user['is_admin']:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    method = data.get('method')
    if method != 'get_users':
        return jsonify({'error': 'Method not found'}), 404
    
    conn, cur = db_connect()
    cur.execute("SELECT id, login, name, age, gender, is_hidden, created_at FROM rgz_users ORDER BY id DESC")
    users = [dict(row) for row in cur.fetchall()]
    db_close(conn, cur)
    
    return jsonify({'result': users})

@rgz.route('/api/admin/delete_user', methods=['POST'])
def admin_delete_user():
    user = get_rgz_user()
    if not user or not user['is_admin']:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    method = data.get('method')
    params = data.get('params', {})
    
    if method != 'delete_user':
        return jsonify({'error': 'Method not found'}), 404
    
    user_id = params.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID required'}), 400
    
    conn, cur = db_connect()
    cur.execute("DELETE FROM rgz_users WHERE id = ?", (user_id,))
    db_close(conn, cur)
    
    return jsonify({'result': 'Пользователь удален'})

@rgz.route('/api/stats', methods=['POST'])
def get_stats():
    user = get_rgz_user()
    if not user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    method = data.get('method')
    if method != 'get_stats':
        return jsonify({'error': 'Method not found'}), 404
    
    conn, cur = db_connect()
    
    cur.execute("SELECT COUNT(*) as total FROM rgz_users")
    total = cur.fetchone()['total']
    
    cur.execute("SELECT COUNT(*) as male FROM rgz_users WHERE gender = 'male'")
    male = cur.fetchone()['male']
    
    cur.execute("SELECT COUNT(*) as female FROM rgz_users WHERE gender = 'female'")
    female = cur.fetchone()['female']
    
    cur.execute("SELECT AVG(age) as avg_age FROM rgz_users")
    avg_age = cur.fetchone()['avg_age'] or 0
    
    db_close(conn, cur)
    
    return jsonify({
        'result': {
            'total_users': total,
            'male_users': male,
            'female_users': female,
            'avg_age': round(float(avg_age), 1)
        }
    })