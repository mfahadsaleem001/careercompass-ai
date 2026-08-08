from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegisterForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match')]
    )
    submit = SubmitField('Create Account')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class CareerAdvisorForm(FlaskForm):
    education_level = SelectField(
        'Education Level',
        choices=[
            ('', 'Select your education level'),
            ('Matric', 'Matric'),
            ('Intermediate (FA/FSc/ICS/ICom)', 'Intermediate (FA/FSc/ICS/ICom)'),
            ('BS / Bachelors', 'BS / Bachelors'),
            ('Graduate', 'Graduate'),
            ('Other', 'Other')
        ],
        validators=[DataRequired()]
    )
    marks_cgpa = StringField('Marks / CGPA', validators=[Length(max=50)])
    interests = TextAreaField('Interests', validators=[DataRequired(), Length(max=300)])
    skills = TextAreaField('Current Skills', validators=[Length(max=300)])
    career_goal = StringField('Career Goal', validators=[Length(max=200)])
    budget = StringField('Budget (for further education)', validators=[Length(max=50)])
    country = StringField('Country', validators=[Length(max=80)])
    preferred_industry = StringField('Preferred Industry', validators=[Length(max=120)])
    submit = SubmitField('Get My Career Plan')