from flask import Blueprint, request, render_template, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path 
lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    username = session.get('username', 'anonymous')
    return render_template('lab5/lab5.html', login=session.get('login'))

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':

        conn = psycopg2.connect(
            host='localhost', 
            database='julia_nichi_knowledge_base',  
            user='julia_nichi_knowledge_base', 
            password='251789'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
        return conn, cur
    else:
 
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  
        cur = conn.cursor()
        return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    real_name = request.form.get('real_name')

    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля')
    
    conn, cur = db_connect()  

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Такой пользователь уже существует')
    
    hashed_password = generate_password_hash(password)
    if current_app.config['DB_TYPE'] == 'postgres': 
        cur.execute("INSERT INTO users (login, password, real_name) VALUES (%s, %s, %s);", (login, hashed_password, real_name))  
    else:
        cur.execute("INSERT INTO users (login, password, real_name) VALUES (?, ?, ?);", (login, hashed_password, real_name))

    conn.commit()  
    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)
    
@lab5.route('/lab5/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/login.html', error="Заполните поля")
    
    conn, cur = db_connect() 

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))

    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны!')
        
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны!')
        
    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5')

@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    if request.method == 'GET':
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT login, real_name FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT login, real_name FROM users WHERE login=?;", (login,))
        
        user = cur.fetchone()
        db_close(conn, cur)
        return render_template('lab5/profile.html', user=user)

    new_real_name = request.form.get('real_name')
    new_password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if new_password and new_password != confirm_password:
        db_close(conn, cur)
        return render_template('lab5/profile.html', user={'login': login, 'real_name': new_real_name}, 
                             error='Пароли не совпадают')

    if new_real_name:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET real_name=%s WHERE login=%s;", (new_real_name, login))
        else:
            cur.execute("UPDATE users SET real_name=? WHERE login=?;", (new_real_name, login))

    if new_password:
        hashed_password = generate_password_hash(new_password)
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET password=%s WHERE login=%s;", (hashed_password, login))
        else:
            cur.execute("UPDATE users SET password=? WHERE login=?;", (hashed_password, login))

    conn.commit()
    db_close(conn, cur)
    return redirect('/lab5/profile')

@lab5.route('/lab5/users')
def users_list():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, real_name FROM users ORDER BY login;")
    else:
        cur.execute("SELECT login, real_name FROM users ORDER BY login;")
    
    users = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/users.html', users=users)


@lab5.route('/lab5/create', methods = ['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = bool(request.form.get('is_favorite'))
    is_public = bool(request.form.get('is_public'))

    if not title or not article_text:
        return render_template('lab5/create_article.html', error='Заполните тему и текст статьи')

    conn, cur = db_connect() 

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    user_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO articles (user_id, title, article_text, is_favorite, is_public) VALUES (%s, %s, %s, %s, %s);", 
               (user_id, title, article_text, is_favorite, is_public))
    else:
        cur.execute("INSERT INTO articles (user_id, title, article_text, is_favorite, is_public) VALUES (?, ?, ?, ?, ?);", 
               (user_id, title, article_text, is_favorite, is_public))
        
    conn.commit()
    db_close(conn, cur)
    return redirect('/lab5')

@lab5.route('/lab5/list')
def list_articles():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login =%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))

    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return "Пользователь не найден", 404
    
    user_id = user['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE user_id=%s ORDER BY is_favorite DESC, id DESC;", (user_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE user_id=? ORDER BY is_favorite DESC, id DESC;", (user_id,))
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles)

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT a.* FROM articles a 
            JOIN users u ON a.user_id = u.id 
            WHERE a.id=%s AND u.login=%s;
        """, (article_id, login))
    else:
        cur.execute("""
            SELECT a.* FROM articles a 
            JOIN users u ON a.user_id = u.id 
            WHERE a.id=? AND u.login=?;
        """, (article_id, login))
    
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return "Статья не найдена или у вас нет прав для редактирования", 404

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = bool(request.form.get('is_favorite'))
    is_public = bool(request.form.get('is_public'))

    if not title or not article_text:
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article, error='Заполните тему и текст статьи')

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            UPDATE articles SET title=%s, article_text=%s, is_favorite=%s, is_public=%s
            WHERE id=%s;
        """, (title, article_text, is_favorite, is_public, article_id))
    else:
        cur.execute("""
            UPDATE articles SET title=?, article_text=?, is_favorite=?, is_public=?
            WHERE id=?;
        """, (title, article_text, is_favorite, is_public, article_id))
    conn.commit()
    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/public')
def public_articles():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT a.*, u.login, u.real_name 
            FROM articles a 
            JOIN users u ON a.user_id = u.id 
            WHERE a.is_public = TRUE 
            ORDER BY a.is_favorite DESC, a.id DESC;
        """)
    else:
        cur.execute("""
            SELECT a.*, u.login, u.real_name 
            FROM articles a 
            JOIN users u ON a.user_id = u.id 
            WHERE a.is_public = TRUE 
            ORDER BY a.is_favorite DESC, a.id DESC;
        """)
        
    articles = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/public_articles.html', articles=articles)

@lab5.route('/lab5/delete/<int:article_id>')
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT a.* FROM articles a 
            JOIN users u ON a.user_id = u.id 
            WHERE a.id=%s AND u.login=%s;
        """, (article_id, login))
    else:
        cur.execute("""
            SELECT a.* FROM articles a 
            JOIN users u ON a.user_id = u.id 
            WHERE a.id=? AND u.login=?;
        """, (article_id, login))
    
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return "Статья не найдена или у вас нет прав для удаления", 404

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("DELETE FROM articles WHERE id=?;", (article_id,))
    
    conn.commit()
    db_close(conn, cur)
    return redirect('/lab5/list')