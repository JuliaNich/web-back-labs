import random
import json
from flask import Blueprint, render_template, request, jsonify, session
from db import db
from db.models import gifts

lab9 = Blueprint('lab9', __name__)

CONGRATULATIONS = [
    "С Новым годом!",
    "Счастья и здоровья!",
    "Успехов в новом году!",
    "Пусть сбудутся мечты!",
    "Тепла и уюта!",
    "Радости каждый день!",
    "Удачи во всех делах!",
    "Хорошего настроения!",
    "Мира и добра!",
    "Исполнения желаний!"
]

@lab9.route('/lab9/')
@lab9.route('/lab9/main')
def main():
    return render_template('lab9/index.html')

@lab9.route('/lab9/api/gifts')
def api_gifts():
    try:
        gifts_list = gifts.query.filter_by(user_id=None).all()

        if not gifts_list:
            for i in range(10):
                pos = {
                    'top': random.randint(10, 70),
                    'left': random.randint(5, 85)
                }
                db.session.add(gifts(
                    user_id=None,
                    gift_number=i + 1,
                    is_opened=False,
                    position_data=json.dumps(pos)
                ))
            db.session.commit()
            gifts_list = gifts.query.filter_by(user_id=None).all()

        opened_count = session.get('opened_count', 0)

        opened_in_db = sum(1 for g in gifts_list if g.is_opened)

        if opened_in_db == 0:
            session['opened_count'] = 0

        return jsonify({
            'success': True,
            'gifts': [
                {
                    'number': g.gift_number,
                    'opened': g.is_opened,
                    **json.loads(g.position_data)
                } for g in gifts_list
            ],
            'opened_count': opened_count,
            'remaining': 10 - sum(g.is_opened for g in gifts_list)
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@lab9.route('/lab9/api/open', methods=['POST'])
def api_open():
    try:
        if session.get('opened_count', 0) >= 3:
            return jsonify({'success': False, 'error': 'Можно открыть не более 3 коробок'})

        data = request.get_json()
        number = data.get('number')

        gift = gifts.query.filter_by(
            user_id=None,
            gift_number=number
        ).first()

        if gift.is_opened:
            return jsonify({'success': False, 'error': 'Коробка уже пустая'})

        gift.is_opened = True
        session['opened_count'] = session.get('opened_count', 0) + 1
        db.session.commit()

        return jsonify({
            'success': True,
            'message': CONGRATULATIONS[number - 1],
            'remaining': 10 - session['opened_count']
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
