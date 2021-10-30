import pandas as pd
from run import db, Impossible, Assigned
import numpy as np
from generate_tasks import GenerateTask
from processing_workers_info import WorkerInfo
from already_assigned_tasks import AlreadyAssigned
from budget_unique_tasks import BudgetUnique
from assign_task import Assign
from validate import Valid, ValidWorkersFile, ValidTasksFile
import argparse
import errno
import os
import sqlalchemy

all_workers_info = {}
budget_of_all = []


def parse_args():
    parser = argparse.ArgumentParser(description='''Generate tasks for each user''')
    parser.add_argument('-manager', type=str,
                        help='The name of the manager that assign tasks', required=True)
    parser.add_argument('-project', type=str,
                        help='The name of the project', required=True)
    args = parser.parse_args()

    return args


def update_manager_and_project_assigned_tasks(assign_table, manager, project):
    assign_table['Manager'] = manager
    assign_table['Project'] = project
    return assign_table


def main():
    args = parse_args()
    engine = sqlalchemy.create_engine('sqlite:///Task_Assigner.db')
    workers_table = pd.read_sql('SELECT * FROM workers WHERE Manager = "%s" AND Project = "%s"' %(args.manager, args.project), engine)
    #workers_table = pd.read_sql('SELECT * FROM workers' , engine)
    print(workers_table)

    tasks_table = pd.read_sql('SELECT * FROM tasks WHERE Manager = "%s" AND Project = "%s"' % (args.manager, args.project), engine)
    print(tasks_table)

    # TBD - Finish the validation
    # ValidWorkersFile(workers_table).valid_values()
    # ValidTasksFile(tasks_table).valid_values()
    # from the tasks file, generate all_tasks and set priority
    tasks = GenerateTask(tasks_table)
    # From the configure file generate the "main task for worker" table
    processing_workers = WorkerInfo(workers_table, tasks.all_tasks)
    # Previous sprint update the main task to worker table

    already_assigned = AlreadyAssigned(processing_workers.df_tasks_db)

    # Prepare Information fo the algorithm - What is the  budget of all the
    # unique tasks that are less urgent than the optional task

    budget_for_unique_tasks_table = BudgetUnique(already_assigned.config_file)
    # Processing- the algorithm
    print("bbb", budget_for_unique_tasks_table.config_file.shape[0])
    assign = Assign(budget_for_unique_tasks_table.config_file, tasks.all_tasks, processing_workers.all_workers,
                    processing_workers.all_impossible_tasks)
    print ("777")
    print (assign.config_file)
    updated_assigned = update_manager_and_project_assigned_tasks(assign.config_file, args.manager, args.project)
    print(updated_assigned)

    # check if user and project already exists, then overwrite their rows, otherwise, append

    existing_assigned = pd.read_sql('assigned', engine)
    update_existing_assigned = existing_assigned
    print("888")
    # check if exists in the db the project and the manager assign
    user_and_project_in_assigned = existing_assigned[(existing_assigned.Manager == args.manager) & (existing_assigned.Project == args.project)]
    print("777")
    print(user_and_project_in_assigned)
    # if yes - drop the old, overwrie
    if not user_and_project_in_assigned.empty:
        #update_existing_assigned = existing_assigned.drop(user_and_project_in_assigned.index)
        update_existing_assigned= pd.concat([existing_assigned, user_and_project_in_assigned, user_and_project_in_assigned]).drop_duplicates(keep=False)
        print(existing_assigned)
        print("fffffffffffffffff")
        print(update_existing_assigned)
        assigned = update_existing_assigned.to_sql('assigned', engine, if_exists='replace',index=False)


    print("999")
    print(update_existing_assigned)
    print("000")
     # if it was exists or not, now this is safe to append
    if update_existing_assigned.empty:
        assigned = updated_assigned.to_sql('assigned', engine, if_exists='replace')
    else:
        assigned = updated_assigned.to_sql('assigned', engine, if_exists='append')
    if not assign.all_impossible_tasks.empty:
        impossible = assign.all_impossible_tasks.to_sql('impossible', engine, if_exists='replace')
    else:
        db.session.query(Impossible).delete()
        db.session.commit()
    print("true")
    existing_assigned2 = pd.read_sql('assigned', engine)
    print (existing_assigned2)
    print(processing_workers.all_impossible_tasks)
    # TBD -View availability
    print(processing_workers.all_workers.values())
    for worker in processing_workers.all_workers.values():
        budget = str(round(float(worker.count_current_hours) / float(worker.availability_initial) * 100,2))+ "%"
        budget_of_all.append(budget)
    ### this one is the current delta
    print ("yyyyy")
    workers_table["Budget"] = budget_of_all
    print("yyyyy2")
    #workers_table.reset_index()
    # Check if the existing workers table in sql is empty, if yes- replace
    print ("try i")
    existing_workers = pd.read_sql('workers', engine)
    #update_existing_workers = existing_workers.reset_index()
    update_existing_workers = existing_workers
    print("kkkkkkkkkkk")
    print(update_existing_workers)
    # switch all, not check each worker
    user_and_project_in_workers = existing_workers[
        (existing_workers.Manager == args.manager) & (existing_workers.Project == args.project)]
    print ("yyyy", user_and_project_in_workers)

    # if cureent project appears in sql
    if not user_and_project_in_workers.empty:
        #update_existing_assigned = existing_assigned.drop(user_and_project_in_assigned.index)
        update_existing_workers= pd.concat([existing_workers, user_and_project_in_workers, user_and_project_in_workers]).drop_duplicates(keep=False)
        print(existing_workers)
        print(update_existing_workers)
        print("fffffffffffffffff")
        e = pd.read_sql('workers', engine)
        print ("eeeee", e)
        #workers_table['index'] = range(1, len(workers_table) + 1)
        print (workers_table)

        print(workers_table)
        #workers_table.reset_index()
        # inital table
        if update_existing_workers.empty:
            workers= workers_table.to_sql('workers', engine, if_exists='replace',index=False)
            v = pd.read_sql('workers', engine)
            print("vvvvvv", v)
        # not initial table
        else:
            #+2df : existing and workers_table
            all_workers = update_existing_workers.append(workers_table)
            print ("8888", all_workers)
            workers = all_workers.to_sql('workers', engine, if_exists='replace',index=False)
            c = pd.read_sql('workers', engine)
            print("cccc", c)



    print(update_existing_workers)



    # If not empty-
    # check if this project already exists,
    #    - if yes- drop the rows,
    # if not - append

   # workers = workers_table.to_sql('workers', engine, if_exists='replace', index=False)
    print(budget_of_all)


main()