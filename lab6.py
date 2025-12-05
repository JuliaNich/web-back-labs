from flask import Blueprint, render_template, request, session
import os
import sqlite3

lab6 = Blueprint('lab6', __name__)

def get_db_type():
    db_type = os.environ.get('FLASK_DB_TYPE', 'sqlite')
    return db_type

def get_offices_from_db():
    db_type = get_db_type()
    
    if db_type == 'postgres':
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            conn = psycopg2.connect(
                host='localhost',
                database='julia_nichi_knowledge_base',
                user='julia_nichi_knowledge_base',
                password='251789'
            )
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT number, tenant, price FROM offices ORDER BY number")
            offices = cur.fetchall()
            conn.close()
            return offices
        except Exception as e:
            print(f"PostgreSQL ошибка: {e}")
            db_type = 'sqlite'
    
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'database.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT number, tenant, price FROM offices ORDER BY number")
        offices = cur.fetchall()
        conn.close()
        offices = [dict(row) for row in offices]
        return offices
    except Exception as e:
        print(f"SQLite ошибка: {e}")
        return []

def update_office_in_db(office_number, tenant):
    db_type = get_db_type()
    
    if db_type == 'postgres':
        try:
            import psycopg2
            conn = psycopg2.connect(
                host='localhost',
                database='julia_nichi_knowledge_base',
                user='julia_nichi_knowledge_base',
                password='251789'
            )
            cur = conn.cursor()
            cur.execute("UPDATE offices SET tenant = %s WHERE number = %s", 
                       (tenant, office_number))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"PostgreSQL update ошибка: {e}")
            return False
    
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'database.db')
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("UPDATE offices SET tenant = ? WHERE number = ?", 
                   (tenant, office_number))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"SQLite update ошибка: {e}")
        return False

@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data.get('id', 1)
    
    if data['method'] == 'info':
        offices = get_offices_from_db()
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }
    
    elif data['method'] == 'booking':
        login = session.get('login')
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {'code': 1, 'message': 'Unauthorized'},
                'id': id
            }

        office_number = data['params']
        offices = get_offices_from_db()
        
        for office in offices:
            if office['number'] == office_number:
                if office['tenant']:
                    return {
                        'jsonrpc': '2.0',
                        'error': {'code': 2, 'message': 'Офис уже арендуется'},
                        'id': id
                    }
                if update_office_in_db(office_number, login):
                    return {
                        'jsonrpc': '2.0',
                        'result': 'success',
                        'id': id
                    }
                else:
                    return {
                        'jsonrpc': '2.0',
                        'error': {'code': 5, 'message': 'Ошибка базы данных'},
                        'id': id
                    }
    
    elif data['method'] == 'cancellation':
        login = session.get('login')
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {'code': 1, 'message': 'Unauthorized'},
                'id': id
            }
        
        office_number = data['params']
        offices = get_offices_from_db()
        
        for office in offices:
            if office['number'] == office_number:
                if not office['tenant']:
                    return {
                        'jsonrpc': '2.0',
                        'error': {'code': 3, 'message': 'Офис не арендован'},
                        'id': id
                    }
                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {'code': 4, 'message': 'Нельзя снять чужую аренду'},
                        'id': id
                    }
                if update_office_in_db(office_number, ""):
                    return {
                        'jsonrpc': '2.0',
                        'result': 'success',
                        'id': id
                    }
                else:
                    return {
                        'jsonrpc': '2.0',
                        'error': {'code': 5, 'message': 'Ошибка базы данных'},
                        'id': id
                    }
    
    return {
        'jsonrpc': '2.0',
        'error': {'code': -32601, 'message': 'Method not found'},
        'id': id
    }