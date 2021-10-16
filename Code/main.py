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

#
# def parse_args():
#     parser = argparse.ArgumentParser(description='''Generate tasks for each user''')
#     parser.add_argument('-tasks', type=str,
#                         help='path to tasks xls file', required=True)
#     parser.add_argument('-workers', type=str,
#                         help='path to config file', required=True)
#     args = parser.parse_args()
#
#     return args


def main():
    # df = pd.read_csv(
    #     r"C:\Users\Yael Hadad\Desktop\She codes\Final project\UnitTesting\WorkerInfo\before_assign_gold.csv")
    # args = parse_args()
    # if not os.path.isfile(args.workers):
    #     print(FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), args.config))
    #     return
    # if not os.path.isfile(args.tasks):
    #     print(FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), args.tasks))
    #     return
    engine =sqlalchemy.create_engine('sqlite:///Users_Info.db')
    workers_table = pd.read_sql('SELECT * FROM workers',engine)
    print (workers_table)

    tasks_table = pd.read_sql('SELECT * FROM tasks',engine)
    print(tasks_table)


   #  workers_table1 = pd.read_csv(args.workers)
   # # print (workers_table1)
   #  workers_table1.insert(loc=0, column='id', value=np.arange(len(workers_table1)))
   #  workers_table1['id'] = workers_table1['id']+ 1
    #print (workers_table1)

    # tasks_table1 = pd.read_csv(args.tasks)
    # tasks_table1.insert(loc=0, column='id', value=np.arange(len(tasks_table1)))
    # tasks_table1['id'] = tasks_table1['id'] + 1
    # print (tasks_table1)
    # TBD - Finish the validation
    #ValidWorkersFile(workers_table).valid_values()
    #ValidTasksFile(tasks_table).valid_values()
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
    print ("000")
    assign = Assign(budget_for_unique_tasks_table.config_file, tasks.all_tasks, processing_workers.all_workers,
                    processing_workers.all_impossible_tasks)
    print ("11")
    assign_tasks_for_each_worker = TaskAssigned(assign.config_file, processing_workers.all_workers).generate_tasks()
    # TBD -View availability








main()
