from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField
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


class DateForm(FlaskForm):
    date = DateField('Add New Date',
                     validators=[InputRequired('Bro? the date ?')])


class DayFoodForm(FlaskForm):
    dayFood = SelectField(
        'Add Food', validators=[InputRequired('Bro what do want to add?')])
