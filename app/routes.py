from flask import render_template, redirect, url_for, Blueprint, flash, request, make_response, session
from .models import User
from .forms import LoginForm, RegistrationForm
from flask_login import login_required, login_user, current_user
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required
from . import db
from datetime import datetime
from PIL import Image
import logging as log
import os

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
profile = Blueprint('profile', __name__)
cors = CORS()

@main.route('/')
def index():
    return render_template('index.html')

@auth.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
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
    return render_template('login.html', form=form)


@auth.route('/register', methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
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
    return render_template('registrate.html', form=form)

@profile.route('/confirm-description-edit', methods=["POST"])
def confirm_desc_edit():
    user = User.query.get(request.json['userId'])
    user.description = request.json['content']
    db.session.commit()
    print(User.query.get(request.json['userId']).description    )
    return redirect(url_for('profile.user'))

@profile.route('/change-avatar', methods=["POST"])
def change_avatar():
    file = request.files['image']
    id = request.form['userId']
    img = Image.open(file.stream)
    img = img.convert("RGB")
    save_path = os.path.join('app/static/avatars', f'avatar{id}.png')
    os.makedirs('app/static/avatars', exist_ok=True) 
    img.save(save_path)
    user = User.query.get(id)
    user.avatar = f'avatar{id}.png'
    db.session.commit()
    return redirect(url_for('profile.user'))


@profile.route('/user')
@jwt_required()
@login_required
def user():
    current_user.avatar = f'/static/avatars/{current_user.avatar}' if current_user.avatar else '/static/styles/images/user-profile-pic.jpg'
    return render_template('user-profile.html')