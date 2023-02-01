from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

attended_class_choices = [
    ('Computer for kids', 'Computer for kids'),
    ('Basic', 'Basic'),
    ('DPT', 'DPT'),
    ('Advanced Excel', 'Advanced Excel'),
    ('Multimedia', 'Multimedia'),
    ('Photoshop', 'Photoshop'),
    ('A+', 'A+'),
    ('Network', 'Network'),
    ('Internet', 'Internet'),
    ('Web Design', 'Web Design')
]

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')


class AddStudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Length(min=7, max=15)])
    attended_class = SelectField('Classes', choices=attended_class_choices)
    submit = SubmitField('Add Student')

class UpdateStudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Length(min=7, max=15)])
    attended_class = SelectField(u'Computer for kids', choices=attended_class_choices)
    submit = SubmitField('Update Student')

