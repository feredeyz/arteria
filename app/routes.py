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
    return redirect(url_for('auth.register', next=request.url))

@main.app_errorhandler(405)
def handle_405_error(_err):
    return redirect(url_for('main.index'))

@main.app_errorhandler(404)
def handle_404_error(_err):
    return render_template('404.html')
#   ----------------------
#           Pages
#   ----------------------

@main.route('/')
def index():
    return render_template('index.html')

@posts.route('/popular')
def popular():
    return render_template('popular.html', form=PostForm(), posts=get_posts())

@main.route('/about')
def about():
    return render_template('about.html')

#   ----------------------
#          Posts
#   ----------------------

@posts.route('/add-post', methods=["GET", "POST"])
def add_post():
    if request.method == "GET":
        if not current_user.is_authenticated:
            return redirect(url_for('auth.register'))
        return render_template('addpost.html', form=PostForm())
    else:
        form = PostForm()
        return post_add(form, current_user)

@posts.route('/delete-post', methods=["DELETE"])
def delete_post():
    user_id = request.json['id']
    if not user_id:
        return {"message": "User not found."}, 404
    post = Post.query.get(user_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return {"message": "Post deleted"}, 200
    return {"message": "Post not found"}, 400

@posts.route('/edit-post', methods=["POST"])
def edit_post():
    content, user_id = request.json['content'], request.json['id']
    if not content or not user_id:
        return {"message": "Missing data."}
    post = Post.query.get(user_id)
    if post:
        post.content = content
        db.session.commit()
        return {"message": "Post edited"}, 200 
    return {"message": "Post not found"}, 400

@posts.route('/add-like', methods=["POST"])
def add_like():
    data = request.get_json()
    if not data or 'user' not in data or 'post' not in data:
        return jsonify({"error": "Invalid JSON data"}), 400

    user_id, post_id = data['user'], data['post']
    user = User.query.get(user_id)
    post = Post.query.get(post_id)

    if not user or not post:
        return jsonify({"error": "User or post not found"}), 404

    if post not in user.liked_posts:
        user.liked_posts.append(post)
        db.session.commit()
        return jsonify({"msg": "Like added"}), 200

    return jsonify({"msg": "Already liked"}), 200

@posts.route('/delete-like', methods=["POST"])
def delete_like():
    data = request.get_json()
    if not data or 'user' not in data or 'post' not in data:
        return jsonify({"error": "Invalid JSON data"}), 400

    user_id, post_id = data['user'], data['post']
    user = User.query.get(user_id)
    post = Post.query.get(post_id)

    if not user or not post:
        return jsonify({"error": "User or post not found"}), 404

    if post in user.liked_posts:
        user.liked_posts.remove(post)
        db.session.commit()
        return jsonify({"msg": "Like removed"}), 200

    return jsonify({"msg": "Like not found"}), 400


#   ----------------------
#       Authentication
#   ----------------------

@auth.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        next_page = request.args.get('next')
        return redirect(next_page or url_for('profile.user'))
    form = LoginForm()
    if form.validate_on_submit():
        return validate_login(form)
    return render_template('login.html', form=form)


@auth.route('/register', methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        return validate_registration(form)
    return render_template('registrate.html', form=form)

#   ----------------------
#        User profile
#   ----------------------

@profile.route('/confirm-edit', methods=["POST"])
def confirm_edit():
    return change_info(request)

@profile.route('/change-avatar', methods=["POST"])
def change_av():
    return change_avatar(request)

@profile.route('/logout', methods=["POST"])
def logout():
    response = make_response(jsonify({"message": "Logged out"}))
    unset_jwt_cookies(response)
    logout_user()
    return response, 200

@profile.route('/user')
@login_required
@jwt_required()
def user():
    return render_template('user-profile.html')
