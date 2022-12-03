from flask import Blueprint, render_template, redirect, url_for, abort, flash
from ..forms import FoodForm, DateForm, DayFoodForm, EditFoodForm, RegisterForm, LoginForm
from datetime import datetime
from ..models import User, Food, Log, LogFoodUser
from ..extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

main = Blueprint('main', __name__)

# For better modularization, auth shoulda been a separate blueprint.


@main.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # return {
        #     "name": form.name.data,
        #     "username": form.username.data,
        #     "password": generate_password_hash(form.password.data)
        # }

        newUser = User(name=form.name.data,
                       username=form.username.data,
                       password=generate_password_hash(form.password.data))
        db.session.add(newUser)
        db.session.commit()
        login_user(newUser)
        return redirect(url_for("main.index"))

    return render_template('main/register.html', form=form)


@main.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # return {"username": form.username.data, "password": form.password.data}
        userToLogin = User.query.filter_by(username=form.username.data).first()
        if check_password_hash(userToLogin.password, form.password.data):
            login_user(userToLogin)
            flash('Logged ' + userToLogin.name + ' in successfully.')
            return redirect(url_for('main.index'))
        else:
            return "Wrong password, bucko.", 503
    return render_template('main/login.html', form=form)


@main.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route("/help")
def help():
    return render_template('main/help.html')


@main.route("/", methods=['GET', 'POST'])
@login_required
def index():
    form = DateForm()

    if form.validate_on_submit():
        # return {"date": form.date.data.strftime("%B %m, %Y")}

        # Have to do a check to see if the date already exists to avoid duplicate date entries.
        newLog = Log(logDate=form.date.data)
        db.session.add(newLog)
        current_user.logs.append(newLog)
        db.session.commit()

        return redirect(url_for("main.index"))

    ############################################################################################
    ## SETTING THE LIMIT TO 5, BECAUSE IN REALITY THERE NEEDS TO BE PAGINATION OR SEARCH HERE ##
    ############################################################################################
    logList = current_user.logs[:]
    existingRecordsCount = len(logList[:])
    statsThisDate = {}
    for log in logList[-5:]:
        foodsids = LogFoodUser.query.filter_by(
            user_id=current_user.id).filter_by(log_id=log.id).all()
        foodsThisDate = []
        for fid in foodsids:
            foodsThisDate.append(Food.query.filter_by(id=fid.food_id).first())
        statsThisDate[log.id] = {"proteins": 0, "carbs": 0, "fats": 0}
        for food in foodsThisDate:
            statsThisDate[log.id]["proteins"] += food.proteins
            statsThisDate[log.id]["carbs"] += food.carbs
            statsThisDate[log.id]["fats"] += food.fats
    return render_template('main/index.html',
                           form=form,
                           logList=logList,
                           statsThisDate=statsThisDate,
                           existingRecordsCount=existingRecordsCount)


@main.route("/add", methods=['GET', 'POST'])
@login_required
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
    ##############################################################################################
    # allowDelete:boolean - This is because there may be references to deletedFood in some dates #
    ##############################################################################################
    return render_template("main/add.html",
                           form=form,
                           foodList=foodList,
                           allowDelete=False)


@main.route("/edit/<foodid>", methods=['GET', 'POST'])
@login_required
def edit(foodid):
    form = FoodForm()
    foodToEdit = Food.query.filter_by(id=foodid).first()
    if form.validate_on_submit():
        foodToEdit.name = form.name.data
        foodToEdit.proteins = form.protein.data
        foodToEdit.carbs = form.carbs.data
        foodToEdit.fats = form.fats.data
        db.session.commit()
        return redirect(url_for("main.add"))
    return render_template("main/edit.html", form=form, foodToEdit=foodToEdit)


@main.route("/view/<dateid>", methods=['GET', 'POST'])
@login_required
def view(dateid):
    form = DayFoodForm()
    form.dayFood.choices = [(food.id, food.name)
                            for food in Food.query.order_by('name')]

    if form.validate_on_submit():
        # return {"food_id": form.dayFood.data, "log_id": dateid}
        foodToAdd = Food.query.filter_by(id=form.dayFood.data).first()
        LogToAddTo = Log.query.filter_by(id=dateid).first()
        newUserLogFood = LogFoodUser(log_id=LogToAddTo.id,
                                     food_id=foodToAdd.id,
                                     user_id=current_user.id)
        db.session.add(newUserLogFood)
        db.session.commit()
        return redirect(url_for('main.view', dateid=dateid))

    logDate = Log.query.filter_by(id=dateid).first()
    foodsids = LogFoodUser.query.filter_by(user_id=current_user.id).filter_by(
        log_id=dateid).all()
    foodsThisDate = []
    for fid in foodsids:
        foodsThisDate.append(Food.query.filter_by(id=fid.food_id).first())
    todayStats = {"proteins": 0, "carbs": 0, "fats": 0}
    for food in foodsThisDate:
        todayStats["proteins"] += food.proteins
        todayStats["carbs"] += food.carbs
        todayStats["fats"] += food.fats
    return render_template("main/view.html",
                           form=form,
                           logDate=logDate,
                           foodsThisDate=foodsThisDate,
                           todayStats=todayStats)


@main.route("/deleteFood/<foodid>")
@login_required
def deleteFood(foodid):
    foodToDelete = Food.query.filter_by(id=foodid).delete()
    db.session.commit()
    return redirect(url_for('main.add'))


@main.route("/deleteDayFood/<day>/<food>")
@login_required
def deleteDayFood(day, food):
    LogFoodUser.query.filter_by(food_id=food,
                                log_id=day,
                                user_id=current_user.id).delete()
    db.session.commit()
    return redirect(url_for('main.view', dateid=day))