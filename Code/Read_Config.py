import pandas as pd
from worker import Worker
from task import Task

all_workers = []
A1 = Task('A1','ATEGEN','BLA BLA', 4, None, 'A', 'New', 1,1,'current')
A2 = Task('A2','GENERAL','BLA BLA',4, None, 'A', 'New',2,2,'current')
A3 = Task('A3','GENERAL','BLA BLA',1, None, 'A', 'New',3,3,'current')
B1 = Task('B1','ATEGEN','BLA BLA', 1, None, 'B', 'New',4,1,'current')
B2 = Task('B2','STILEDITOR','BLA BLA',7, None, 'B', 'New',5,2,'current')
B3 = Task('B3','ATEGEN','BLA BLA',8, None, 'B', 'New',6,3,'current')

all_tasks = [A1, A2, A3, B1, B2, B3]


df = pd.read_csv("configure.csv")

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
IS_ASSIGNED = "Is the task assigned?"
ONE = 1
UNIQUE = True
NOT_UNIQUE = False
def set_worker(worker_info):
    name = df.loc[worker_info, NAME]
    role = df.loc[worker_info, ROLE]
    availability = df.loc[worker_info, TOTAL]
    availability_start = df.loc[worker_info, TOTAL_START]
    expertise = df.loc[worker_info, EXPERTISE]
    locals()[name] = Worker(name, None, role, expertise, availability, availability_start, 0, [])
    all_workers.append(locals()[name])

def create_db_possible_tasks():
    column_names = [NAME, EXPERTISE, TASK, ALLOTTED_TIME,IS_UNIQUE, BUDGET_FOR_UNIQUE_BELLOW, SPRINT,
                    STATUS, IS_ASSIGNED]
    db = pd.DataFrame(columns=column_names)
    return db


def who_can_do_it(task):
    possible_workers = []
    for worker in all_workers:
        if (task.subject in worker.expertise) and (worker.enough_time(task)):
            possible_workers.append(worker)
    return possible_workers

def update_initial_information_db_table(db,name, subject, task, is_unique,i):
   new_info = [name,subject, task.id, task.allotted_time, is_unique,0,0,0,0]
   db.loc[i] = new_info



#### Main
for idx, row in df.iterrows():
    set_worker(idx)

df_tasks_db = create_db_possible_tasks()
print (df_tasks_db)
i = 0
for task in all_tasks:
    subject = task.subject
    possibile_workers = who_can_do_it(task)
    if len(possibile_workers) == ONE:
        update_initial_information_db_table(df_tasks_db, possibile_workers[0].name, subject, task, UNIQUE,i)
        i += 1
    else:
        for pos_worker in possibile_workers:
            update_initial_information_db_table(df_tasks_db, pos_worker.name, subject, task, NOT_UNIQUE,i)
            i += 1


print(df_tasks_db)
df_tasks_db.to_csv(r"C:\Users\Yael Hadad\PycharmProjects\FinalProject\Try_Pandas\s6.csv")



