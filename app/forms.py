from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField('Your username: ', name='username', validators=[DataRequired()])
    password = PasswordField('Your password: ', name='password', validators=[DataRequired()])
    submit = SubmitField('Log in')
    
    
class RegistrationForm(FlaskForm):
    username = StringField('Enter username: ', name='username', validators=[DataRequired()])
    password = PasswordField('Enter password: ', name='password', validators=[DataRequired()])
    verify_password = PasswordField('Verify password: ', name='password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
class PostForm(FlaskForm):
    title = StringField('Title: ', name='title', validators=[DataRequired()])
    content = StringField('Content: ', name='content', validators=[DataRequired(), Length(max=250)])
    submit = SubmitField('Post')