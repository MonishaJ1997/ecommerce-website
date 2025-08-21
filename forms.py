from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class ProductForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=200)])
    description = TextAreaField("Description")
    price = FloatField("Price", validators=[DataRequired()])
    submit = SubmitField("Save")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

