import numpy as np
from Read_Config import all_workers

TASK = "Task"
IS_UNIQUE = "Is the task Unique?"
ASSIGNED = 'assigned'
STATUS = "Status"
NAME = 'Name'
BUDGET_UNIQUE = 'Total time for less important unique tasks'
ONLY_ONE = 1
ONE = -1
AVAILABILITY = "availability"
FIRST = 0


def get_worker(name):
    for worker in all_workers:
        if name == worker.name:
            return worker
    return None


def assign_task(task, worker):
    task.set_task(ASSIGNED, worker.name)
    worker.update_assigned_task(task)


def find_worker_with_max_availability(df):
    for idx, row in df.iterrows():
        name = row.loc[NAME]
        worker = get_worker(name)
        df.at[idx, AVAILABILITY] = worker.availability
    df = df.sort_values(by=[AVAILABILITY], ascending=False)
    needless_indexes = df.index.values
    return df.iloc[FIRST][NAME], np.delete(needless_indexes, FIRST)


class Assign:

    def __init__(self, config_file, all_tasks):
        self.config_file = config_file
        self.all_tasks = all_tasks

    def get_task(self, name):
        for task in self.all_tasks:
            if name == task.name:
                return task
        return None

    def update_workers(self, index, min_budget_index):
        set_difference = set(index) - set(min_budget_index)
        list_difference = list(set_difference)
        self.config_file = self.config_file.drop(list_difference)

    def decide_who_will_assign(self, task):
        df_possible_workers = self.config_file.loc[self.config_file[TASK] == task.name]
        for idx, row in df_possible_workers.iterrows():
            name = row.loc[NAME]
            budget = row.loc[BUDGET_UNIQUE]
            worker = get_worker(name)
            if not worker.verify_optional_task_before_devide(task, budget):
                df_possible_workers = df_possible_workers.drop(idx)
                self.config_file = self.config_file.drop(idx)
        if len(df_possible_workers.index) == ONLY_ONE and task.status != ASSIGNED:
            assign_task(task, get_worker(df_possible_workers.iloc[ONE][NAME]))
            return
        df_min_budget = df_possible_workers.sort_values(by=[BUDGET_UNIQUE])
        # Case that there is only one worker with the most minimal budget
        if df_min_budget.iloc[0][BUDGET_UNIQUE] != df_min_budget.iloc[1][BUDGET_UNIQUE]:
            assign_task(task, get_worker(df_min_budget.head(1).iloc[ONE][NAME]))
            self.update_workers(df_possible_workers.index, df_min_budget.head(1).index)
            return
        else:
            # Case that there are many workers with the most minimal budget
            # Pick by the max availability
            worker, index_drop = find_worker_with_max_availability(df_min_budget)
            assign_task(task, get_worker(worker))
            self.config_file = self.config_file.drop(index_drop)

    def run(self):
        print(self.config_file)
        self.config_file.to_csv(
            r"C:\Users\Yael Hadad\PycharmProjects\FinalProject\code_for_project\Tests\Test6\before_assign_gold.csv")
        self.config_file = self.config_file.sort_values(by=[TASK])
        # Check if the task is unique:
        for idx, row in self.config_file.iterrows():
            task = self.get_task(row.loc[TASK])
            if row.loc[IS_UNIQUE]:
                assign_task(task, get_worker(row.loc[NAME]))
            # Decide what to do if a task appear in the optional list of multiple workers
            if not row.loc[IS_UNIQUE] and task.status != ASSIGNED:
                self.decide_who_will_assign(self.get_task(row.loc[TASK]))
        self.config_file.to_csv(
            r"C:\Users\Yael Hadad\PycharmProjects\FinalProject\code_for_project\Tests\Test6\after_assign_gold.csv")
