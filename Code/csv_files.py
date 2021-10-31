from flask import request
from io import TextIOWrapper
import csv
import sys


class ThreatStackError(Exception):
    def rin(self):
        return '<h1> Invalid format'



def csv_upload(Tasks, Workers, user_projects, db, manager, project):
  try:
    if request.files.get('upload_tasks'):
        tasks_csv = request.files['upload_tasks']
        tasks_csv = TextIOWrapper(tasks_csv, encoding='utf-8')
        csv_reader_tasks = csv.reader(tasks_csv, delimiter=',')
        if db.session.query(Tasks).filter_by(Manager="%s" % manager, Project="%s" % project).count() >= 1:
            try:
                db.session.query(Tasks).filter_by(Manager="%s" % manager, Project="%s" % project).delete()
                db.session.commit()
            except:
                return '<h1> Invalid format of the file. For mor details, read the tutorial'
        try:
            first_row = next(csv_reader_tasks)
        except:
             return '<h1> Invalid file, load csv file'
        for row in csv_reader_tasks:
            task = Tasks(ID_Task=row[0], Status=row[1], Description=row[2], Subject=row[3], Assignee=row[4],
                            Queue=float(row[5]), Allotted_time=float(row[6]), Review_Time=float(row[7]), Manager=manager,
                            Project=user_projects[manager])
            db.session.add(task)
            db.session.commit()


    if request.files.get('upload_workers'):
        workers_csv = request.files['upload_workers']
        workers_csv = TextIOWrapper(workers_csv, encoding='utf-8')
        csv_reader_workers = csv.reader(workers_csv, delimiter=',')
        try:
            if db.session.query(Workers).filter_by(Manager="%s" % manager, Project="%s" % project).count() >= 1:
                db.session.query(Workers).filter_by(Manager="%s" % manager, Project="%s" % project).delete()
                db.session.commit()
        except:
                return '<h1> Invalid format of the file. For mor details, read the tutorial'

        try:
            first_row = next(csv_reader_workers)
        except:
            return '<h1> Invalid file, load csv file'
        for row in csv_reader_workers:
            try:
                worker = Workers(Name=row[0], Role=row[1], Total_hours=float(row[2]), Total_hours_at_begin=float(row[3]),
                             Expertise=row[4], Budget='', Manager=manager, Project=user_projects[manager])
                db.session.add(worker)
                db.session.commit()
            except:
                return '<h1> Invalid format of the file. For mor details, read the tutorial'
  except request.exceptions.RequestException as e:
    exc_info = sys.exc_info()
    raise ThreatStackError.rin
