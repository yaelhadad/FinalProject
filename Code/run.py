from flask import Flask, g, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from sqlalchemy import CheckConstraint
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length, DataRequired
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlalchemy
import pandas as pd
from io import TextIOWrapper
import sys, traceback
import csv
from constants import Constants
from csv_files import  csv_upload

import email_validator

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Task_Assigner.db'
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.secret_key = "123"
ALLOWED_EXTENSIONS = {'csv'}

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
Bootstrap(app)
all_workers_names = []
all_workers_get_task_names = {}
manager_projects = {}
user_roles = {}

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    role = db.Column(db.String(10))
    project = db.Column(db.String(10))
    password = db.Column(db.String(80))


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ID_Task = db.Column(db.String(4))
    Status = db.Column(db.String)
    Description = db.Column(db.String)
    Subject = db.Column(db.String)
    Assignee = db.Column(db.String)
    Queue = db.Column(db.Float)
    Allotted_time = db.Column(db.Float)
    Review_Time = db.Column(db.Float)
    Manager = db.Column(db.String)
    Project = db.Column(db.String)


class Workers(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    Role = db.Column(db.String)
    Total_hours = db.Column(db.Float)
    Total_hours_at_begin = db.Column(db.Float)
    Expertise = db.Column(db.String)
    Budget = db.Column(db.String)
    Manager = db.Column(db.String)
    Project = db.Column(db.String)


class Assigned(db.Model):
    __tablename__ = 'assigned'
    index = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    Expertise = db.Column(db.String)
    ID = db.Column(db.Integer)
    Description = db.Column(db.String)
    Allotted_time = db.Column(db.Float)
    Is_the_task_Unique = db.Column(db.String)
    Total_time_for_less_important_unique_tasks = db.Column(db.Float)
    Already_assigned_by = db.Column(db.String)
    Status = db.Column(db.String)
    Is_already_assigned = db.Column(db.String)
    Manager = db.Column(db.String)
    Project = db.Column(db.String)



class Impossible(db.Model):
    __tablename__ = 'impossible'

    ID = db.Column(db.Integer, primary_key=True)
    Subject = db.Column(db.String)
    Description = db.Column(db.String)
    Allotted_time = db.Column(db.Float)


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=3, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')
    project = StringField('project', validators=[InputRequired(), Length(min=4, max=15)])


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=3, max=15)])
    role = SelectField('role', validators=[DataRequired()], choices=[('manager', 'manager'), ('member', 'member')])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=8)])

def is_user_has_project(name, project):
    all_members = db.session.query(Assigned).filter_by(Name="%s" % name, Project=project)
    if all_members.count() <= 1:
        return False
    else:
        return True

def get_assigned_tasks(name, project):
    print((name, project))
    query = 'select Name, Description, Expertise, ID, Allotted_time, Status from assigned WHERE Name ="%s" ' \
            'AND Project = "%s"' % (name, project)
    engine = sqlalchemy.create_engine('sqlite:///Task_Assigner.db')
    print(pd.read_sql(query, engine))
    return pd.read_sql(query, engine)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/tutorial', methods=['GET', 'POST'])
def tutorial():
    return render_template('tutorial.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    user_roles[form.username.data] = form.role.data
    print ("signup", user_roles)
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password,role=form.role.data)
        db.session.add(new_user)
        db.session.commit()

        return render_template('welcome.html', user=form.username.data)

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user = User.query.filter_by(username=form.username.data).first()
    project = User.query.filter_by(project=form.project.data).first()
    manager_projects[form.username.data] = form.project.data
    if user:
        if check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            print ("login", user_roles)
            if User.query.filter_by(username=form.username.data).first().role== "manager":
                return redirect(url_for('upload_csv_files'))
            else:
                if is_user_has_project(form.username.data, form.project.data):
                    assigned_tasks_for_member = get_assigned_tasks(form.username.data, form.project.data)
                    print(assigned_tasks_for_member)
                    #edirect(url_for('view_tasks_for_worker(%s)' % user))
                    return render_template("view.html",
                               data=assigned_tasks_for_member.to_html(index=False, classes="table table-striped"),
                               title="Assigned task for worker")
                else:
                    return '<h1> User has no tasks'
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/welcome', methods=['GET'])
def welcome():
    return render_template('welcome.html')


@app.route('/upload_csv_files', methods=['GET', 'POST'])
@login_required
def upload_csv_files():
    print(manager_projects)
    manager = list(manager_projects)[-1]
    project = manager_projects[manager]
    if db.session.query(Assigned).filter_by(Manager="%s" % manager, Project="%s" % project).count() >= 1 :
        msg = "Note: The project '%s' exists, Notice that if you upload files you will overwrite the old files." % project
    else:
        msg = "Note: The project '%s' is a  new project, Upload your files" % project
    if request.method == 'POST':
        csv_upload(Tasks, Workers, manager_projects, db, manager, project)
        return redirect(url_for('upload_csv_files'))

    return render_template("upload_csv_files.html", msg=msg)


