# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UpdateCourseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    id = IntegerField('ID', validators=[DataRequired()])
    submit = SubmitField('Update')

class UpdateVideoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    link = StringField('Link', validators=[DataRequired()])
    submit = SubmitField('Update')

class AddCourseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired(), Length(min=2, max=1000)])
    iframes_links = StringField('description', validators=[DataRequired(), Length(min=2, max=1000)])
    submit = SubmitField('Add')
