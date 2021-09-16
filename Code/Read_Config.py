import pandas as pd
from worker import Worker

all_workers = []

NAME = "Name"
ROLE = "Role"
TOTAL = "Total hours"
TOTAL_START = "Total hours at begin"
EXPERTISE = "Expertise"
TASK = "Task"
ALLOTTED_TIME = "Allotted time"
BUDGET_FOR_UNIQUE_BELLOW = "Total time for less important unique tasks"
IS_UNIQUE = "Is the task Unique?"
SPRINT = "Sprint"
STATUS = "Status"
DESCRIPTION = "Description"
IDENTIFIER = "ID"
IS_ASSIGNED = "Assigned from last sprint"
PREV = 'Previous'
ONE = 1
UNIQUE = True
NOT_UNIQUE = False


def update_initial_information_db_table(db, name, subject, task, is_unique, i):
    if task.sprint == PREV:
        assignee = task.assignee
    else:
        assignee = None
    new_info = [name, subject, task.name, task.description, task.identifier, task.allotted_time, is_unique, 0,
                task.sprint, task.status, assignee]
    db.loc[i] = new_info


def create_db_possible_tasks():
    column_names = [NAME, EXPERTISE, TASK, DESCRIPTION, IDENTIFIER, ALLOTTED_TIME, IS_UNIQUE,
                    BUDGET_FOR_UNIQUE_BELLOW, SPRINT, STATUS, IS_ASSIGNED]
    db = pd.DataFrame(columns=column_names)
    return db


class Config:

    def __init__(self, config_file, all_tasks):
        self.config_file = config_file
        self.all_tasks = all_tasks

    def set_worker(self, worker_info):
        name = self.config_file.loc[worker_info, NAME]
        role = self.config_file.loc[worker_info, ROLE]
        availability = self.config_file.loc[worker_info, TOTAL]
        availability_start = self.config_file.loc[worker_info, TOTAL_START]
        expertise = self.config_file.loc[worker_info, EXPERTISE]
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
            if len(possible_workers) == ONE:
                update_initial_information_db_table(df_tasks_db, possible_workers[0].name, subject, task, UNIQUE, i)
                i += 1
            else:
                for pos_worker in possible_workers:
                    update_initial_information_db_table(df_tasks_db, pos_worker.name, subject, task, NOT_UNIQUE, i)
                    i += 1

        print(df_tasks_db)
        df_tasks_db.to_csv(r"C:\Users\Yael Hadad\PycharmProjects\FinalProject\code_for_project\Tests\Test2\temp_db_table.csv")
