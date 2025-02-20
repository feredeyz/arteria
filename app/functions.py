from .models import User, Post
from . import db
from datetime import datetime
from flask import make_response, redirect, url_for, render_template
from flask_login import login_user
from flask_jwt_extended import create_access_token
import os
from PIL import Image


from flask_jwt_extended import create_access_token, set_access_cookies

def validate_login(form):
    user = User.query.filter_by(username=form.username.data).first()
    if user and user.check_password(form.password.data):
        login_user(user, remember=True)
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                'username': user.username,
                'description': user.description or "",
                'avatar': user.avatar,
            }
        )

        response = make_response(redirect(url_for('profile.user')))
        set_access_cookies(response, access_token, max_age=3600)
        return response

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
    set_access_cookies(response, access_token, max_age=3600) 
    return response

def change_info(req):
    user = User.query.get(req.json['userId'])
    if not user:
        response = make_response({"msg": "User not found."}, 404)
        return response
    new_username = req.json['content'][1]
    if User.query.filter_by(username=new_username).first():
        return {"msg": "Username already taken."}, 400
    user.description = req.json['content'][0]
    db.session.commit()
    access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                'username': user.username,
                'description': user.description or "",
                'avatar': user.avatar
            }
        )
    response = make_response({"msg": "ok"}, 200)
    response.set_cookie('access_token_cookie', access_token, httponly=True)
    return response
    
def change_avatar(req):
    avatar = req.files['image']
    user_id = req.form['userId']
    if not avatar or not user_id:
        return {"msg": "User not found."}, 404
    img = Image.open(avatar.stream)
    img = img.convert("RGB")
    save_path = os.path.join('app/static/avatars', f'avatar{user_id}.png')
    img.save(save_path)
    user = User.query.get(user_id)
    user.avatar = f'avatars/avatar{user_id}.png'
    db.session.commit()
    return redirect(url_for('profile.user'))
    
def post_add(form, user):
    db.session.add(Post(title=form.title.data, content=form.content.data, created_at=str(datetime.now())[:-7], user_id=user.id))
    db.session.commit()
    return redirect(url_for('posts.popular'))

def get_posts():
    posts = Post.query.all()
    if not posts:
        return []
    result = []
    
    for post in posts:
        result.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "created_at": post.created_at,
            "user": post.user,
            "user_id": post.user_id,
            "liked_by": post.liked_by,
            "likes": len(post.liked_by)
        })
    return result