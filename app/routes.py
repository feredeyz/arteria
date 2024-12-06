from flask import render_template, redirect, url_for, Blueprint, request
from .forms import LoginForm, RegistrationForm, PostForm
from flask_login import login_required, current_user, logout_user
from flask_jwt_extended import jwt_required
from .functions import *

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
profile = Blueprint('profile', __name__)
posts = Blueprint('posts', __name__)

#   ----------------------
#          Pages
#   ----------------------

@main.route('/')
def index():
    return render_template('index.html')
 
@posts.route('/popular')
def popular():
    return render_template('popular.html', form=PostForm(), posts=Post.query.all())

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
    return render_template('user-profile.html')