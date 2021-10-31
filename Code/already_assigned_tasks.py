import numpy as np
import pandas as pd
from constants import Constants


class AlreadyAssigned:
    all_tasks_to_be_removed = []

    def __init__(self, config_file):
        self.config_file = config_file
        self.run()

    def remove_already_assigned_tasks_prev_sprint_from_possible_worker(self, task):
        self.config_file = self.config_file.drop(self.config_file[(self.config_file[Constants.TASK] == task) &
                                                                  (self.config_file[
                                                                       Constants.IS_UNIQUE] == False)].index)

    def run(self):

        is_already_assigned = any(self.config_file[Constants.IS_ASSIGNED].to_list())
        if is_already_assigned:
            already_assigned_tasks = self.config_file[self.config_file[Constants.IS_ASSIGNED]]
            already_assigned_tasks[Constants.IS_ASSIGNED_UNIQUE] = np.where(already_assigned_tasks[Constants.NAME] ==
                                                                            already_assigned_tasks[Constants.ALREADY_ASSIGNED], True, False)
            initial_assigned = already_assigned_tasks.loc[(already_assigned_tasks[Constants.IS_UNIQUE] == False) &
                                                  (already_assigned_tasks[Constants.IS_ASSIGNED_UNIQUE] == True)].index.values
            for row in initial_assigned:
                already_assigned_tasks.at[row, Constants.IS_UNIQUE] = True
                task_to_be_updated = (already_assigned_tasks.loc[row, Constants.TASK])
                self.all_tasks_to_be_removed.append(task_to_be_updated)

            self.config_file.update(already_assigned_tasks)
            for task_to_be_updated in self.all_tasks_to_be_removed:
                self.remove_already_assigned_tasks_prev_sprint_from_possible_worker(task_to_be_updated)
