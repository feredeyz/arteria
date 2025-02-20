from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField('', name='username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField('', name='password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Log in')
    
    
class RegistrationForm(FlaskForm):
    username = StringField('', name='username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField('', name='password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    verify_password = PasswordField('', name='verify_password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Verify password"})
    submit = SubmitField('Sign up')
    
class PostForm(FlaskForm):
    title = TextAreaField(' ', id='form-title', name='title', validators=[DataRequired()], render_kw={"placeholder": "Title"})
    content = TextAreaField(' ', id='form-content', name='content', validators=[DataRequired(), Length(max=350)], render_kw={"placeholder": "Your thoughts"})
    submit = SubmitField('Post', id='form-submit')
