from flask import Flask, url_for, request, redirect, make_response, abort
import datetime
from lab1 import lab1  
from lab2 import lab2  

app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)

log_404 = []

def render_404_html(requested_url, client_ip, access_time):
    css_url = url_for("static", filename="lab1.css")
    img_url = url_for("static", filename="sadcat.jpeg")

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

@app.errorhandler(400)
def error_400(e):
    return "400 — Bad Request (Неверный запрос)", 400

@app.errorhandler(401)
def error_401(e):
    return "401 — Unauthorized (Неавторизован)", 401

@app.errorhandler(403)
def error_403(e):
    return "403 — Forbidden (Доступ запрещён)", 403

@app.errorhandler(405)
def error_405(e):
    return "405 — Method Not Allowed (Метод не разрешён)", 405

@app.errorhandler(500)
def error_500(e):
    css_url = url_for("static", filename="lab1.css")
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
@app.route("/index")
def index():
    css_url = url_for("static", filename="lab1.css")
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
            <!-- Лабораторная 1 -->
            <li><a href="{url_for('lab1.lab1_index')}">Лабораторная №1</a></li>
            <!-- Лабораторная 2 -->
            <li><a href="{url_for('lab2.lab22')}">Лабораторная №2</a></li>
        </ul>
    </nav>
    <footer>
        Ничипоренко Юлия Николаевна, ФБИ-33, 3 курс, 2025 год
    </footer>
</body>
</html>"""
    return html