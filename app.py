import os
from os import path
from flask import Flask, url_for, request, redirect, make_response, abort, send_from_directory
import datetime
from db import db
from db.models import users
from flask_login import LoginManager

app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "super-secret-key-12345")
app.config['DB_TYPE'] = os.environ.get('DB_TYPE', 'postgres')  

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'julia_nichiporenko_orm'
    db_user = 'julia_nichiporenko_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'

else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "julia_nichiporenko_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

from lab1 import lab1  
from lab2 import lab2  
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from rgz import rgz
from lab8 import lab8
from lab9 import lab9

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(rgz, url_prefix='/rgz')
app.register_blueprint(lab8)
app.register_blueprint(lab9)

log_404 = []

def render_404_html(requested_url, client_ip, access_time):
    css_url = url_for("static", filename="lab1/lab1.css")
    img_url = url_for("static", filename="lab1/sadcat.jpeg")

    html = f"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>404 — Страница не найдена</title>
    <link rel="stylesheet" href="{css_url}">
  </head>
  <body class="page-bg">
    <div class="center-box">
      <h1>404 — Такой страницы нет, котик грустит </h1>
      <p>Мы не нашли страницу: <b>{requested_url}</b></p>
      <img src="{img_url}" alt="sad cat" class="small-image">
      <p>Ваш IP: <b>{client_ip}</b></p>
      <p>Дата и время доступа: <b>{access_time}</b></p>
      <p><a href="{url_for('index')}">Вернуться на главную</a></p>
    </div>

    <hr>
    <h2>Журнал 404 (последние 10 записей)</h2>
    <ul>
"""
    for entry in log_404[-10:]:
        html += f"<li>{entry}</li>"
    html += "</ul></body></html>"
    return html


@app.errorhandler(404)
def handle_404(err):
    client_ip = request.remote_addr
    access_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url
    log_404.append(f"[{access_time}] пользователь {client_ip} зашёл на адрес: {requested_url}")
    html = render_404_html(requested_url, client_ip, access_time)
    resp = make_response(html, 404)
    resp.headers['Content-Type'] = 'text/html; charset=utf-8'
    return resp



@app.errorhandler(500)
def error_500(e):
    css_url = url_for("static", filename="lab1/lab1.css")
    html = f"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>500 — Внутренняя ошибка сервера</title>
    <link rel="stylesheet" href="{css_url}">
  </head>
  <body>
    <h1>500 — Внутренняя ошибка сервера</h1>
    <p>Произошла ошибка на сервере. Попробуйте повторить позже.</p>
    <p><a href="/">Вернуться на главную</a></p>
  </body>
</html>"""
    return html, 500


@app.route("/")
def index():
    css_url = url_for("static", filename="lab1/lab1.css")

    links = []

    blueprints_to_check = [
        ('lab1', 'Лабораторная №1', 'lab1.lab1_index'),
        ('lab2', 'Лабораторная №2', 'lab2.lab22'),
        ('lab3', 'Лабораторная №3', 'lab3.lab'),
        ('lab4', 'Лабораторная №4', 'lab4.lab'),
        ('lab5', 'Лабораторная №5', 'lab5.lab'),
        ('lab6', 'Лабораторная №6', 'lab6.lab'),
        ('lab7', 'Лабораторная №7', 'lab7.lab'),
        ('lab8', 'Лабораторная №8', 'lab8.lab'),
        ('lab9', 'Лабораторная №9', 'lab9.main'),
    ]
    
    for bp_name, bp_text, endpoint in blueprints_to_check:
        if bp_name in app.blueprints:
            links.append(f'<li><a href="{url_for(endpoint)}">{bp_text}</a></li>')

    if 'rgz' in app.blueprints:
        links.append(f'<li><a href="{url_for("rgz.index")}">РГЗ (Сайт знакомств)</a></li>')
    
    links_html = '\n'.join(links) if links else '<li>Нет доступных лабораторных работ</li>'
    
    html = f"""<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>НГТУ, ФБ, Лабораторные работы</title>
    <link rel="stylesheet" href="{css_url}">
</head>
<body>
    <h1>НГТУ, ФБ — WEB-программирование, часть 2. Список лабораторных</h1>
    <nav>
        <ul>
            {links_html}
        </ul>
    </nav>
    <footer>
        Ничипоренко Юлия Николаевна, ФБИ-33, 3 курс, 2025 год
    </footer>
</body>
</html>"""
    
    return html

