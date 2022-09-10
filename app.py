import datetime
from flask import Flask, render_template, session, request, redirect, flash, url_for
import db


app = Flask(__name__)
app.config.from_object("config")


@app.route('/')
def index():
    return render_template("index.html", session=session)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password:
            account = db.get_user(username, password)
            if account:
                session["loggedin"] = True
                session["username"] = username
                session["id"] = account[0]
                flash("Вы успешно авторизовались")
                return redirect(url_for('index'))
            else:
                flash("Введены неверные данные")
                return redirect(url_for('login'))
        else:
            flash("Введите логин и пароль")
            return redirect(url_for('login'))


@app.route('/logout', methods=["GET"])
def logout():
    session.pop('loggedin')
    session.pop('username')
    flash("Вы успешно вышли из системы")
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        account = db.get_user(request.form.get("username"), request.form.get("password"))
        if account:
            flash("Пользователь с таким логином уже существует")
            return redirect(url_for('register'))
        else:
            db.add_user(request.form.get("username"), request.form.get("password"),
                        request.form.get("first_name"), request.form.get("last_name"))
            flash("Пользователь успешно зарегистрирован")
            return redirect(url_for("index"))


@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if 'loggedin' not in session:
        flash("Авторизируйтесь, чтобы пользоваться сервисом")
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('add_task.html')
    else:
        if request.form.get("date") == '':
            flash("Введите дату")
            return redirect(url_for('add_task'))
        if request.form.get("name") == '':
            flash("Введите задачу")
            return redirect(url_for('add_task'))
        date = request.form.get("date")
        name = request.form.get("name")
        db.add_task(name, date, session["id"])
        flash("Задача успешно добавлена")
        return redirect(url_for('add_task'))


@app.route('/get_tasks', methods=['GET', 'POST'])
def get_tasks():
    if 'loggedin' not in session:
        flash("Авторизируйтесь, чтобы пользоваться сервисом")
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('get_tasks.html')
    else:
        if request.form.get("date") != '':
            tasks = db.get_tasks(session["id"], request.form.get("date"))
            return render_template("get_tasks.html", tasks=tasks)
        else:
            flash("Введите дату")
            return redirect(url_for('get_tasks'))


if __name__ == '__main__':
    app.run()
