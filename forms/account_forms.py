from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, InputRequired, EqualTo, Length, Regexp, ValidationError
from flask_wtf.csrf import CSRFProtect

from util.validators import Unique
from db.models import Users


class SignUpForm(FlaskForm):
    firstname = StringField('First name',
                            validators=[
                                DataRequired(),
                                Regexp('^\w+$', message="First name can only contain letters."),
                                Length(max=25, message="First name cannot exceed 25 characters")
                            ],
                            render_kw={'placeholder': 'First name'})

    lastname = StringField('Last name',
                           validators=[
                               DataRequired(),
                               Regexp('^\w+$', message="Last name can only contain letters."),
                               Length(max=25, message="First name cannot exceed 25 characters")
                           ],
                           render_kw={'placeholder': 'Last name'})

    username = StringField('Username',
                           validators=[
                               DataRequired(),
                               Regexp('^\w+$', message="Username can contain only letters, numbers and underscores"),
                               Length(min=4, max=15, message="Username must be between 4 & 15 characters"),
                               Unique(Users, Users.username, message='This username already exists. Pick a new one.')
                           ],
                           render_kw={'placeholder': 'Username'})

    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email(),
                            Length(min=5, max=60),
                            Unique(Users, Users.email, message='There is already an account with that email.')
                        ],
                        render_kw={'placeholder': 'example@example.com'})

    password = PasswordField('Create Password',
                             validators=[
                                 InputRequired(),
                                 EqualTo('confirm', message='Passwords must match'),
                                 Regexp('(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*-_]).+', message="Password must contain at least: 1 lowercase letter, 1 uppercase letter, 1 number, and special character (!@#$%^&*-_)"),
                                 Length(min=6, max=25, message="Password must be between 6 & 25 characters")
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
                        render_kw={'placeholder': 'example@example.com'})

    password = PasswordField('Password',
                             validators=[
                                 DataRequired()
                             ],
                             render_kw={'placeholder': 'Password'})

    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
