import pandas as pd
from worker import Worker
from constants import Constants
from validate import Valid, ValidPosTasks


def create_db_possible_tasks():
    db = pd.DataFrame({Constants.NAME: pd.Series(dtype='str'),
                       Constants.EXPERTISE: pd.Series(dtype='str'),
                       Constants.TASK: pd.Series(dtype='str'),
                       Constants.DESCRIPTION: pd.Series(dtype='str'),
                       Constants.IDENTIFIER: pd.Series(dtype='int'),
                       Constants.ALLOTTED_TIME: pd.Series(dtype='float'),
                       Constants.IS_UNIQUE: pd.Series(dtype='bool'),
                       Constants.BUDGET_FOR_UNIQUE_BELLOW: pd.Series(dtype='float'),
                       Constants.ALREADY_ASSIGNED: pd.Series(dtype='str'),
                       Constants.STATUS: pd.Series(dtype='str'),
                       Constants.IS_ASSIGNED: pd.Series(dtype='bool')})
    return db


def update_initial_information_db_table(db, name, subject, task, is_unique, i):
    new_info = [name, subject, task.name, task.description, task.identifier, task.allotted_time, is_unique, 0,
                task.assignee, task.status, task.already_assigned]
    db.loc[i] = new_info


def create_db_impossible_tasks():
    db = pd.DataFrame({Constants.IDENTIFIER: pd.Series(dtype='int'),
                       Constants.SUBJECT: pd.Series(dtype='str'),
                       Constants.DESCRIPTION: pd.Series(dtype='str'),
                       Constants.ALLOTTED_TIME: pd.Series(dtype='float')})
    return db


def update_impossible_tasks(db, id, subject, description, allotted_time):
    new_info = [id, subject, description, allotted_time]
    db.loc[len(db)] = new_info


class WorkerInfo:

    def __init__(self, config_file, all_tasks):
        self.config_file = config_file
        self.all_tasks = all_tasks
        self.all_workers = {}
        self.all_impossible_tasks = pd.DataFrame()
        self.df_tasks_db = None
        self.run()

    def set_worker(self, worker_info):
        name = self.config_file.loc[worker_info, Constants.NAME]
        role = self.config_file.loc[worker_info, Constants.ROLE]
        availability = float(self.config_file.loc[worker_info, Constants.TOTAL])
        availability_start = float(self.config_file.loc[worker_info, Constants.TOTAL_START])
        expertise = self.config_file.loc[worker_info, Constants.EXPERTISE]
        return Worker(name, None, role, expertise, availability, availability_start, count_current_hours=0,
                      current_tasks=[])

    def set_all_workers(self):
        for worker_info, each_worker in self.config_file.iterrows():
            worker = self.set_worker(worker_info)
            self.all_workers[worker.name] = worker

    def who_can_do_it(self, task):
        possible_workers = []
        for worker in self.all_workers.values():
            if (task.subject in worker.expertise) and (worker.enough_time(task)):
                possible_workers.append(worker)
        return possible_workers

    def update_initial_impossible_tasks(self, id, subject, description, allotted_time, i):
        new_info = [id, subject, description, allotted_time]
        self.all_impossible_tasks.loc[i] = new_info

    def run(self):
        self.set_all_workers()
        self.df_tasks_db = create_db_possible_tasks()
        ## index for possible tasks
        i = 0
        ## index for impossible tasks
        j = 0
        possible_workers = []
        self.all_impossible_tasks = create_db_impossible_tasks()
        for task in self.all_tasks.values():
            subject = task.subject
            possible_workers = self.who_can_do_it(task)
            if len(possible_workers) == Constants.ONE:
                update_initial_information_db_table(self.df_tasks_db, possible_workers[0].name, subject, task,
                                                    Constants.UNIQUE,
                                                    i)
                i += 1

            if len(possible_workers) > Constants.ONE:
                for pos_worker in possible_workers:
                    update_initial_information_db_table(self.df_tasks_db, pos_worker.name, subject, task,
                                                        Constants.NOT_UNIQUE, i)
                    i += 1

            if len(possible_workers) == Constants.ZERO:
                self.update_initial_impossible_tasks(task.identifier, task.subject, task.description,
                                                     task.allotted_time, j)
                j += 1