@app.route('/view_tasks')
def view_tasks():
    engine = sqlalchemy.create_engine('sqlite:///Task_Assigner.db')
    user = list(manager_projects)[-1]
    project = manager_projects[user]
    df = pd.read_sql(
        'select ID_Task, Status, Description, Subject, Assignee, Allotted_time, Review_Time  from tasks WHERE Manager = "%s" AND Project = "%s"' % (
        user, project), engine)
    return render_template("view.html",
                          data=df.to_html(index=False, classes="table table-striped"),
                         title="Tasks table")



@app.route('/view_workers')
def view_workers():
    engine = sqlalchemy.create_engine('sqlite:///Task_Assigner.db')
    user = list(manager_projects)[-1]
    project = manager_projects[user]
    df = pd.read_sql(
        'select Name, Total_hours, Total_hours_at_begin,Expertise from workers WHERE Manager = "%s" AND Project = "%s"' % (
            user, project), engine)
    #df = pd.read_sql('select Name,Role,Total_hours, Total_hours_at_begin,Expertise from workers ', engine)
    return render_template("view.html",
                           data=df.to_html(index=False, classes="table table-striped"),
                           title="Workers table")


@app.route('/assign', methods=['GET', 'POST'])
def assign():
    manager = list(manager_projects)[-1]
    project = manager_projects[manager]
    try:
        os.system("python main.py -manager %s -project %s" % (manager, project))
    except Exception:
        print("Exception in user code:")
        traceback.print_exc(file=sys.stdout)
    return redirect(url_for('tasks_assigned'))


@app.route('/tasks_assigned', methods=['GET', 'POST'])
def tasks_assigned():
    try:
        print("aa")
        count_tasks_for_each_worker = {}
        manager = list(manager_projects)[-1]
        project = manager_projects[manager]
        all_workers = db.session.query(Workers.Name).filter_by(Manager="%s" % manager, Project="%s" % project)
        budget_all_workers = db.session.query(Workers.Budget).filter_by(Manager="%s" % manager, Project="%s" % project)
        # all_workers = db.session.query(Workers.Name).all()
        # budget_all_workers = db.session.query(Workers.Budget).all()
        workers_get_tasks = db.session.query(Assigned).filter_by(Manager="%s" % manager, Project="%s" % project)
        for worker in workers_get_tasks:
            all_workers_get_task_names[worker.Name] = db.session.query(Assigned).filter_by(Name=worker.Name,Manager="%s" % manager, Project="%s" % project)
            count_tasks_for_each_worker[worker.Name] = all_workers_get_task_names[worker.Name].count()
        tasks_number = db.session.query(Tasks).filter_by(Manager="%s" % manager, Project="%s" % project).count()
        are_any_impossible = db.session.query(Impossible).first()
        impossible = None
        if are_any_impossible:
            count_impossible_tasks = db.session.query(Impossible).count()
            impossible_tasks = [task_impos.ID for task_impos in db.session.query(Impossible).all()]
            impossible = db.session.query(Impossible).all
            assigned_tasks_sum = str(tasks_number - count_impossible_tasks)
            if count_impossible_tasks >1:
                msg1 = "%s tasks are impossible:  %s" % (count_impossible_tasks, str(impossible_tasks))
            else:
                msg1 = "%s task is impossible:  %s" % (count_impossible_tasks, str(impossible_tasks))
            msg2 = "%s tasks were assigned." % assigned_tasks_sum

        else:
            msg1 = "All the tasks were assigned successfully!"
            msg2 = "Good Luck!"
        return render_template('tasks_assigned.html', data=all_workers, tasks_number=tasks_number,
                               msg1=msg1, msg2=msg2, count=count_tasks_for_each_worker, budget=budget_all_workers, impossible=impossible)
    except Exception:
        print("Exception in user code:")
        traceback.print_exc(file=sys.stdout)
    return redirect('upload_csv_files')


@app.route('/view_tasks_for_worker/<string:WorkerName>')
def view_tasks_for_worker(WorkerName):
    workers_tasks = {}
    for name, value in all_workers_get_task_names.items():
        df = pd.DataFrame()
        df = pd.read_sql(value.statement, db.session.bind)
        df = df.drop([Constants.IS_UNIQUE, Constants.BUDGET_UNIQUE, Constants.ALREADY_ASSIGNED, Constants.IS_ASSIGNED,
                      "Manager", "Project","index"], axis=1)
        workers_tasks[name] = df
    if WorkerName not in all_workers_get_task_names.keys():
        return 'Worker did not get tasks'
    else:
        return render_template("view.html",
                               data=workers_tasks[WorkerName].to_html(index=False, classes="table table-striped"),
                               title="Assigned task for worker")


@app.route('/exit_view', methods=['GET', 'POST'])
def exit_view():
    return redirect(url_for("index"))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=False)