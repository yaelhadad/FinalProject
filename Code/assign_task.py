import numpy as np
from processing_workers_info import update_impossible_tasks, create_table_impossible_tasks
from constants import Constants
import pandas as pd


def assign_task(task, worker):
    task.set_task(Constants.ASSIGNED, worker.name)
    worker.update_assigned_task(task)


class Assign:

    def __init__(self, config_file, all_tasks, all_workers, impossible_tasks):
        self.config_file = config_file
        self.all_tasks = all_tasks
        self.all_workers = all_workers
        self.all_impossible_tasks = impossible_tasks
        self.run()

    def find_worker_with_max_availability(self, df):
        for idx, row in df.iterrows():
            name = row.loc[Constants.NAME]
            worker = self.all_workers[name]
            df.at[idx, Constants.AVAILABILITY] = worker.availability
        df = df.sort_values(by=[Constants.AVAILABILITY], ascending=False)
        needless_indexes = df.index.values
        return df.iloc[Constants.FIRST][Constants.NAME], np.delete(needless_indexes, Constants.FIRST)

    def remove_needless_optional_workers(self, index_drop):
        self.config_file = self.config_file.drop(index_drop)

    def update_workers(self, index, min_budget_index):
        set_difference = set(index) - set(min_budget_index)
        list_difference = list(set_difference)
        self.config_file = self.config_file.drop(list_difference)

    def decide_who_will_assign(self, task):
        df_possible_workers = self.config_file.loc[self.config_file[Constants.TASK] == task.name]
        # If assigning a possible task for worker will prevent him to do unique task, he won't get it.
        for idx, row in df_possible_workers.iterrows():
            name = row.loc[Constants.NAME]
            budget = row.loc[Constants.BUDGET_UNIQUE]
            worker = self.all_workers[name]
            if not worker.verify_optional_task_before_assign(task, budget):
                df_possible_workers = df_possible_workers.drop(idx)
                self.remove_needless_optional_workers(idx)
        # After the filter above, there is a separate handle for each case
        # If there aren't any possible workers to do the task, update the impossible table and get out the function
        if df_possible_workers.empty:
            if self.all_impossible_tasks.empty:
                self.all_impossible_tasks = create_table_impossible_tasks()
            update_impossible_tasks(self.all_impossible_tasks, int(task.identifier), task.subject, task.description,
                                    float(task.allotted_time))
            self.config_file = self.config_file[self.config_file.ID != task.identifier]
            task.status = Constants.IMPOSSIBLE
            return
        # If there is 1 possible worker now to do the task, assign it and get out the function
        if len(df_possible_workers.index) == Constants.ONLY_ONE and task.status != Constants.ASSIGNED:
            assign_task(task, self.all_workers[df_possible_workers.iloc[Constants.ONE_AND_LAST][Constants.NAME]])
            return
        # Sorting the workers according to the budget for their unique tasks
        df_min_budget = df_possible_workers.sort_values(by=[Constants.BUDGET_UNIQUE])
        # Case that there is only one worker with the most minimal budget - will assign the task
        # The purpose is that other more busy members will have enough time to do their own big unique tasks
        if df_min_budget.iloc[Constants.FIRST][Constants.BUDGET_UNIQUE] != df_min_budget.iloc[Constants.SECOND][
            Constants.BUDGET_UNIQUE]:
            assign_task(task, self.all_workers[
                df_min_budget.head(Constants.ONLY_ONE).iloc[Constants.ONE_AND_LAST][Constants.NAME]])
            self.update_workers(df_possible_workers.index, df_min_budget.head(Constants.ONLY_ONE).index)
            return
        else:
            # Case that there are many workers with the most minimal budget
            # Pick by the max availability
            worker, index_drop = self.find_worker_with_max_availability(df_min_budget)
            assign_task(task, self.all_workers[worker])
            self.remove_needless_optional_workers(index_drop)

    def run(self):

        self.config_file[Constants.MANAGER] = pd.Series(dtype='str')
        self.config_file[Constants.PROJECT] = pd.Series(dtype='str')
        self.config_file = self.config_file.sort_values(by=[Constants.TASK])

        for idx, row in self.config_file.iterrows():
            task = self.all_tasks[row.loc[Constants.TASK]]
            # Check if the task is unique:
            if row.loc[Constants.IS_UNIQUE]:
                assign_task(task, self.all_workers[row.loc[Constants.NAME]])
            # Decide what to do if a task appears in the optional list of multiple workers
            if not row.loc[Constants.IS_UNIQUE] and task.status not in (Constants.ASSIGNED, Constants.IMPOSSIBLE):
                self.decide_who_will_assign(self.all_tasks[row.loc[Constants.TASK]])

        # self.config_file.to_csv(
        #     r"C:\Users\Yael Hadad\Desktop\She codes\project_demo\appendix\Artzy family - appendix\results\assign.csv",
        #     index=False)