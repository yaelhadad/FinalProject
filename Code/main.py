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
    workers_table = pd.read_sql('SELECT * FROM workers ', engine)
    print(type(workers_table))

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
    print(update_existing_assigned)
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

    print(processing_workers.all_impossible_tasks)
    # TBD -View availability
    print(processing_workers.all_workers.values())
    for worker in processing_workers.all_workers.values():
        budget = str(float(worker.count_current_hours) / float(worker.availability_initial) * 100) + "%"
        budget_of_all.append(budget)
    workers_table["Budget"] = budget_of_all
    workers = workers_table.to_sql('workers', engine, if_exists='replace', index=False)
    print(budget_of_all)


main()