from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3
import pandas as pd
import sys, traceback
import email_validator

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users_Info.db'
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['UPLOAD_FOLDER'] = r"C:\Users\User\PycharmProjects\FinalProject\Code\static\Excel"
app.secret_key = "123"

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
Bootstrap(app)


con = sqlite3.connect('Input_Files.db')
con.execute("create table if not exists data(pid integer primary key,exceldata TEXT)")
con.close()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

class Temp(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    banana = db.Column(db.String(15), unique=True)


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

# def connect_input_file():
#     con = sqlite3.connect("Input_Files.db")
#     con.row_factory = sqlite3.Row
#     cur = con.cursor()
#     cur.execute("select * from data")
#     data = cur.fetchall()
#     con.close()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        new_banana = Temp(banana="new")
        db.session.add(new_user)
        db.session.add(new_banana)
        db.session.commit()
        return '<h1> New user'

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user = User.query.filter_by(username=form.username.data).first()
    if user:
        if check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('ExcelUpload'))
    return render_template('login.html', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/ExcelUpload', methods=['GET', 'POST'])
@login_required
def ExcelUpload():
    if request.method == 'POST':
        uploadExcel = request.files['uploadExcel']
        if uploadExcel.filename != '':
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], uploadExcel.filename)
            uploadExcel.save(filepath)
            con = sqlite3.connect("Input_Files.db")
            cur = con.cursor()
            cur.execute("insert into data(exceldata)values(?)", (uploadExcel.filename,))
            con.commit()
            flash("Excel Sheet Upload Successfully", "success")
            con = sqlite3.connect("Input_Files.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("select * from data")
            data = cur.fetchall()
            con.close()
            return render_template("ExcelUpload.html", data=data)
    else:
        con = sqlite3.connect("Input_Files.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from data")
        data = cur.fetchall()
        con.close()
        return render_template("ExcelUpload.html", data=data)

    return render_template("ExcelUpload.html")


@app.route('/view_excel/<string:id>')
def view_excel(id):
    con = sqlite3.connect("Input_Files.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from data where pid=?", (id))
    data = cur.fetchall()
    print(data)
    for val in data:
        path = os.path.join("static/Excel/", val[1])
        print(val[1])
        data = pd.read_csv(path)
    con.close()
    return render_template("view_excel.html",
                           data=data.to_html(index=False, classes="table table-bordered").replace('<th>',
                                                                                                  '<th style="text-align:center">'))



@app.route('/delete_record/<string:id>')
def delete_record(id):
    try:
        con = sqlite3.connect("Input_Files.db")
        cur = con.cursor()
        cur.execute("delete from data where pid=?", [id])
        con.commit()
        flash("Record Deleted Successfully", "success")
        return redirect(url_for("ExcelUpload"))
        con.close()
    except:
        flash("Record Deleted Failed", "danger")
    # finally:
    #     return redirect(url_for("ExcelUpload"))
    #     con.close()


@app.route('/assign', methods=['GET', 'POST'])
def assign():
    arr = []
    for root, dirs, files in os.walk(os.path.abspath("./static/Excel")):
        for file in files:
            arr.append(os.path.join(root, file))
    print(arr[0], arr[1])
    tasks = arr[1].replace(r"C:\Users\Yael Hadad\PycharmProjects\FinalProject\code_for_project", '.')
    workers = arr[0].replace(r"C:\Users\Yael Hadad\PycharmProjects\FinalProject\code_for_project", '.')
    print(tasks, workers)

    try:
        os.system("python main.py -tasks %s -workers %s" % (tasks, workers))
    except Exception:
        print("Exception in user code:")
        traceback.print_exc(file=sys.stdout)

    return redirect(url_for('index'))


@app.route('/exit_view', methods=['GET', 'POST'])
def exit_view():
    return redirect(url_for("ExcelUpload"))

if __name__ == '__main__':
    app.run(debug=False)
