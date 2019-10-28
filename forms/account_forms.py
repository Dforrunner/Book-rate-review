from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, InputRequired, EqualTo, Length, Regexp

from util.validators import Unique, ValidUser
from models import User


class SignUpForm(FlaskForm):
    username = StringField('Username',
                           validators=[
                               DataRequired(),
                               Regexp('^\w+$', message="Username can contain only letters, numbers and underscores"),
                               Length(min=4, max=15, message="Username must be between 4 & 15 characters"),
                               Unique(User, User.username, message='This username already exists. Pick a new one.')
                           ],
                           render_kw={'placeholder': 'Username'})

    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email(),
                            Length(min=5, max=60),
                            Unique(User, User.email, message='There is already an account with that email.')
                        ],
                        render_kw={'placeholder': 'E-mail'})

    password = PasswordField('Create Password',
                             validators=[
                                 InputRequired(),
                                 EqualTo('confirm', message='Passwords must match'),
                                 Regexp('(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*-_]).+', message="Password must contain at least: 1 lowercase letter, 1 uppercase letter, 1 number, and special character (!@#$%^&*-_)"),
                                 Length(min=8, max=25, message="Password must be between 8 & 25 characters")
                             ],
                             render_kw={'placeholder': 'Password'})

    confirm = PasswordField('Confirm Password', render_kw={'placeholder': 'Confirm password'})
    submit = SubmitField('Sign Up')


class SignInForm(FlaskForm):
    email = StringField('Email address',
                        validators=[
                            DataRequired(),
                            Email()
                        ],
                        render_kw={'placeholder': 'E-mail'})

    password = PasswordField('Password',
                             validators=[
                                 DataRequired()
                             ],
                             render_kw={'placeholder': 'Password'})

    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# Form to reset forgotten password
class PassResetEmailForm(FlaskForm):
    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email(),
                            ValidUser(User, User.email, message='There is no account associated to the given email.')
                        ],
                        render_kw={'placeholder': 'E-mail'})
    submit = SubmitField('Reset Password')


class PassResetForm(FlaskForm):
    password = PasswordField('Create Password',
                             validators=[
                                 InputRequired(),
                                 EqualTo('confirm', message='Passwords must match'),
                                 Regexp('(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*-_]).+', message="Password must contain at least: 1 lowercase letter, 1 uppercase letter, 1 number, and special character (!@#$%^&*-_)"),
                                 Length(min=8, max=25, message="Password must be between 8 & 25 characters")
                             ],
                             render_kw={'placeholder': 'Password'})

    confirm = PasswordField('Confirm Password', render_kw={'placeholder': 'Confirm password'})
    submit = SubmitField('Reset Password')


# Form to change password given that you know the old password
class ChangePassForm(FlaskForm):
    old_password = PasswordField('Old Password',
                             validators=[
                                 InputRequired(),
                             ],
                             render_kw={'placeholder': 'Password'})

    password = PasswordField('Create Password',
                             validators=[
                                 InputRequired(),
                                 EqualTo('confirm', message='Passwords must match'),
                                 Regexp('(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*-_]).+', message="Password must contain at least: 1 lowercase letter, 1 uppercase letter, 1 number, and special character (!@#$%^&*-_)"),
                                 Length(min=8, max=25, message="Password must be between 8 & 25 characters")
                             ],
                             render_kw={'placeholder': 'Password'})

    confirm = PasswordField('Confirm Password', render_kw={'placeholder': 'Confirm password'})
    submit = SubmitField('Change Password')

