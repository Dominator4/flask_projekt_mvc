from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember_me = BooleanField('Zapamiętaj')
    submit = SubmitField('Zaloguj')

class RegistrationForm(FlaskForm):
    firstname = StringField('Imie', validators=[DataRequired()])
    lastname = StringField('Nazwisko', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    password2 = PasswordField(
        'Powtórz hasło', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Rejestracja')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Prosze podać inny adres email.')

class EditProfileForm(FlaskForm):
    firstname = StringField('Imię', validators=[DataRequired()])
    lastname = StringField('Nazwisko', validators=[DataRequired()])
    about_me = TextAreaField('O mnie:', validators=[Length(min=0, max=140)])
    contact = TextAreaField('Kontakt:', validators=[Length(min=0, max=140)])
    submit = SubmitField('Zatwierć')

class Addoffersform(FlaskForm):
    name = StringField('Nazwa', validators=[DataRequired()])
    about_this = TextAreaField('Opis oferty', validators=[Length(min=0, max=140)])
    submit = SubmitField('Zatwierć')

class Resetpasswordform(FlaskForm):
    password = PasswordField('Hasło', validators=[DataRequired()])
    password2 = PasswordField(
        'Powtórz hasło', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Zatwierć')