from flask import Blueprint, request, render_template, redirect, session 
import psycopg2
lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    username = session.get('username', 'anonymous')
    return render_template('lab5/lab5.html', username=username)

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля')
    
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='julia_nichi_knowledge_base',
            user='julia_nichi_knowledge_base', 
            password='251789',
            client_encoding='utf8'
        )
        cur = conn.cursor()  

        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
        if cur.fetchone():
            cur.close()
            conn.close()
            return render_template('lab5/register.html', error='Такой пользователь уже существует')
        
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password))  
        conn.commit()  
        cur.close()
        conn.close()
        return render_template('lab5/success.html', login=login)
    
    except Exception as e:
        return render_template('lab5/register.html', error=f'Ошибка БД: {str(e)}')
    