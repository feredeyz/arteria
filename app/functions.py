from .models import User, Post
from . import db
from datetime import datetime
from flask import make_response, redirect, url_for, render_template
from flask_login import login_user, logout_user
from flask_jwt_extended import create_access_token
import os
from PIL import Image


def validate_login(form):
    user = User.query.filter_by(username=form.username.data).first()
    if user and user.check_password(form.password.data):
        login_user(user, remember=True)
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                'username': user.username,
                'description': user.description or ""
            }
        )
        
        response = make_response(redirect(url_for('profile.user')))
        response.set_cookie('access_token_cookie', access_token, httponly=True)
        return response
    else:
        return render_template('login.html', form=form, error='Incorrect username or password!')
    
def validate_registration(form):
    if User.query.filter_by(username=form.username.data).first():
            return render_template('registrate.html', form=form, error='Username already taken!')
    user = User(username=form.username.data, pwd=form.password.data, date=str(datetime.now())[:-7])
    db.session.add(user)
    db.session.commit()
    login_user(user, remember=True)
    access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                'username': user.username,
                'description': user.description or "",
                'avatar': user.avatar
            }
        )
    response = make_response(redirect(url_for('profile.user')))
    response.set_cookie('access_token_cookie', access_token, httponly=True)
    return response

def change_description(req):
    user = User.query.get(req.json['userId'])
    user.description = req.json['content']
    db.session.commit()
    
def change_avatar(req):
    file = req.files['image']
    id = req.form['userId']
    img = Image.open(file.stream)
    img = img.convert("RGB")
    save_path = os.path.join('app/static/avatars', f'avatar{id}.png')
    os.makedirs('app/static/avatars', exist_ok=True) 
    img.save(save_path)
    user = User.query.get(id)
    user.avatar = f'avatar{id}.png'
    db.session.commit()
    
def post_add(form, user):
    db.session.add(Post(title=form.title.data, content=form.content.data, created_at=str(datetime.now())[:-7], user_id=user.id))
    db.session.commit()