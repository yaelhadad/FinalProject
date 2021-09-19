import pandas as pd
from Generate_Tasks import GenerateTask
from Read_Config import Config
from Prev_Sprint import PreviousSprint
from Budget_Unique_Tasks import BudgetUnique
import argparse


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
    # Validation if one of the file does not exits, test for it
    ## TBD
    df_config = pd.read_csv(args.config)
    df_tasks = pd.read_csv(args.tasks)
    all_workers = []

    # from the tasks file, generate all_tasks and set priority
    tasks = GenerateTask(df_tasks)
    # From the configure file generate the main task to worker table
    config = Config(df_config, tasks.all_tasks)
    db_tasks_table = config.run()
    # Previous sprint update the main task to worker table
    prev = PreviousSprint(db_tasks_table)
    # Prepare Information fo the algorithm - What is the  budget of all the
    # unique tasks that are less urgent than the optional task
    budget_for_unique_tasks = BudgetUnique(prev.config_file).run()

    # print(budget_for_unique_tasks.iloc[: , :8])
    # Processing- the algorithm


main()
