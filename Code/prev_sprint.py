import numpy as np
import pandas as pd
from constants import Constants

class PreviousSprint:

    all_tasks_to_be_removed = []

    def __init__(self, config_file):
        self.config_file = config_file
        self.run()

    def remove_tasks_prev_sprint_from_possible_worker(self, task):
        self.config_file = self.config_file.drop(self.config_file[(self.config_file[Constants.TASK] == task) &
                                                                  (self.config_file[Constants.IS_UNIQUE] == False)].index)

    def run(self):
        is_prev_sprint = self.config_file.Sprint == Constants.PREVIOUS
        df_prev_sprint = self.config_file.loc[is_prev_sprint]
        df_prev_sprint[Constants.IS_ASSIGNED_UNIQUE] = np.where(df_prev_sprint[Constants.NAME] ==
                                                                df_prev_sprint[Constants.ASSIGNED_PREV], True, False)

        prev_sprint_assigned = df_prev_sprint.loc[(df_prev_sprint[Constants.IS_UNIQUE] == False) &
                                                  (df_prev_sprint[Constants.IS_ASSIGNED_UNIQUE] == True)].index.values
        for row in prev_sprint_assigned:
            df_prev_sprint.at[row, Constants.IS_UNIQUE] = True
            task_to_be_updated = (df_prev_sprint.loc[row, Constants.TASK])
            self.all_tasks_to_be_removed.append(task_to_be_updated)

        self.config_file.update(df_prev_sprint)
        for task_to_be_updated in self.all_tasks_to_be_removed:
            self.remove_tasks_prev_sprint_from_possible_worker(task_to_be_updated)

        # self.config_file.to_csv(
        #     r"C:\Users\Yael Hadad\PycharmProjects\FinalProject\code_for_project\Tests\Test3\temp_db_table_gold.csv")
        # self.backup.to_csv(
        #     r"C:\Users\Yael Hadad\PycharmProjects\FinalProject\code_for_project\Tests\Test3\back_up_prev_sprint_gold.csv")
