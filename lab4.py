from flask import Blueprint, request, render_template, redirect, session 
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    
    if x2 == 0:
        return render_template('lab4/div.html', error='Деление на ноль невозможно!')
    
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '':
        x1 = 0
    else:
        x1 = int(x1)
    
    if x2 == '':
        x2 = 0
    else:
        x2 = int(x2)
    
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '':
        x1 = 1
    else:
        x1 = int(x1)
    
    if x2 == '':
        x2 = 1
    else:
        x2 = int(x2)
    
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def pow():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    
    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='Оба поля не могут быть равны нулю!')
    
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)

tree_count = 0

@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)   

    operation = request.form.get('operation')

    if operation == 'cut':
        if tree_count > 0:
            tree_count -= 1

    elif operation == 'plant':
        if tree_count < 7:
            tree_count += 1
    
    return redirect('/lab4/tree')

users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр Петров', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Боб Джонсон', 'gender': 'male'},
    {'login': 'julia', 'password': '251', 'name': 'Юлия Смирнова', 'gender': 'female'},
    {'login': 'elena', 'password': '281', 'name': 'Елена Иванова', 'gender': 'female'}
]

@lab4.route('/lab4/login', methods=['POST', 'GET'])
def login(): 
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            user_name = ''
            for user in users:
                if user['login'] == session['login']:
                    user_name = user['name']
                    break
            return render_template("lab4/login.html", authorized=authorized, login=session['login'], name=user_name)
        else:
            authorized = False
            login = ''
            return render_template("lab4/login.html", authorized=authorized, login=login)
    
    login = request.form.get('login')
    password = request.form.get('password')

    errors = []
    if not login:
        errors.append('Не введён логин')
    if not password:
        errors.append('Не введён пароль')
    
    if errors:
        return render_template("lab4/login.html", errors=errors, login=login, authorized=False)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            session['name'] = user['name']
            return redirect('/lab4/login')
    
    error = 'Неверные логин и/или пароль'
    return render_template("lab4/login.html", error=error, login=login, authorized=False)

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    session.pop('name', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'GET':
        return render_template('/lab4/fridge.html')
    
    temperature = request.form.get('temperature')
    
    if not temperature:
        return render_template('/lab4/fridge.html', error='Ошибка: не задана температура')
    
    try:
        temp = int(temperature)
    except ValueError:
        return render_template('/lab4/fridge.html', error='Ошибка: температура должна быть числом')
    
    if temp < -12:
        return render_template('/lab4/fridge.html', error='Не удалось установить температуру — слишком низкое значение')
    elif temp > -1:
        return render_template('/lab4/fridge.html', error='Не удалось установить температуру — слишком высокое значение')
    elif -12 <= temp <= -9:
        snowflakes = '❄️❄️❄️'
        return render_template('/lab4/fridge.html', success=f'Установлена температура: {temp}°C', snowflakes=snowflakes)
    elif -8 <= temp <= -5:
        snowflakes = '❄️❄️'
        return render_template('/lab4/fridge.html', success=f'Установлена температура: {temp}°C', snowflakes=snowflakes)
    elif -4 <= temp <= -1:
        snowflakes = '❄️'
        return render_template('/lab4/fridge.html', success=f'Установлена температура: {temp}°C', snowflakes=snowflakes)
    
@lab4.route('/lab4/grain_order', methods=['GET', 'POST'])
def grain_order():
    if request.method == 'GET':
        return render_template('lab4/grain_order.html')
    
    grain_type = request.form.get('grain_type')
    weight = request.form.get('weight')

    prices = {
        'barley': 12000,  
        'oats': 8500,     
        'wheat': 9000,    
        'rye': 15000      
    }
    
    grain_names = {
        'barley': 'ячмень',
        'oats': 'овёс', 
        'wheat': 'пшеница',
        'rye': 'рожь'
    }

    if not weight:
        return render_template('lab4/grain_order.html', error='Ошибка: не указан вес')
    
    try:
        weight_float = float(weight)
    except ValueError:
        return render_template('lab4/grain_order.html', error='Ошибка: вес должен быть числом')
    
    if weight_float <= 0:
        return render_template('lab4/grain_order.html', error='Ошибка: вес должен быть положительным числом')
    
    if weight_float > 100:
        return render_template('lab4/grain_order.html', error='Извините, такого объёма сейчас нет в наличии')

    price_per_ton = prices.get(grain_type)
    if not price_per_ton:
        return render_template('lab4/grain_order.html', error='Ошибка: не выбран тип зерна')
    
    total = weight_float * price_per_ton
    
    discount_applied = False
    discount_amount = 0
    
    if weight_float > 10:
        discount_amount = total * 0.1
        total -= discount_amount
        discount_applied = True
    
    grain_name = grain_names.get(grain_type)
    
    return render_template('lab4/grain_order.html', 
                         success=True,
                         grain_name=grain_name,
                         weight=weight_float,
                         total=total,
                         discount_applied=discount_applied,
                         discount_amount=discount_amount)