from flask import Flask, url_for, request, redirect, make_response, abort
import datetime

app = Flask(__name__)


log_404 = []
count = 0


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
      <h1>404 — Такой страницы нет, котик грустит</h1>
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
    html += """
    </ul>
  </body>
</html>
"""
    return html


@app.route("/lab1/404")
def page_404():
    client_ip = request.remote_addr
    access_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url
    log_404.append(f"[{access_time}] пользователь {client_ip} зашёл на адрес: {requested_url}")
    html = render_404_html(requested_url, client_ip, access_time)
    resp = make_response(html, 404)
    resp.headers['Content-Type'] = 'text/html; charset=utf-8'
    return resp


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
</html>
"""
    return html, 500


@app.route("/lab1/402")
def route_402():
    return "402 — Payment Required (Требуется оплата)", 402

@app.route("/lab1/418")
def route_418():
    return "418 — I'm a teapot (Я — чайник)", 418


@app.route("/lab1/error")
def trigger_error():
    1 / 0
    return "не будет"


@app.route("/lab1/web")
def web():
    css_url = url_for("static", filename="lab1.css")
    html = f"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Lab1 — Web</title>
    <link rel="stylesheet" href="{css_url}">
  </head>
  <body>
    <h1>web-сервер на Flask</h1>
    <p><a href="{url_for('author')}">author</a></p>
  </body>
</html>
"""
    resp = make_response(html, 200)
    resp.headers['Content-Type'] = 'text/html; charset=utf-8'
    resp.headers['X-server'] = 'sample'
    return resp


@app.route("/lab1/author")
def author():
    name = 'Ничипоренко Юлия Николаевна'
    group = 'ФБИ-33'
    faculty = 'ФБ'
    css_url = url_for("static", filename="lab1.css")
    html = f"""<!doctype html>
<html>
  <head><meta charset="utf-8"><title>Автор</title>
  <link rel="stylesheet" href="{css_url}">
  </head>
  <body>
    <h1>Информация об авторе</h1>
    <p><b>Студент:</b> {name}</p>
    <p><b>Группа:</b> {group}</p>
    <p><b>Факультет:</b> {faculty}</p>
    <p><a href="{url_for('web')}">Перейти к /lab1/web</a></p>
  </body>
</html>
"""
    resp = make_response(html)
    resp.headers['Content-Type'] = 'text/html; charset=utf-8'
    return resp


@app.route("/lab1/image")
def image():
    img_url = url_for('static', filename='oak.jpeg')
    css_url = url_for('static', filename='lab1.css')
    html = f"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Картинка — Дуб</title>
    <link rel="stylesheet" href="{css_url}">
  </head>
  <body>
    <h1>Дуб</h1>
    <img src="{img_url}" alt="oak" class="small-image">
    <p><a href="{url_for('lab1')}">Вернуться в меню лабораторной</a></p>
  </body>
</html>
"""
    resp = make_response(html, 200)
    resp.headers['Content-Language'] = 'ru-RU'
    resp.headers['X-Student'] = 'Julia'
    resp.headers['X-Lab'] = 'Lab1'
    resp.headers['Content-Type'] = 'text/html; charset=utf-8'
    return resp


@app.route("/lab1/counter")
def counter():
    global count
    count += 1
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url = request.url
    client_ip = request.remote_addr
    css_url = url_for("static", filename="lab1.css")
    html = f"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Счётчик</title>
    <link rel="stylesheet" href="{css_url}">
  </head>
  <body>
    <h1>Счётчик посещений</h1>
    <p>Сколько раз вы заходили на эту страницу: <b>{count}</b></p>
    <p>Дата и время: {time_now}</p>
    <p>Запрошенный адрес: {url}</p>
    <p>Ваш IP-адрес: {client_ip}</p>
    <p><a href="{url_for('reset_counter')}">Сбросить счётчик</a></p>
  </body>
</html>
"""
    resp = make_response(html)
    resp.headers['Content-Type'] = 'text/html; charset=utf-8'
    return resp


@app.route("/lab1/reset_counter")
def reset_counter():
    global count
    count = 0
    return redirect(url_for('counter'))


@app.route("/lab1/info")
def info():
    return redirect(url_for('author'))


@app.route("/lab1/created")
def created():
    css_url = url_for("static", filename="lab1.css")
    html = f"""<!doctype html>
<html>
  <head><meta charset="utf-8"><title>Created</title>
  <link rel="stylesheet" href="{css_url}">
  </head>
  <body>
    <h1>Создано успешно</h1>
    <div><i>что-то создано...</i></div>
  </body>
</html>
"""
    return html, 201


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
        <li><a href="{url_for('lab1')}">Первая лабораторная</a></li>
      </ul>
    </nav>
    <footer>
      Ничипоренко Юлия Николаевна, ФБИ-33, 3 курс, 2025 год
    </footer>
  </body>
</html>
"""
    resp = make_response(html)
    resp.headers['Content-Type'] = 'text/html; charset=utf-8'
    return resp

@app.route("/lab1")
def lab1():
    css_url = url_for("static", filename="lab1.css")
    html = f"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Лабораторная 1</title>
    <link rel="stylesheet" href="{css_url}">
  </head>
  <body>
    <h1>Лабораторная 1</h1>
    <p>
      Flask — фреймворк для создания веб-приложений на языке Python, 
      использующий инструменты Werkzeug и шаблонизатор Jinja2. 
      Flask относится к категории микрофреймворков — минималистичных каркасов веб-приложений, 
      предоставляющих базовые возможности для быстрого старта.
    </p>
    <p><a href="{url_for('index')}">Вернуться на корень сайта</a></p>

    <h2>Список роутов</h2>
    <ul>
      <li><a href="{url_for('web')}">/lab1/web</a></li>
      <li><a href="{url_for('author')}">/lab1/author</a></li>
      <li><a href="{url_for('image')}">/lab1/image</a></li>
      <li><a href="{url_for('counter')}">/lab1/counter</a></li>
      <li><a href="{url_for('info')}">/lab1/info</a></li>
      <li><a href="{url_for('reset_counter')}">/lab1/reset_counter</a></li>
      <li><a href="{url_for('created')}">/lab1/created</a></li>
      <li><a href="{url_for('page_404')}">/lab1/404</a> (тест 404)</li>
      <li><a href="{url_for('route_402')}">/lab1/402</a></li>
      <li><a href="{url_for('route_418')}">/lab1/418</a></li>
      <li><a href="{url_for('trigger_error')}">/lab1/error</a> (тест 500)</li>
    </ul>
  </body>
</html>
"""
    resp = make_response(html)
    resp.headers['Content-Type'] = 'text/html; charset=utf-8'
    return resp


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = ['колокольчик', 'хризантема', 'роза', 'пион']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return 'цветок: ' + flower_list[flower_id]
    

    

