import pandas as pd
from login import db, Impossible, Assigned
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

def main():

    engine = sqlalchemy.create_engine('sqlite:///Task_Assigner.db')
    workers_table = pd.read_sql('SELECT * FROM workers',engine)
    print(workers_table)

    tasks_table = pd.read_sql('SELECT * FROM tasks',engine)
    print(tasks_table)


    # TBD - Finish the validation
    #ValidWorkersFile(workers_table).valid_values()
    #ValidTasksFile(tasks_table).valid_values()
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
    print("bbb",budget_for_unique_tasks_table.config_file)
    assign = Assign(budget_for_unique_tasks_table.config_file, tasks.all_tasks, processing_workers.all_workers,
                    processing_workers.all_impossible_tasks)

    assigned = assign.config_file.to_sql('assigned', engine, if_exists='replace')

    if not assign.all_impossible_tasks.empty:
        impossible = assign.all_impossible_tasks.to_sql('impossible', engine, if_exists='replace')
    else:
        db.session.query(Impossible).delete()
        db.session.commit()


    print(processing_workers.all_impossible_tasks)
    # TBD -View availability








main()
