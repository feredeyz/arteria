from flask import render_template, redirect, url_for, Blueprint, request
from .forms import LoginForm, RegistrationForm, PostForm
from flask_login import login_required, current_user, logout_user
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
    return render_template('popular.html', form=PostForm(), posts=Post.query.all())

@main.route('/contacts')
def contacts():
    return render_template('contacts.html')

@main.route('/about')
def about():
    return render_template('about.html')

#   ----------------------
#          Posts
#   ----------------------

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

#   ----------------------
#           Admin
#   ----------------------

@admin.route('/admin')
def log_admin():
    return render_template('admin.html')

@admin.route('/log-admin', methods=["POST"])
def check_log_admin():
    if request.form['username'] == 'admin' and request.form['password'] == 'admin':
        user = User(username='admin', password='admin', role='admin', date=str(datetime.now())[:-7])
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('admin.admin_panel'))
    return redirect(url_for('posts.popular'))
    
@admin.route('/admin-panel')
def admin_panel():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return render_template('admin-panel.html')
    return redirect(url_for('main.index'))

@admin.route('/delete-all-posts')
def delete_all_posts():
    Post.query.delete()
    db.session.commit()
    return {"message": "Deleted all posts"}, 200
    
@admin.route('/delete-all-users')
def delete_all_users():
    User.query.delete()
    db.session.commit()
    return {"message": "Deleted all users"}, 200
 