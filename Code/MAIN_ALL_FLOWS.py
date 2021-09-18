import pandas as pd
from Generate_Tasks import GenerateTask
from Read_Config import Config
from Prev_Sprint import PreviousSprint
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
    ## Valdaion if one of the file does not exits, test for it
    ## TBD
    df_config = pd.read_csv(args.config)
    df_tasks = pd.read_csv(args.tasks)

    ### from the tasks file, generate all_tasks and set priority
    tasks = GenerateTask(df_tasks)
    ### from the configure file generate the main task to worker table
    db_tasks_table = Config(df_config, tasks.all_tasks).run()
    ### Previous sprint update the main task to worker table
    prev = PreviousSprint(db_tasks_table)
    print(prev.config_file)
    ### Previous sprint:
    # 1) iterate the previous sprint
    # 2) If name is identical to the name of assigned from lase sprint:
    #          -) set this task to be unique, it will be handle in the algorithem
    #           -) remove it from the others - mabiy move it to backup list







main()


# read the task to worker table and:
# 1)sort by worker
# 2) Validation
# 3)fill another information for each task in the table
# e.g- how much unique for the worker less than it


# Procssing- the algoritem