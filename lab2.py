from flask import Blueprint, url_for, request, redirect, make_response, abort, render_template
import datetime

lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/a')
def a():
    return 'без слэша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'


flower_list = [
    {"name": "роза", "price": 120},
    {"name": "пион", "price": 150},
    {"name": "тюльпан", "price": 90},
    {"name": "ромашка", "price": 60}
]


@lab2.route('/lab2/flowers/')
def flowers_all():
    return render_template('flowers.html', flowers=flower_list)


@lab2.route('/lab2/flowers/<int:flower_id>/')
def flower_info(flower_id):
    if 0 <= flower_id < len(flower_list):
        return render_template('flower_info.html', flower=flower_list[flower_id], id=flower_id)
    else:
        abort(404)


@lab2.route('/lab2/add_flower/', methods=['POST'])
def add_flower():
    name = request.form.get('name')
    price = request.form.get('price')

    if not name:
        return "Вы не задали имя цветка", 400

    try:
        price = int(price)
    except (TypeError, ValueError):
        price = 0

    flower_list.append({"name": name, "price": price})
    return redirect(url_for('flowers_all'))


@lab2.route('/lab2/delete_flower/<int:flower_id>/')
def delete_flower(flower_id):
    if 0 <= flower_id < len(flower_list):
        del flower_list[flower_id]
        return redirect(url_for('flowers_all'))
    else:
        abort(404)


@lab2.route('/lab2/clear_flowers/')
def clear_flowers():
    flower_list.clear()
    return render_template('flowers.html', flowers=flower_list, cleared=True)


if __name__ == '__main__':
    lab2.run(debug=True)


@lab2.route('/lab2/example')
def example():
    No = '2'
    name = 'Ничипоренко Юлия'
    group = 'ФБИ-33'
    number = '3 курс'
    fruits = [
        {'name':'манго', 'price': 100 }, 
        {'name':'яблоко', 'price': 55 },
        {'name':'мандарин', 'price': 85 },
        {'name':'киви', 'price': 90 },
        {'name':'апельсин', 'price': 67 },
     ]
    return render_template(
        'example.html',
        No=No,
        name=name,
        group=group,
        number=number,
        fruits=fruits
        )


