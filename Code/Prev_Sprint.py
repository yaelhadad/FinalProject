import numpy as np
import pandas as pd

ASSIGNED_PREV = 'Assigned from last sprint'
IS_ASSIGNED_UNIQUE = "Is assigned unique?"
NAME = 'Name'
PREVIOUS = "Previous"
IS_UNIQUE = "Is the task Unique?"
UPDATE_UNIQUE = "Should be update as unique?"
Removed = "Should be removed?"
TASK = "Task"


class PreviousSprint:

    all_tasks_to_be_removed = []

    def __init__(self, config_file):
        self.config_file = config_file
        self.backup = pd.DataFrame()
        self.run()

    def remove_tasks_prev_sprint_from_possible_worker(self, task):
        self.backup = self.backup.append(self.config_file[(self.config_file[TASK] == task) &
                                                          (self.config_file[IS_UNIQUE] == False)])
        self.config_file = self.config_file.drop(self.config_file[(self.config_file[TASK] == task) &

                                                                  (self.config_file[IS_UNIQUE] == False)].index)

    def run(self):
        is_prev_sprint = self.config_file.Sprint == PREVIOUS
        df_prev_sprint = self.config_file.loc[is_prev_sprint]
        df_prev_sprint[IS_ASSIGNED_UNIQUE] = np.where(df_prev_sprint[NAME] == df_prev_sprint[ASSIGNED_PREV],
                                                      True, False)

        prev_sprint_assigned = df_prev_sprint.loc[(df_prev_sprint[IS_UNIQUE] == False) &
                                                  (df_prev_sprint[IS_ASSIGNED_UNIQUE] == True)].index.values
        for row in prev_sprint_assigned:
            df_prev_sprint.at[row, IS_UNIQUE] = True
            task_to_be_updated = (df_prev_sprint.loc[row, TASK])
            self.all_tasks_to_be_removed.append(task_to_be_updated)

        self.config_file.update(df_prev_sprint)
        for task_to_be_updated in self.all_tasks_to_be_removed:
            self.remove_tasks_prev_sprint_from_possible_worker(task_to_be_updated)

        self.config_file.to_csv(
            r"C:\Users\Yael Hadad\PycharmProjects\FinalProject\code_for_project\Tests\Test3\temp_db_table_gold.csv")
        self.backup.to_csv(
            r"C:\Users\Yael Hadad\PycharmProjects\FinalProject\code_for_project\Tests\Test3\back_up_prev_sprint_gold.csv")
