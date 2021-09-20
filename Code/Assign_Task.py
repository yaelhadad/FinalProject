from Read_Config import all_workers

TASK = "Task"
IS_UNIQUE = "Is the task Unique?"
ASSIGNED = 'assigned'
NAME = 'Name'
BUDGET_UNIQUE = 'Total time for less important unique tasks'


def get_worker(name):
    for worker in all_workers:
        if name == worker.name:
            return worker
    return None


class Assign:

    def __init__(self, config_file, all_tasks):
        self.config_file = config_file
        self.all_tasks = all_tasks

    def get_task(self, name):
        for task in self.all_tasks:
            if name == task.name:
                return task
        return None

    def update_workers (self, index, min_budget_index):
            set_difference = set(index) - set(min_budget_index)
            list_difference = list(set_difference)
            self.config_file = self.config_file.drop(list_difference)


    def assign_task(self, task, worker):

        task.set_task(ASSIGNED, worker.name)
        worker.update_assigned_task(task)

    def decide_who_will_assign(self, task):
        df = self.config_file.loc[self.config_file[TASK] == task.name]
        df_min_budget = df.sort_values(by=[BUDGET_UNIQUE]).head(1)
        for idx, row in df_min_budget.iterrows():
            name = row.loc[NAME]
        self.assign_task(task, get_worker(name))
        self.update_workers(df.index, df_min_budget.index)

    def run(self):
        self.config_file = self.config_file.sort_values(by=[TASK])
        print(self.config_file)
        print(self.all_tasks)
        print(all_workers)
        # Check if the task is unique:
        for idx, row in self.config_file.iterrows():
            if row.loc[IS_UNIQUE]:
                self.assign_task(self.get_task(row.loc[TASK]), get_worker(row.loc[NAME]))
            if row.loc[IS_UNIQUE] == False:
                self.decide_who_will_assign(self.get_task(row.loc[TASK]))
        for worker in all_workers:
            worker.print_current()
        print(self.config_file)
