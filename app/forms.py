from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
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
    title = StringField(' ', id='form-title', name='title', validators=[DataRequired()], render_kw={"placeholder": "Title"})
    content = TextAreaField(' ', id='form-content', name='content', validators=[DataRequired(), Length(max=250)], render_kw={"placeholder": "Your thoughts"})
    submit = SubmitField('Post', id='form-submit')