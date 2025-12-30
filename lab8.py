from flask import Blueprint, request, render_template, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path 
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    if current_user.is_authenticated:
        username = current_user.login
    else:
        username = 'anonymous'
    
    return render_template('lab8/lab8.html', username=username)

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or not password_form:
        return render_template('lab8/register.html',
                               error='Логин и пароль не могут быть пустыми')

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html',
                               error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user, remember=False)
    return redirect('/lab8/')

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    if not login_form or not password_form:
        return render_template('lab8/login.html',
                               error='Логин и пароль не могут быть пустыми')
    
    user = users.query.filter_by(login=login_form).first()

    if user and check_password_hash(user.password, password_form):
        remember = request.form.get('remember') == 'on'  
        login_user(user, remember=remember)             
        return redirect('/lab8/')
    
    return render_template('lab8/login.html',
                           error='Ошибка входа: логин и/или пароль неверны')

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    
    return render_template('lab8/articles.html', articles=user_articles)

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = request.form.get('is_favorite') == 'on'
    is_public = request.form.get('is_public') == 'on'
    likes = request.form.get('likes', 0, type=int)
    
    if not title or not article_text:
        return render_template('lab8/create_article.html',
                               error='Заголовок и текст статьи обязательны')
    
    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=article_text,
        is_favorite=is_favorite,
        is_public=is_public,
        likes=likes
    )
    
    db.session.add(new_article)
    db.session.commit()
    
    return redirect('/lab8/articles/')

@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)
    
    # Проверяем, что пользователь редактирует свою статью
    if article.login_id != current_user.id:
        return "Вы не можете редактировать чужую статью", 403
    
    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = request.form.get('is_favorite') == 'on'
    is_public = request.form.get('is_public') == 'on'
    likes = request.form.get('likes', 0, type=int)
    
    if not title or not article_text:
        return render_template('lab8/edit_article.html', 
                               article=article,
                               error='Заголовок и текст статьи обязательны')
    
    article.title = title
    article.article_text = article_text
    article.is_favorite = is_favorite
    article.is_public = is_public
    article.likes = likes
    
    db.session.commit()
    
    return redirect('/lab8/articles/')

@lab8.route('/lab8/delete/<int:article_id>')
@login_required
def delete_article(article_id):
    article = articles.query.get_or_404(article_id)

    if article.login_id != current_user.id:
        return "Вы не можете удалить чужую статью", 403
    
    db.session.delete(article)
    db.session.commit()
    
    return redirect('/lab8/articles/')

@lab8.route('/lab8/public_articles')
def public_articles():
    public_articles_list = articles.query.filter_by(is_public=True).all()
    
    return render_template('lab8/public_articles.html', 
                          articles=public_articles_list,
                          current_user=current_user)