@lab2.route('/lab2/')
def lab22():
    return render_template('lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)


@lab2.route('/lab2/calc/')
def calc_default_redirect():
    return redirect('/lab2/calc/1/1')


@lab2.route('/lab2/calc/<int:a>')
def calc_one_number(a):
    return redirect(f'/lab2/calc/{a}/1')


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    result = {
        'sum': a + b,
        'sub': a - b,
        'mul': a * b,
        'div': a / b if b != 0 else 'Деление на ноль!',
        'pow': a ** b
    }
    return render_template('calc.html', a=a, b=b, result=result)

books = [
    {'title': 'Мастер и Маргарита', 'author': 'М. Булгаков', 'genre': 'Роман', 'pages': 480},
    {'title': 'Преступление и наказание', 'author': 'Ф. Достоевский', 'genre': 'Роман', 'pages': 620},
    {'title': 'Война и мир', 'author': 'Л. Толстой', 'genre': 'Роман-эпопея', 'pages': 1225},
    {'title': 'Три товарища', 'author': 'Э. М. Ремарк', 'genre': 'Роман', 'pages': 480},
    {'title': '1984', 'author': 'Дж. Оруэлл', 'genre': 'Антиутопия', 'pages': 328},
    {'title': 'Гарри Поттер и философский камень', 'author': 'Дж. Роулинг', 'genre': 'Фэнтези', 'pages': 350},
    {'title': 'Убить пересмешника', 'author': 'Х. Ли', 'genre': 'Драма', 'pages': 400},
    {'title': 'Анна Каренина', 'author': 'Л. Толстой', 'genre': 'Роман', 'pages': 850},
    {'title': 'Пикник на обочине', 'author': 'Стругацкие', 'genre': 'Фантастика', 'pages': 300},
    {'title': 'Тень ветра', 'author': 'К. Сафон', 'genre': 'Мистика', 'pages': 500}
]


@lab2.route('/lab2/books/')
def show_books():
    return render_template('books.html', books=books)

cats = [
    {'name': 'Мурзик', 'desc': 'По одной из версий, прародительницу абиссинских кошек в 1868 году вывез из Абиссинии в Англию капитан Баррет-Ленард.', 'img': 'cat1.jpg'},
    {'name': 'Луна', 'desc': 'Первый котенок с такой загнутой формой ушей появился на свет в далеком 1981 голу, в Калифорнии.', 'img': 'cat2.jpg'},
    {'name': 'Малыш', 'desc': 'Балинез это по сути прекрасная сиамская кошка только с длинной шерстью. ', 'img': 'cat3.jpg'},
    {'name': 'Степаша', 'desc': 'Бенгальская порода кошек возникла в результате целенаправленного скрещивания дикого азиатского кота с домашней кошкой.', 'img': 'cat4.jpg'},
    {'name': 'Ветта', 'desc': 'Впервые Священная Бирма была представлена на выставке кошек в Париже в 1926 году, но только в 1950 году порода получила свое официальное название.', 'img': 'cat5.jpg'},
    {'name': 'Ника', 'desc': 'Британские короткошерстные кошки являются традиционной английской породой и гордостью Великобритании.', 'img': 'cat6.jpg'},
    {'name': 'Джемка', 'desc': 'Египетские мау произошли от очень древней породы кошек, представители которой жили в Древнем Египте и считались священными животными, воплощением богини Баст или Бастет.', 'img': 'cat7.jpg'},
    {'name': 'Мурка', 'desc': 'Бурманские кошки относятся к короткошерстной группе кошек. Родиной этих кошек является Юго-Восточная Азия. ', 'img': 'cat8.jpg'},
    {'name': 'Арнольд', 'desc': 'Кошки породы эльф немногочисленны, их разведением стали заниматься американские энтузиасты-заводчики в 90-х годах прошлого века. ', 'img': 'cat9.jpg'},
    {'name': 'Пушок', 'desc': 'Из-за своих крупных размеров, большого пушистого хвоста и окраса этих кошек считали похожими на енотов.', 'img': 'cat10.jpg'},
    {'name': 'Дымка', 'desc': 'Из названия породы понятно, что невская маскарадная кошка была выведена в России, в Санкт-Петербурге. Это сибирские кошки, имеющие оригинальный окрас.', 'img': 'cat11.jpg'},
    {'name': 'Тучка', 'desc': 'Согласно одной из историй возникновения данной породы кошек, прародителями лесного норвежского кота являются длинношерстные коты, завезенные викингами из Турции.', 'img': 'cat12.jpg'},
    {'name': 'Бусинка', 'desc': 'Русские голубые кошки отличаются своим изяществом и благородством внешнего вида, их мягкая короткая шерсть голубого цвета с серебристым отливом оригинально сочетается с необыкновенными зелеными глазами.', 'img': 'cat13.jpg'},
    {'name': 'Бубик', 'desc': 'Сиамская кошка настоящая королевская особа! Эти кошки действительно долгое время считались священными животными и жили исключительно в храмах или во дворцах царских семей Таиланда. .', 'img': 'cat14.jpg'},
    {'name': 'Викуся', 'desc': 'Сибирская кошка отличается своим пушистым красивым мехом. Это достаточно крупное, мощное и сильное животное.', 'img': 'cat15.jpg'},
    {'name': 'Маруся', 'desc': 'Данная порода кошек мало отличается по своим характеристикам от британской короткошерстной кошки, что вызывает горячие споры у заводчиков и владельцев этих плюшевых созданий.', 'img': 'cat16.png'},
    {'name': 'Эмка', 'desc': 'Тайские кошки относятся к древней породе кошек, упоминания о тайских кошках встречаются в рукописях 14 века, с которыми сегодня можно познакомится в Бангкоке.', 'img': 'cat17.jpg'},
    {'name': 'Рыжик', 'desc': 'Теннессийский рекс имеет средние размеры, тело мускулистое в пределах нормы, спина прямая, из – за разницы в длине задних и передних ног туловище наклонено в сторону головы. ', 'img': 'cat18.jpg'},
    {'name': 'Сэм', 'desc': 'Тонкинская кошка появилась в результате скрещивания бурманской и сиамской кошек.', 'img': 'cat19.jpg'},
    {'name': 'Симба', 'desc': 'Турецкая ангора признана практическими всеми ассоциациями, среди них CFA, WCF, TICA, FIFE и пр. Турецкой эта порода называется, так как была выведена специалистами – фелинологами из Америки и Европы на основе кошек, завезенных из Турции.', 'img': 'cat20.jpg'},
]


@lab2.route('/lab2/cats/')
def show_cats():
    return render_template('cats.html', cats=cats)
