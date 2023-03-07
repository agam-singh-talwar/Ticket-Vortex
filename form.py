from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, BooleanField, SubmitField, TimeField, EmailField, PasswordField, DateField, DecimalRangeField, SelectField, validators,TextAreaField,DecimalRangeField, SelectField, FileField

class RegisterForm(FlaskForm):
    Name=StringField("Hi! What can I call you?",[validators.data_required()])
    Email = EmailField("What's your email", [validators.data_required()])
    Pass1 = PasswordField(
        "Password", [validators.data_required(), validators.Length(min=6)])
    Pass2 = PasswordField("Password", [validators.data_required(
    ), validators.Length(min=6), validators.equal_to('Pass1')])
    Bulk = BooleanField("Are you a Bulk buyer?")
    Submit = SubmitField("Register")


class LoginForm(FlaskForm):
    Email = EmailField("What's your email", [validators.data_required()])
    Pass = PasswordField(
        "Password", [validators.data_required(), validators.Length(min=6)])
    Submit = SubmitField("Sign In ")


class ConcertForm(FlaskForm):
    default = {}

    title = StringField('concert title: ', [validators.data_required()])
    artist = StringField('Artist name: ', [validators.data_required()])
    preivew = ''
    image = FileField('concert cover: ', [])
    description = TextAreaField('concert description: ', [validators.data_required(), validators.length(min=10)])
    date = DateField('concert date: ', [validators.data_required()])
    time = TimeField('Time: ', [validators.data_required()])
    utilization = DecimalRangeField('Percent of venue seats used: ', [validators.data_required(), validators.number_range(50, 100)])
    floorPrice = DecimalField('Price per floor seat: ')
    bowlPrice = DecimalField('Price per bowl seat: ')
    boxPrice = DecimalField('Price per box seat: ')

    venue = SelectField('concert venue: ', choices=[
        ('64038bc348aac9e739e734f2', 'Danforth Music Hall'),
        ('64038db2ffbf6fe0e51b555d', 'Koerner Hall'),
        ('640390b446140ae93a279eb1', 'Budweiser Stage'),
        ('6403917b74814f460a9c5f46', 'Massey Hall')
    ],
        validators=[validators.data_required()]
    )
    submit = SubmitField("Create concert")
