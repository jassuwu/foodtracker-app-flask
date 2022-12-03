from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField, PasswordField
from wtforms.validators import InputRequired, Length


class FoodForm(FlaskForm):
    name = StringField('Food Name',
                       validators=[InputRequired('You have to enter a name.')])
    protein = IntegerField('Protein',
                           validators=[
                               InputRequired('Proteins where?'),
                           ])
    carbs = IntegerField('Carbs',
                         validators=[InputRequired('Carbohydrates where?')])
    fats = IntegerField('Fats', validators=[InputRequired('Fats where?')])


class EditFoodForm(FlaskForm):
    protein = IntegerField('Protein',
                           validators=[
                               InputRequired('Proteins where?'),
                           ])
    carbs = IntegerField('Carbs',
                         validators=[InputRequired('Carbohydrates where?')])
    fats = IntegerField('Fats', validators=[InputRequired('Fats where?')])


class DateForm(FlaskForm):
    date = DateField('Add New Date',
                     validators=[InputRequired('Bro? the date ?')])


class DayFoodForm(FlaskForm):
    dayFood = SelectField(
        'Add Food', validators=[InputRequired('Bro what do want to add?')])


class RegisterForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[InputRequired('Name where?'),
                    Length(min=0, max=100)])
    username = StringField(
        'Username',
        validators=[InputRequired('Username where?'),
                    Length(min=0, max=30)])
    password = PasswordField(
        'Password',
        validators=[InputRequired('Password where?'),
                    Length(min=0, max=8)])


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[InputRequired('Username where?'),
                    Length(min=0, max=30)])
    password = PasswordField(
        'Password',
        validators=[InputRequired('Password where?'),
                    Length(min=0, max=8)])
