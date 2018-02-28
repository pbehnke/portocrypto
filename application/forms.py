from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, BooleanField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from application.models import User, Coins, Transactions
from application.helpers import totalcoin

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class TransForm(FlaskForm):
    userid = StringField('Userid', validators=[DataRequired()])
    short = StringField('Short', validators=[DataRequired()])
    longname = StringField('Longname', validators=[DataRequired()])
    number = FloatField('Number', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    buyOrsell = BooleanField('buyOrsell')
    submit = SubmitField()

    def validate_number(self, number):
        # when selling (buyOrsell.data == True), checking if enough coins available
        if self.buyOrsell.data and number.data > totalcoin(self.userid.data, self.short.data):
            raise ValidationError('Not enough coins.')
        # when buying (buyOrsell.data == False), checking if enough cash available
        if not self.buyOrsell.data:
            print("validating buy transaction")
            cash = User.query.get(int(self.userid.data)).cash
            if (number.data * self.price.data) > cash:
                raise ValidationError('Not enough cash.')

class ChangeForm(FlaskForm):
    oldPassword = PasswordField('oldPassword', validators=[DataRequired()])
    newPassword = PasswordField('newPassword', validators=[DataRequired()])
    submit = SubmitField()
