import numpy as np
from constants import Constants


class AlreadyAssigned:
    all_tasks_to_be_removed = []

    def __init__(self, possible_tasks_table):
        self.possible_tasks_table = possible_tasks_table
        self.run()

    def remove_already_assigned_tasks_from_possible_worker(self, task):
        self.possible_tasks_table = self.possible_tasks_table.drop(self.possible_tasks_table[(self.possible_tasks_table[Constants.TASK] == task) &
                                                                  (self.possible_tasks_table[
                                                                       Constants.IS_UNIQUE] == False)].index)

    def run(self):
        # List of all the assigned
        is_already_assigned = any(self.possible_tasks_table[Constants.IS_ASSIGNED].to_list())
        if is_already_assigned:
            already_assigned_tasks = self.possible_tasks_table[self.possible_tasks_table[Constants.IS_ASSIGNED]]
            already_assigned_tasks[Constants.IS_ASSIGNED_UNIQUE] = np.where(already_assigned_tasks[Constants.NAME] ==
                                                                            already_assigned_tasks[
                                                                                Constants.ALREADY_ASSIGNED], True,
                                                                            False)
            initial_assigned = already_assigned_tasks.loc[(already_assigned_tasks[Constants.IS_UNIQUE] == False) &
                                                          (already_assigned_tasks[
                                                               Constants.IS_ASSIGNED_UNIQUE] == True)].index.values
            for row in initial_assigned:
                already_assigned_tasks.at[row, Constants.IS_UNIQUE] = True
                task_to_be_updated = (already_assigned_tasks.loc[row, Constants.TASK])
                self.all_tasks_to_be_removed.append(task_to_be_updated)

            # Update the col in the possible table
            self.possible_tasks_table.update(already_assigned_tasks)
            # Remove all possible workers that are not already assigned
            for task_to_be_updated in self.all_tasks_to_be_removed:
                self.remove_already_assigned_tasks_from_possible_worker(task_to_be_updated)
