import pandas as pd
from task import Task
from worker import Worker
from Generate_Tasks import Gen_Task
from Read_Config import Config
import argparse
import math


def parse_args():
    parser = argparse.ArgumentParser(description='''Generate tasks for each user''')
    parser.add_argument('-tasks', type=str,
                        help='path to tasks xls file', required=True)
    parser.add_argument('-config', type=str,
                        help='path to config file', required=True)
    args = parser.parse_args()

    return args



### from the tasks file, generate all_tasks and set priority

### from the configure file generate te task to worker table

def main():
    args = parse_args()
    ## Valdaion if one of the file does not exits, test for it
    df_config = pd.read_csv(args.config)
    df_tasks = pd.read_csv(args.tasks)
    tasks = Gen_Task(df_tasks)
    tasks.run()
    config = Config(df_config,tasks.all_tasks)
    config.run()


main()


# read the ask to worker table and:
# 1)sort by worker
# 2) Validation
# 3)fill another information for each task in the tavbe
# e.g- how much unique for the worker less than it


# Procssing- the algoritem