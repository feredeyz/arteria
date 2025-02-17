from flask import render_template, redirect, url_for, Blueprint, request, jsonify
from .forms import LoginForm, RegistrationForm, PostForm
from flask_login import login_required, current_user, logout_user
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from .functions import *
from . import jwt_manager, login_manager


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
    return redirect(url_for('auth.login'))

@login_manager.unauthorized_handler
def custom_unauthorized_response_login(_err):
    return redirect(url_for('auth.login'))

@main.app_errorhandler(405)
def handle_405_error(error):
    return redirect(url_for('main.index'))

@main.app_errorhandler(404)
def handle_405_error(error):
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

def get_posts():
    posts = Post.query.all()
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

@posts.route('/add-post', methods=["POST"])
def add_post():
    form = PostForm()
    post_add(form, current_user)    
    return redirect(url_for('posts.popular'))

@posts.route('/delete-post', methods=["DELETE"])
def delete_post():
    id = request.json['id']
    post = Post.query.get(id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return {"message": "Post deleted"}, 200
    return {"message": "Post not found"}, 400

@posts.route('/edit-post', methods=["POST"])
def edit_post():
    content, id = request.json['content'], request.json['id']
    post = Post.query.get(id)
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
        return redirect(url_for('profile.user'))
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

@profile.route('/confirm-description-edit', methods=["POST"])
def confirm_desc_edit():
    change_description(request)
    return redirect(url_for('profile.user'))

@profile.route('/change-avatar', methods=["POST"])
def change_av():
    change_avatar(request)
    return redirect(url_for('profile.user'))

@profile.route('/logout', methods=["DELETE"])
def logout():
    logout_user()
    return {"message": "Logged out"}, 200 

@profile.route('/user')
@jwt_required()
@login_required
def user():
    print(current_user.password)
    return render_template('user-profile.html')
