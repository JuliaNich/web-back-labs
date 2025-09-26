from flask import Flask, url_for, request, redirect, make_response, send_from_directory
import datetime, os
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    return """
<!doctype html>
<html>
   <head>
      <style>
         body { background-color: #fce4ec; color: #880e4f; text-align: center; }
         img { width: 300px; margin-top: 20px; }
      </style>
   </head>
   <body>
      <h1>Такой страницы нет</h1>
      <p>Похоже из-за вашей проблемы расстроился котик(</p>
      <img src='/static/sadcat.jpeg'>
   </body>
</html>
""", 404


@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href='/lab1/author'>author</a>
           </body>
        </html>""", 200, {
            'X-server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
            }

@app.route("/lab1/author")
def author():
    name = 'Ничипоренко Юлия Николаевна'
    group = 'ФБИ-33'
    faculty = 'ФБ'

    return """<!doctype html>
        <html>
           <body>
               <p>Студент: """ + name + """</p>
               <p>Группа: """ + group + """</p>
               <p>Факультет: """ + faculty + """</p>
               <a href='/lab1/web'>web</a>
           </body>
        </html>"""

from flask import Flask, url_for, make_response

app = Flask(__name__)

@app.route("/lab1/image")
def image():
    path = url_for('static', filename='oak.jpeg')
    css = url_for('static', filename='lab1.css')
    html = f"""
<!doctype html>
<html>
   <head>
      <link rel='stylesheet' href='{css}'>
   </head>
   <body>
      <h1>Дуб</h1>
      <img src='{path}'>
   </body>
</html>
"""
    return html, 200, {
        "Content-Language": "ru",
        "X-Student": "Юлия",
        "X-Lab": "Lab1"
    }


@app.route("/lab1/counter")
def counter():
    global count
    count = 0
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return '''
<!doctype html>
<html>
   <body>
      Сколько раз вы сюда заходили ''' + str(count) + '''
      <hr>
      Дата и время: ''' + str(time) + '''<br>
      Запрошенный адрес: ''' + url + '''<br>
      Ваш IP-адрес: ''' + client_ip + '''<br>
      <a href='/lab1/reset_counter'>Сбросить счётчик</a>
  </body>
</html>
'''

@app.route("/lab1/reset_counter")
def reset_counter():
    global count
    count = 0
    return redirect("/lab1/counter")

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
   <body>
      <h1>Создано успешно</h1>
      <div><i>что-то создано...</i></div>
  </body>
</html>
''', 201

@app.route("/")
@app.route("/index")
def index():
    return """
<!doctype html>
<html>
   <head>
      <title>НГТУ, ФБ, Лабораторные работы</title>
   </head>
   <body>
      <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
      <ul>
         <li><a href='/lab1'>Первая лабораторная</a></li>
      </ul>
      <hr>
      <footer>
         Ничипоренко Юлия Николаевна, ФБИ-33, 3 курс, 2025 год
      </footer>
   </body>
</html>
"""
@app.route("/lab1")
def lab1():
    return """
<!doctype html>
<html>
   <head>
      <title>Лабораторная 1</title>
   </head>
   <body>
      Flask — фреймворк для создания веб-приложений на языке
      программирования Python, использующий набор инструментов
      Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
      называемых микрофреймворков — минималистичных каркасов
      веб-приложений, сознательно предоставляющих лишь самые 
      базовые возможности.
      <br><br>
      <a href='/'>На главную</a>
      <h2>Список роутов</h2>
      <ul>
         <li><a href='/lab1/web'>/lab1/web</a></li>
         <li><a href='/lab1/author'>/lab1/author</a></li>
         <li><a href='/lab1/image'>/lab1/image</a></li>
         <li><a href='/lab1/counter'>/lab1/counter</a></li>
         <li><a href='/lab1/info'>/lab1/info</a></li>
         <li><a href='/lab1/reset_counter'>/lab1/reset_counter</a></li>
         <li><a href='/lab1/error'>/lab1/error</a></li>
      </ul>
   </body>
</html>
"""
@app.errorhandler(400)
def error_400(e):
    return "Ошибка 400 — Неверный запрос", 400

@app.errorhandler(401)
def error_401(e):
    return "Ошибка 401 — Неавторизован", 401

@app.route("/lab1/402")
def error_402():
    return "Ошибка 402 — Требуется оплата", 402

@app.errorhandler(403)
def error_403(e):
    return "Ошибка 403 — Доступ запрещён", 403

@app.errorhandler(405)
def error_405(e):
    return "Ошибка 405 — Метод не разрешён", 405

@app.route("/lab1/418")
def error_418():
    return "Ошибка 418 — Ошибка", 418

@app.route("/lab1/error")
def error():
    return 1 / 0  

@app.errorhandler(500)
def error_500(e):
    return "Ошибка 500 — внутренняя ошибка сервера", 500


