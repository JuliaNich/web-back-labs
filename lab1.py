from flask import Blueprint, url_for, request, redirect, make_response, abort, render_template
import datetime

lab1 = Blueprint('lab1', __name__)

count = 0


@lab1.route("/lab1", endpoint='lab1_index')
def lab():
    css_url = url_for("static", filename="lab1/lab1.css")
    html = f"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Лабораторная 1</title>
    <link rel="stylesheet" href="{css_url}">
    <link rel="icon" type="image/jpeg" href="{url_for('static', filename='lab2/favicon.jpeg')}">
  </head>
  <body>
    <h1>Лабораторная работа №1</h1>
    <p>
      Flask — это микрофреймворк для создания веб-приложений на Python, 
      использующий шаблонизатор Jinja2 и библиотеку Werkzeug.
    </p>
    <p><a href="/">Вернуться на главную страницу</a></p>

    <h2>Список маршрутов:</h2>
    <ul>
      <li><a href="{url_for('lab1.web')}">/lab1/web</a></li>
      <li><a href="{url_for('lab1.author')}">/lab1/author</a></li>
      <li><a href="{url_for('lab1.image')}">/lab1/image</a></li>
      <li><a href="{url_for('lab1.counter')}">/lab1/counter</a></li>
      <li><a href="{url_for('lab1.info')}">/lab1/info</a></li>
      <li><a href="{url_for('lab1.reset_counter')}">/lab1/reset_counter</a></li>
      <li><a href="{url_for('lab1.created')}">/lab1/created</a></li>
      <li><a href="{url_for('lab1.route_402')}">/lab1/402</a></li>
      <li><a href="{url_for('lab1.route_418')}">/lab1/418</a></li>
    </ul>
  </body>
</html>
"""
    resp = make_response(html)
    resp.headers['Content-Type'] = 'text/html; charset=utf-8'
    return resp


@lab1.route("/lab1/402")
def route_402():
    return "402 — Payment Required (Требуется оплата)", 402


@lab1.route("/lab1/418")
def route_418():
    return "418 — I'm a teapot (Я — чайник)", 418


@lab1.route("/lab1/error")
def trigger_error():
    1 / 0  
    return "не будет"


@lab1.route("/lab1/web")
def web():
    css_url = url_for("static", filename="lab1/lab1.css")
    html = f"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Lab1 — Web</title>
    <link rel="stylesheet" href="{css_url}">
    <link rel="icon" type="image/jpeg" href="{url_for('static', filename='lab2/favicon.jpeg')}">
  </head>
  <body>
    <h1>Web-сервер на Flask</h1>
    <p><a href="{url_for('lab1.author')}">Информация об авторе</a></p>
    <p><a href="{url_for('lab1.lab1_index')}">Назад к лабораторной</a></p>
  </body>
</html>
"""
    resp = make_response(html, 200)
    resp.headers['X-server'] = 'Flask-demo'
    return resp


@lab1.route("/lab1/author")
def author():
    name = 'Ничипоренко Юлия Николаевна'
    group = 'ФБИ-33'
    faculty = 'ФБ'
    css_url = url_for("static", filename="lab1/lab1.css")
    html = f"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Автор</title>
    <link rel="stylesheet" href="{css_url}">
    <link rel="icon" type="image/jpeg" href="{url_for('static', filename='lab2/favicon.jpeg')}">
  </head>
  <body>
    <h1>Информация об авторе</h1>
    <p><b>Студент:</b> {name}</p>
    <p><b>Группа:</b> {group}</p>
    <p><b>Факультет:</b> {faculty}</p>
    <p><a href="{url_for('lab1.web')}">Перейти к /lab1/web</a></p>
    <p><a href="{url_for('lab1.lab1_index')}">Назад к лабораторной</a></p>
  </body>
</html>
"""
    return make_response(html)


@lab1.route("/lab1/image")
def image():
    img_url = url_for('static', filename='lab1/oak.jpeg')
    css_url = url_for('static', filename='lab1/lab1.css')
    html = f"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Картинка — Дуб</title>
    <link rel="stylesheet" href="{css_url}">
    <link rel="icon" type="image/jpeg" href="{url_for('static', filename='lab2/favicon.jpeg')}">
  </head>
  <body>
    <h1>Дуб</h1>
    <img src="{img_url}" alt="oak" class="small-image">
    <p><a href="{url_for('lab1.lab1_index')}">Вернуться к лабораторной</a></p>
  </body>
</html>
"""
    return make_response(html)


@lab1.route("/lab1/counter")
def counter():
    global count
    count += 1
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    css_url = url_for("static", filename="lab1/lab1.css")
    html = f"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Счётчик посещений</title>
    <link rel="stylesheet" href="{css_url}">
  </head>
  <body>
    <h1>Счётчик посещений</h1>
    <p>Количество посещений: <b>{count}</b></p>
    <p>Дата и время: {time_now}</p>
    <p><a href="{url_for('lab1.reset_counter')}">Сбросить счётчик</a></p>
    <p><a href="{url_for('lab1.lab1_index')}">Назад к лабораторной</a></p>
  </body>
</html>
"""
    return make_response(html)


@lab1.route("/lab1/reset_counter")
def reset_counter():
    global count
    count = 0
    return redirect(url_for('lab1.counter'))


@lab1.route("/lab1/info")
def info():
    return redirect(url_for('lab1.author'))


@lab1.route("/lab1/created")
def created():
    css_url = url_for("static", filename="lab1/lab1.css")
    html = f"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Created</title>
    <link rel="stylesheet" href="{css_url}">
  </head>
  <body>
    <h1>Создано успешно!</h1>
    <div><i>Объект создан...</i></div>
    <p><a href="{url_for('lab1.lab1_index')}">Назад к лабораторной</a></p>
  </body>
</html>
"""
    return html, 201
