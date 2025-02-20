from flask import render_template, redirect, url_for, Blueprint, request, jsonify
from .forms import LoginForm, RegistrationForm, PostForm
from flask_login import login_required, current_user, logout_user
from flask_jwt_extended import jwt_required, unset_jwt_cookies
from .functions import *
from . import jwt_manager


#   ---------------------- 
#         Blueprints
#   ----------------------

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
profile = Blueprint('profile', __name__)
posts = Blueprint('posts', __name__)
admin = Blueprint('admin', __name__)

#   ---------------------- 
#       Error handlers
#   ----------------------

@jwt_manager.unauthorized_loader
def custom_unauthorized_response_jwt(_err):
    '''
    Обработчик ошибок, связанных с отсутствием JWT токена
    '''
    return redirect(url_for('auth.register', next=request.url))

@main.app_errorhandler(405)
def handle_405_error(_err):
    '''
    Обработчик ошибок HTTP 405
    '''
    return redirect(url_for('main.index'))

@main.app_errorhandler(404)
def handle_404_error(_err):
    '''
    Обработчик ошибок HTTP 404
    '''
    return render_template('404.html')
#   ----------------------
#           Pages
#   ----------------------

@main.route('/')
def index():
    '''
    Функция для рендера главной страницы
    '''
    return render_template('index.html')

@posts.route('/popular')
def popular():
    '''
    Функция для рендера страницы с постами
    '''
    return render_template('popular.html', form=PostForm(), posts=get_posts())

@main.route('/about')
def about():
    '''
    Функция для рендера страницы "About"
    '''
    return render_template('about.html')

#   ----------------------
#          Posts
#   ----------------------

@posts.route('/add-post', methods=["GET", "POST"])
def add_post():
    '''
    Функция для добавления постов.
    '''
    if request.method == "GET":
        '''
        Если запрос был отправлен методом GET, т. е. пользователь нажал на кнопку "Create" в шапке сайта,
        рендерится страница с добавлением поста.
        '''
        if not current_user.is_authenticated:
            '''
            Если пользователь не авторизован, перенаправить на страницу регистрации
            '''
            return redirect(url_for('auth.register'))
        return render_template('addpost.html', form=PostForm())
    else:
        form = PostForm()
        return post_add(form, current_user)

@posts.route('/delete-post', methods=["DELETE"])
def delete_post():
    '''
    Функция удаления поста.
    '''
    post_id = request.json['id']
    if not post_id:
        '''
        Если в запросе не был отправлен id поста, отправить ошибку.
        '''
        return {"message": "Post not found."}, 404
    post = Post.query.get(post_id)
    if post:
        '''
        Если есть пост с данным id, удалить его из БД
        '''
        db.session.delete(post)
        db.session.commit()
        return {"message": "Post deleted"}, 200
    '''
    Если нету, отправить ошибку
    '''
    return {"message": "Post not found"}, 400

@posts.route('/edit-post', methods=["POST"])
def edit_post():
    '''
    Функция для обновления поста в БД
    '''
    content, post_id = request.json['content'], request.json['id']
    if not content or not post_id:
        '''
        Если в запросе не был отправлен id поста, отправить ошибку.
        '''
        return {"message": "Missing data."}
    post = Post.query.get(post_id)
    if post:
        '''
        Если такой пост существует, обновить его информацию.
        '''
        post.content = content
        db.session.commit()
        return {"message": "Post edited"}, 200 
    '''
    Если нету, отправить ошибку.
    '''
    return {"message": "Post not found"}, 400

@posts.route('/add-like', methods=["POST"])
def add_like():
    '''
    Функция для добавления лайка.
    '''
    data = request.get_json()
    if not data or 'user' not in data or 'post' not in data:
        '''
        Если в запросе не корректно была отправлена информация, отправить ошибку.
        '''
        return jsonify({"error": "Invalid JSON data"}), 400

    user_id, post_id = data['user'], data['post']
    user = User.query.get(user_id)
    post = Post.query.get(post_id)

    if not user or not post:
        '''
        Если нет пользователя и поста по данным id, то отправить ошибку.
        '''
        return jsonify({"error": "User or post not found"}), 404

    if post not in user.liked_posts:
        '''
        Если пользователь ранее не лайкал пост, добавить его лайк.
        '''
        user.liked_posts.append(post)
        db.session.commit()
        return jsonify({"msg": "Like added"}), 200
    '''
    Если лайкал, отправить ошибку
    '''
    return jsonify({"msg": "Already liked"}), 400

@posts.route('/delete-like', methods=["POST"])
def delete_like():
    '''
    Функция удаления лайка
    '''
    data = request.get_json()
    if not data or 'user' not in data or 'post' not in data:
        '''
        Если в запросе не корректно была отправлена информация, отправить ошибку.
        '''
        return jsonify({"error": "Invalid JSON data"}), 400

    user_id, post_id = data['user'], data['post']
    user = User.query.get(user_id)
    post = Post.query.get(post_id)

    if not user or not post:
        '''
        Если нет пользователя и поста по данным id, то отправить ошибку.
        '''
        return jsonify({"error": "User or post not found"}), 404

    if post in user.liked_posts:
        '''
        Если пользователь ранее лайкал пост, удалить его лайк.
        '''
        user.liked_posts.remove(post)
        db.session.commit()
        return jsonify({"msg": "Like removed"}), 200
    '''
    Если не лайкал, отправить ошибку.
    '''
    return jsonify({"msg": "Like not found"}), 400


#   ----------------------
#       Authentication
#   ----------------------

@auth.route('/login', methods=["POST", "GET"])
def login():
    '''
    Функция входа в аккаунт
    '''
    if current_user.is_authenticated:
        '''
        Если пользователь уже авторизован, перенаправить его на другую страницу.
        '''
        next_page = request.args.get('next')
        return redirect(next_page or url_for('profile.user'))
    form = LoginForm()
    if form.validate_on_submit():
        '''
        Валидация данных.
        '''
        return validate_login(form)
    '''
    Рендер страницы
    '''
    return render_template('login.html', form=form)


@auth.route('/register', methods=["POST", "GET"])
def register():
    '''
    Функция регистрации
    '''
    if current_user.is_authenticated:
        '''
        Если пользователь уже авторизован, перенаправить его на другую страницу.
        '''
        next_page = request.args.get('next')
        return redirect(next_page or url_for('profile.user'))
    form = RegistrationForm()
    if form.validate_on_submit():
        '''
        Валидация данных
        '''
        return validate_registration(form)
    '''
    Рендер страницы.
    '''
    return render_template('registrate.html', form=form)

#   ----------------------
#        User profile
#   ----------------------

@profile.route('/confirm-edit', methods=["POST"])
def confirm_edit():
    '''
    Функция изменения данных пользователя
    '''
    return change_info(request)

@profile.route('/change-avatar', methods=["POST"])
def change_av():
    '''
    Функция изменения картинки профилья пользователя.
    '''
    return change_avatar(request)

@profile.route('/logout', methods=["POST"])
def logout():
    '''
    Функция выхода из аккаунта
    '''
    response = make_response(jsonify({"message": "Logged out"}))
    unset_jwt_cookies(response)
    logout_user()
    return response, 200

@profile.route('/user')
@login_required
@jwt_required()
def user():
    '''
    Рендер профиля пользователя
    '''
    return render_template('user-profile.html')
