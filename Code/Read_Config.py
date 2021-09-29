import pandas as pd
from worker import Worker
import Defs

all_workers = []
all_impossible_tasks = []


def update_initial_information_db_table(db, name, subject, task, is_unique, i):
    if task.sprint == Defs.PREV:
        assignee = task.assignee
    else:
        assignee = None
    new_info = [name, subject, task.name, task.description, task.identifier, task.allotted_time, is_unique, 0,
                task.sprint, task.status, assignee]
    db.loc[i] = new_info


def create_db_possible_tasks():
    column_names = [Defs.NAME, Defs.EXPERTISE, Defs.TASK, Defs.DESCRIPTION, Defs.IDENTIFIER, Defs.ALLOTTED_TIME,
                    Defs.IS_UNIQUE, Defs.BUDGET_FOR_UNIQUE_BELLOW, Defs.SPRINT, Defs.STATUS, Defs.IS_ASSIGNED]
    db = pd.DataFrame(columns=column_names)
    return db


class Config:

    def __init__(self, config_file, all_tasks):
        self.config_file = config_file
        self.all_tasks = all_tasks
        self.workers = all_workers

    def set_worker(self, worker_info):
        name = self.config_file.loc[worker_info, Defs.NAME]
        role = self.config_file.loc[worker_info, Defs.ROLE]
        availability = self.config_file.loc[worker_info, Defs.TOTAL]
        availability_start = self.config_file.loc[worker_info, Defs.TOTAL_START]
        expertise = self.config_file.loc[worker_info, Defs.EXPERTISE]
        locals()[name] = Worker(name, None, role, expertise, availability, availability_start, 0, [])
        all_workers.append(locals()[name])

    @staticmethod
    def who_can_do_it(task):
        possible_workers = []
        for worker in all_workers:
            if (task.subject in worker.expertise) and (worker.enough_time(task)):
                possible_workers.append(worker)
        return possible_workers

    def run(self):
        for idx, row in self.config_file.iterrows():
            self.set_worker(idx)
        df_tasks_db = create_db_possible_tasks()
        i = 0
        for task in self.all_tasks:
            subject = task.subject
            possible_workers = self.who_can_do_it(task)
            if len(possible_workers) == Defs.ONE:
                update_initial_information_db_table(df_tasks_db, possible_workers[0].name, subject, task, Defs.UNIQUE,
                                                    i)
                i += 1
            if len(possible_workers) > Defs.ONE:
                for pos_worker in possible_workers:
                    update_initial_information_db_table(df_tasks_db, pos_worker.name, subject, task, Defs.NOT_UNIQUE, i)
                    i += 1
            if len(possible_workers) == Defs.ZERO:
                all_impossible_tasks.append(task)
                print(str(task.identifier) + ' ' + task.name + Defs.IMPOSSIBLE)

        print(df_tasks_db)
        return df_tasks_db
