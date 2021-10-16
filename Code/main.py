import pandas as pd
from login import db,app
import numpy as np
from generate_tasks import GenerateTask
from processing_workers_info import WorkerInfo
from prev_sprint import PreviousSprint
from budget_unique_tasks import BudgetUnique
from assign_task import Assign
from tasks_for_each_worker import TaskAssigned
from validate import Valid, ValidWorkersFile, ValidTasksFile
import argparse
import errno
import os
import sqlalchemy

def main():

    engine =sqlalchemy.create_engine('sqlite:///Users_Info.db')
    workers_table = pd.read_sql('SELECT * FROM workers',engine)
    print (workers_table)

    tasks_table = pd.read_sql('SELECT * FROM tasks',engine)
    print(tasks_table)


    # TBD - Finish the validation
    ValidWorkersFile(workers_table).valid_values()
    ValidTasksFile(tasks_table).valid_values()
    # from the tasks file, generate all_tasks and set priority
    tasks = GenerateTask(tasks_table)
    # From the configure file generate the "main task foo worker" table
    processing_workers = WorkerInfo(workers_table, tasks.all_tasks)
    # Previous sprint update the main task to worker table
    prev = PreviousSprint(processing_workers.df_tasks_db)

    # Prepare Information fo the algorithm - What is the  budget of all the
    # unique tasks that are less urgent than the optional task
    budget_for_unique_tasks_table = BudgetUnique(prev.config_file)
    # Processing- the algorithm
    assign = Assign(budget_for_unique_tasks_table.config_file, tasks.all_tasks, processing_workers.all_workers,
                    processing_workers.all_impossible_tasks)
    assign_tasks_for_each_worker = TaskAssigned(assign.config_file, processing_workers.all_workers).generate_tasks()
    print(processing_workers.all_impossible_tasks)
    # TBD -View availability








main()
