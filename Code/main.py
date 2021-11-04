import pandas as pd
import argparse
import sqlalchemy

from run import db, Impossible, Assigned
from generate_tasks import GenerateTask
from processing_workers_info import WorkerInfo
from already_assigned_tasks import AlreadyAssigned
from budget_unique_tasks import BudgetUnique
from assign_task import Assign
from constants import Constants


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
    assign_table[Constants.MANAGER] = manager
    assign_table[Constants.PROJECT] = project
    return assign_table


def main():
    args = parse_args()
    engine = sqlalchemy.create_engine('sqlite:///Task_Assigner.db')
    workers_table = pd.read_sql(
        'SELECT * FROM workers WHERE Manager = "%s" AND Project = "%s"' % (args.manager, args.project), engine)
    tasks_table = pd.read_sql(
        'SELECT * FROM tasks WHERE Manager = "%s" AND Project = "%s"' % (args.manager, args.project), engine)

    # Read the tasks file ans keep all the information for each task in separate class
    # Sort the class ans set them unique priority, e.g A1, A2, A3
    tasks = GenerateTask(tasks_table)
    # From the configure file generate the "main task for worker" table
    processing_workers = WorkerInfo(workers_table, tasks.all_tasks)
    # Already assigned
    already_assigned = AlreadyAssigned(processing_workers.all_possible_tasks)
    # Prepare Information fo the algorithm - What is the  budget of all the
    # unique tasks that are less urgent than the optional task
    budget_for_unique_tasks_table = BudgetUnique(already_assigned.possible_tasks_table)
    # Processing- the algorithm

    assign = Assign(budget_for_unique_tasks_table.config_file, tasks.all_tasks, processing_workers.all_workers,
                    processing_workers.all_impossible_tasks)

    updated_assigned = update_manager_and_project_assigned_tasks(assign.config_file, args.manager, args.project)

    # check if user and project already exists, then overwrite their rows, otherwise, append

    existing_assigned = pd.read_sql('assigned', engine)
    update_existing_assigned = existing_assigned
    # check if exists in the db the project and the manager assign
    user_and_project_in_assigned = existing_assigned[
        (existing_assigned.Manager == args.manager) & (existing_assigned.Project == args.project)]

    # if yes - drop the old, overwrie
    if not user_and_project_in_assigned.empty:
        # update_existing_assigned = existing_assigned.drop(user_and_project_in_assigned.index)
        update_existing_assigned = pd.concat(
            [existing_assigned, user_and_project_in_assigned, user_and_project_in_assigned]).drop_duplicates(keep=False)
        assigned = update_existing_assigned.to_sql('assigned', engine, if_exists='replace', index=False)

    # if it was exists or not, now this is safe to append
    if update_existing_assigned.empty:
        assigned = updated_assigned.to_sql('assigned', engine, if_exists='replace')
    else:
        assigned = updated_assigned.to_sql('assigned', engine, if_exists='append')
    if not assign.all_impossible_tasks.empty:
        impossible = assign.all_impossible_tasks.to_sql('impossible', engine, if_exists='replace', index=False)
    else:
        db.session.query(Impossible).delete()
        db.session.commit()

    for worker in processing_workers.all_workers.values():
        budget = str(round(float(worker.count_current_hours) / float(worker.availability_initial) * 100, 2)) + "%"
        budget_of_all.append(budget)

    workers_table["Budget"] = budget_of_all
    # workers_table.reset_index()
    # Check if the existing workers table in sql is empty, if yes- replace
    existing_workers = pd.read_sql('workers', engine)
    # update_existing_workers = existing_workers.reset_index()
    update_existing_workers = existing_workers
    # switch all, not check each worker
    user_and_project_in_workers = existing_workers[
        (existing_workers.Manager == args.manager) & (existing_workers.Project == args.project)]

    # if current project appears in sql
    if not user_and_project_in_workers.empty:
        # update_existing_assigned = existing_assigned.drop(user_and_project_in_assigned.index)
        update_existing_workers = pd.concat(
            [existing_workers, user_and_project_in_workers, user_and_project_in_workers]).drop_duplicates(keep=False)

        # inital table
        if update_existing_workers.empty:
            workers = workers_table.to_sql('workers', engine, if_exists='replace', index=False)
        # not initial table
        else:
            # +2df : existing and workers_table
            all_workers = update_existing_workers.append(workers_table)
            workers = all_workers.to_sql('workers', engine, if_exists='replace', index=False)


main()
