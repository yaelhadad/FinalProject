from constants import Constants
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import declarative_base
from flask import Flask
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users_Info.db'
db = SQLAlchemy(app)


class Assigned(db.Model):
    __tablename__ ='assigned'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    Expertise = db.Column(db.String)
    ID = db.Column(db.Integer)
    Description = db.Column(db.String)
    Allotted_time = db.Column(db.String)
    Is_the_task_Unique = db.Column(db.String)
    Total_time_for_less_important_unique_tasks = db.Column(db.String)
    Sprint = db.Column(db.String)
    Assigned_from_last_sprint = db.Column(db.String)

class TaskAssigned:

    def __init__(self, config_file, all_workers):
        self.config_file = config_file
        self.workers = all_workers
        self.results_of_assign = {}

    def generate_tasks(self):
        print(type(self.config_file))
        dfs = dict(tuple(self.config_file.groupby(Constants.NAME)))

        print(dfs)
        print (self.config_file)
        engine = sqlalchemy.create_engine('sqlite:///Users_Info.db')
        assigned = self.config_file.to_sql('assigned', engine, if_exists='replace')


        #self.results_of_assign = dfsselect * from
        for worker in self.workers.values():
            print(worker.name)
            try:
                df = dfs[worker.name]
                df.to_csv(r"C:\Users\Yael Hadad\PycharmProjects\FinalProject\Code\results\%s.csv"
                          % worker.name)
            except:
                print(f'{worker.name} did not get tasks')

        for worker in self.workers.values():
            worker.print_current()
