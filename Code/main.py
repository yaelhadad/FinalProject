import pandas as pd
from Generate_Tasks import GenerateTask
from Read_Config import Config
from Prev_Sprint import PreviousSprint
from Budget_Unique_Tasks import BudgetUnique
from Assign_Task import Assign
from tasks_for_each_worker import TaskAssigned
from validate import Valid
import argparse
import errno
import os


def parse_args():
    parser = argparse.ArgumentParser(description='''Generate tasks for each user''')
    parser.add_argument('-tasks', type=str,
                        help='path to tasks xls file', required=True)
    parser.add_argument('-config', type=str,
                        help='path to config file', required=True)
    args = parser.parse_args()

    return args


def main():
    args = parse_args()
    if os.path.isfile(args.config) and (os.path.isfile(args.tasks)):
        df_config = pd.read_csv(args.config)
        df_tasks = pd.read_csv(args.tasks)
        Valid(df_config, df_tasks).valid_values()
        # from the tasks file, generate all_tasks and set priority
        tasks = GenerateTask(df_tasks)
        # From the configure file generate the main task to worker table
        config = Config(df_config, tasks.all_tasks)
        db_tasks_table = config.run()
        # Previous sprint update the main task to worker table
        prev = PreviousSprint(db_tasks_table)
        # Prepare Information fo the algorithm - What is the  budget of all the
        # unique tasks that are less urgent than the optional task
        budget_for_unique_tasks_table = BudgetUnique(prev.config_file).run()
        # Processing- the algorithm
        assign = Assign(budget_for_unique_tasks_table, tasks.all_tasks)
        assign_run = assign.run()
        assign_tasks = TaskAssigned(assign.config_file, config.workers).generate_tasks()
        # TBD -View availability

    else:
        if not os.path.isfile(args.config):
            print(FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), args.config))
        if not os.path.isfile(args.tasks):
            print(FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), args.tasks))






main()
