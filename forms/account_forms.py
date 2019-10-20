from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired,Email, InputRequired, EqualTo
from flask_wtf.csrf import CSRFProtect


class SignUpForm(FlaskForm):
    firstname = StringField('First name', validators=[DataRequired(message="Enter first name")], render_kw={'placeholder': 'First name'})
    lastname = StringField('Last name', validators=[DataRequired()], render_kw={'placeholder': 'Last name'})
    username = StringField('Username', validators=[DataRequired()], render_kw={'placeholder': 'Username'})
    email = StringField('Email', validators=[DataRequired, Email()], render_kw={'placeholder': 'example@example.com'})
    password = PasswordField('Create Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')], render_kw={'placeholder': 'Password'})
    confirm = PasswordField('Repeat Password', render_kw={'placeholder': 'Re-enter password'})
    submit = SubmitField('Sign Up')


class SignInForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(message="Enter email"), Email()], render_kw={'placeholder': 'example@example.com'})
    password = PasswordField('Password', validators=[DataRequired(message="Enter password")], render_kw={'placeholder': 'Password'})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
