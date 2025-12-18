from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
import sqlite3
import os

lab7 = Blueprint('lab7', __name__)

DB_PATH = os.path.join(os.path.dirname(__file__), 'film.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_films():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, title_ru, year, description FROM films ORDER BY id")
    films = cursor.fetchall()
    conn.close()
    return [dict(film) for film in films]

def get_film_by_id(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = ?", (id,))
    film = cursor.fetchone()
    conn.close()
    return dict(film) if film else None

def save_film_to_db(film_data):  
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO films (title, title_ru, year, description) VALUES (?, ?, ?, ?)",
        (film_data['title'], film_data['title_ru'], film_data['year'], film_data['description'])
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def update_film_in_db(id, film_data):  
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE films SET title = ?, title_ru = ?, year = ?, description = ? WHERE id = ?",
        (film_data['title'], film_data['title_ru'], film_data['year'], film_data['description'], id)
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def delete_film_from_db(id):  
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM films WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def validate_film_data(data):
    current_year = datetime.now().year
    errors = {}
    
    if 'title_ru' not in data or not data['title_ru'].strip():
        errors['title_ru'] = "Заполните русское название"
    
    if 'year' not in data:
        errors['year'] = "Укажите год выпуска"
    else:
        try:
            year = int(data['year'])
            if year < 1895 or year > current_year:
                errors['year'] = f"Год должен быть от 1895 до {current_year}"
        except ValueError:
            errors['year'] = "Год должен быть числом"
    
    if 'description' not in data or not data['description'].strip():
        errors['description'] = "Заполните описание"
    elif len(data['description']) > 2000:
        errors['description'] = "Описание не должно превышать 2000 символов"
    
    return errors

@lab7.route('/lab7/')
def lab():
    return render_template('lab7/index.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    films = get_all_films()
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    film = get_film_by_id(id)
    if not film:
        return jsonify({"error": "Фильм не найден"}), 404
    return jsonify(film)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    film = get_film_by_id(id)
    if not film:
        return jsonify({"error": "Фильм не найден"}), 404
    
    if delete_film_from_db(id):
        return '', 204
    return jsonify({"error": "Ошибка при удалении"}), 500

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = get_film_by_id(id)
    if not film:
        return jsonify({"error": "Фильм не найден"}), 404
    
    data = request.get_json()
    
    errors = validate_film_data(data)
    if errors:
        return jsonify(errors), 400
    
    title = data.get('title', '').strip()
    if not title:
        title = data['title_ru'].strip()
    
    film_data = {
        'title': title,
        'title_ru': data['title_ru'].strip(),
        'year': int(data['year']),
        'description': data['description'].strip()
    }
    
    if update_film_in_db(id, film_data):
        updated_film = get_film_by_id(id)
        return jsonify(updated_film)
    return jsonify({"error": "Ошибка при обновлении"}), 500

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    data = request.get_json()
    
    errors = validate_film_data(data)
    if errors:
        return jsonify(errors), 400
    
    title = data.get('title', '').strip()
    if not title:
        title = data['title_ru'].strip()
    
    film_data = {
        'title': title,
        'title_ru': data['title_ru'].strip(),
        'year': int(data['year']),
        'description': data['description'].strip()
    }
    
    new_id = save_film_to_db(film_data)  
    if new_id:
        return jsonify({
            "id": new_id,
            "message": "Фильм добавлен"
        }), 201
    
    return jsonify({"error": "Ошибка при добавлении"}), 500