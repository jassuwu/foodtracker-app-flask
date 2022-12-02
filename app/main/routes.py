from flask import Blueprint, render_template, redirect, url_for
from ..forms import FoodForm, DateForm, DayFoodForm
from datetime import datetime
from ..models import Food, Log, log_food
from ..extensions import db

main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
def index():
    form = DateForm()

    if form.validate_on_submit():
        # return {"date": form.date.data.strftime("%B %m, %Y")}

        # Have to do a check to see if the date already exists to avoid duplicate date entries.
        # There is a existing records counter on top of the date panels.
        newLog = Log(logDate=form.date.data)
        db.session.add(newLog)
        db.session.commit()

        return redirect(url_for("main.index"))

    ############################################################################################
    ## SETTING THE LIMIT TO 5, BECAUSE IN REALITY THERE NEEDS TO BE PAGINATION OR SEARCH HERE ##
    ############################################################################################
    logList = Log.query.order_by(Log.id.desc()).limit(5).all()
    statsThisDate = {}
    for log in logList:
        foodsThisDate = log.foods.all()
        statsThisDate[log.id] = {"proteins": 0, "carbs": 0, "fats": 0}
        for food in foodsThisDate:
            statsThisDate[log.id]["proteins"], statsThisDate[
                log.id]["carbs"], statsThisDate[log.id]["fats"] = (
                    food.proteins, food.carbs, food.fats)
    return render_template("main/index.html",
                           form=form,
                           logList=logList,
                           statsThisDate=statsThisDate,
                           existingRecordsCount=Log.query.count())


@main.route("/add", methods=['GET', 'POST'])
def add():
    form = FoodForm()

    if form.validate_on_submit():
        # return {
        #     "name": form.name.data,
        #     "proteins": form.protein.data,
        #     "carbs": form.carbs.data,
        #     "fats": form.fats.data
        # }

        newFood = Food(name=form.name.data,
                       proteins=form.protein.data,
                       carbs=form.carbs.data,
                       fats=form.fats.data)

        db.session.add(newFood)
        db.session.commit()

        return redirect(url_for("main.add"))

    foodList = Food.query.all()
    return render_template("main/add.html", form=form, foodList=foodList)


@main.route("/view/<dateid>", methods=['GET', 'POST'])
def view(dateid):
    form = DayFoodForm()
    form.dayFood.choices = [(food.id, food.name)
                            for food in Food.query.order_by('name')]

    if form.validate_on_submit():
        # return {"food_id": form.dayFood.data, "log_id": dateid}
        foodToAdd = Food.query.filter_by(id=form.dayFood.data).first()
        LogToAddTo = Log.query.filter_by(id=dateid).first()
        LogToAddTo.foods.append(foodToAdd)
        db.session.commit()
        return redirect(url_for('main.view', dateid=dateid))

    logDate = Log.query.filter_by(id=dateid).first()
    foodsThisDate = logDate.foods.all()
    todayStats = {"proteins": 0, "carbs": 0, "fats": 0}
    for food in foodsThisDate:
        todayStats["proteins"], todayStats["carbs"], todayStats["fats"] = (
            food.proteins, food.carbs, food.fats)
    return render_template("main/view.html",
                           form=form,
                           logDate=logDate,
                           foodsThisDate=foodsThisDate,
                           todayStats=todayStats)
