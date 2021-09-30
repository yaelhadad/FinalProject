import numpy as np
from constants import Constants


def assign_task(task, worker):
    task.set_task(Constants.ASSIGNED, worker.name)
    worker.update_assigned_task(task)


class Assign:

    def __init__(self, config_file, all_tasks, all_workers):
        self.config_file = config_file
        self.all_tasks = all_tasks
        self.all_workers = all_workers
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
        for idx, row in df_possible_workers.iterrows():
            name = row.loc[Constants.NAME]
            budget = row.loc[Constants.BUDGET_UNIQUE]
            worker = self.all_workers[name]
            if not worker.verify_optional_task_before_devide(task, budget):
                df_possible_workers = df_possible_workers.drop(idx)
                self.remove_needless_optional_workers(idx)
        if len(df_possible_workers.index) == Constants.ONLY_ONE and task.status != Constants.ASSIGNED:
            assign_task(task, self.all_workers[df_possible_workers.iloc[Constants.ONE_AND_LAST][Constants.NAME]])
            return
        df_min_budget = df_possible_workers.sort_values(by=[Constants.BUDGET_UNIQUE])
        # Case that there is only one worker with the most minimal budget
        if df_min_budget.iloc[Constants.FIRST][Constants.BUDGET_UNIQUE] != df_min_budget.iloc[Constants.SECOND][Constants.BUDGET_UNIQUE]:
            assign_task(task, self.all_workers[df_min_budget.head(Constants.ONLY_ONE).iloc[Constants.ONE_AND_LAST][Constants.NAME]])
            self.update_workers(df_possible_workers.index, df_min_budget.head(Constants.ONLY_ONE).index)
            return
        else:
            # Case that there are many workers with the most minimal budget
            # Pick by the max availability
            worker, index_drop = self.find_worker_with_max_availability(df_min_budget)
            assign_task(task, self.all_workers[worker])
            self.remove_needless_optional_workers(index_drop)

    def run(self):
        print("asssign", self.config_file)
        self.config_file.to_csv(
            r"C:\Users\Yael Hadad\PycharmProjects\FinalProject\code_for_project\Tests\Test6\before_assign_gold.csv")
        self.config_file = self.config_file.sort_values(by=[Constants.TASK])
        # Check if the task is unique:
        for idx, row in self.config_file.iterrows():
            task = self.all_tasks[row.loc[Constants.TASK]]
            if row.loc[Constants.IS_UNIQUE]:
                assign_task(task, self.all_workers[row.loc[Constants.NAME]])
            # Decide what to do if a task appear in the optional list of multiple workers
            if not row.loc[Constants.IS_UNIQUE] and task.status != Constants.ASSIGNED:
                self.decide_who_will_assign(self.all_tasks[row.loc[Constants.TASK]])
        self.config_file.to_csv(
            r"C:\Users\Yael Hadad\PycharmProjects\FinalProject\code_for_project\Tests\Test6\after_assign_gold.csv")
