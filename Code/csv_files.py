from flask import request
from io import TextIOWrapper
import csv


def project_io_status(File, db, manager, project, Tasks, Workers, Assigned, ):
    if db.session.query(File).filter_by(Manager="%s" % manager, Project="%s" % project).count() >= 1:
        is_empty = False
    else:
        is_empty = True

    if File == Tasks:
        if not is_empty:
            is_task_file_exists = True
        else:
            is_task_file_exists = False
        return is_task_file_exists

    if File == Workers:
        if not is_empty:
            is_workers_file_exists = True
        else:
            is_workers_file_exists = False
        return is_workers_file_exists

    if File == Assigned:
        if not is_empty:
            msg = "Note: The project '%s' exists Notice that if you upload files you will overwrite the old files." % project
        else:
            msg = "Note: The project '%s' is a  new project, Tasks ere not assigned yet" % project
        return msg


def csv_upload(Tasks, Workers, user_projects, db, manager, project):
    if request.files.get('upload_tasks'):
        tasks_csv = request.files['upload_tasks']
        tasks_csv = TextIOWrapper(tasks_csv, encoding='utf-8')
        csv_reader_tasks = csv.reader(tasks_csv, delimiter=',')
        if db.session.query(Tasks).filter_by(Manager="%s" % manager, Project="%s" % project).count() >= 1:
            db.session.query(Tasks).filter_by(Manager="%s" % manager, Project="%s" % project).delete()
            db.session.commit()
        first_row = next(csv_reader_tasks)
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
        if db.session.query(Workers).filter_by(Manager="%s" % manager, Project="%s" % project).count() >= 1:
            db.session.query(Workers).filter_by(Manager="%s" % manager, Project="%s" % project).delete()
            db.session.commit()

        first_row = next(csv_reader_workers)
        for row in csv_reader_workers:
            worker = Workers(Name=row[0], Role=row[1], Total_hours=float(row[2]), Total_hours_at_begin=float(row[3]),
                             Expertise=row[4], Budget='', Manager=manager, Project=user_projects[manager])
            db.session.add(worker)
            db.session.commit()
