from flask import Blueprint, request, render_template, make_response, redirect

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name', 'Аноним')
    age = request.cookies.get('age', 'неизвестен')
    name_color = request.cookies.get('name_color', 'grey')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3. route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    # Пусть кофе стоит 120 рублей, чёрный чай - 80 рублей, зелёный - 70 рублей.
    if drink == ' cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else: price = 70 # Добавка молока удорожает напиток на 30 рублей, а сахара - на 10.
    if request.args.get ('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
    return render_template ('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')
    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bgcolor = request.args.get('bgcolor')
    fontsize = request.args.get('fontsize')
    fontstyle = request.args.get('fontstyle')

    if color or bgcolor or fontsize or fontstyle:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bgcolor:
            resp.set_cookie('bgcolor', bgcolor)
        if fontsize:
            resp.set_cookie('fontsize', fontsize)
        if fontstyle:
            resp.set_cookie('fontstyle', fontstyle)
        return resp

    color = request.cookies.get('color', '#000000')
    bgcolor = request.cookies.get('bgcolor', '#ffffff')
    fontsize = request.cookies.get('fontsize', '16')
    fontstyle = request.cookies.get('fontstyle', 'normal')

    resp = make_response(render_template(
        'lab3/settings.html',
        color=color,
        bgcolor=bgcolor,
        fontsize=fontsize,
        fontstyle=fontstyle
    ))
    return resp

@lab3.route('/lab3/train', methods=['GET', 'POST'])
def train():
    errors = {}
    if request.method == 'POST':
        fio = request.form.get('fio')
        shelf = request.form.get('shelf')
        linen = request.form.get('linen')
        baggage = request.form.get('baggage')
        age = request.form.get('age')
        start = request.form.get('start')
        end = request.form.get('end')
        date = request.form.get('date')
        insurance = request.form.get('insurance')

        if not all([fio, shelf, age, start, end, date]):
            errors['form'] = 'Заполните все обязательные поля!'
        else:
            try:
                age = int(age)
                if not (1 <= age <= 120):
                    errors['age'] = 'Возраст должен быть от 1 до 120!'
            except ValueError:
                errors['age'] = 'Возраст должен быть числом!'

        if not errors:
            if age < 18:
                price = 700
                ticket_type = 'Детский билет'
            else:
                price = 1000
                ticket_type = 'Взрослый билет'

            if shelf in ['нижняя', 'нижняя боковая']:
                price += 100
            if linen == 'on':
                price += 75
            if baggage == 'on':
                price += 250
            if insurance == 'on':
                price += 150

            return render_template('lab3/train_ticket.html',
                                   fio=fio, shelf=shelf, start=start, end=end,
                                   date=date, age=age, price=price,
                                   ticket_type=ticket_type)

    return render_template('lab3/train_form.html', errors=errors)

