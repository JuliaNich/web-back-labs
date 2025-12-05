import os
from flask import Flask, url_for, request, redirect, make_response, abort
import datetime
from lab1 import lab1  
from lab2 import lab2  
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "секретно-секретный секрет")
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)

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
            <li><a href="{url_for('lab1.lab1_index')}">Лабораторная №1</a></li>
            <li><a href="{url_for('lab2.lab22')}">Лабораторная №2</a></li>
            <li><a href="{url_for('lab3.lab')}">Лабораторная №3</a></li>
            <li><a href="{url_for('lab4.lab')}">Лабораторная №4</a></li>
            <li><a href="{url_for('lab5.lab')}">Лабораторная №5</a></li>
            <li><a href="{url_for('lab6.lab')}">Лабораторная №6</a></li>
        </ul>
    </nav>
    <footer>
        Ничипоренко Юлия Николаевна, ФБИ-33, 3 курс, 2025 год
    </footer>
</body>
</html>"""
    return html