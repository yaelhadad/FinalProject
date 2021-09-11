import pandas as pd
from task import Task
import math
df = pd.read_csv("result.csv")

PRIORITY       = 'Queue'
SUBJECT        = "Tags"
DESCRIPTION    = 'Subject'
ESTIMATED_TIME = 'QA time'
ASSIGNEE       = 'Tester'
STATUS         = 'Status'

PREV          = 'Previous'
CURRENT       = 'Current'
TETSING       = 'Testing'
REVIEW        = 'Review'
FIRST         = 0
all_tasks = []

sort_queue2 = df.sort_values(by=[PRIORITY])
sort_queue2.to_csv(r"C:\Users\Yael Hadad\PycharmProjects\FinalProject\Try_Pandas\s1.csv")
sort_queue = pd.read_csv("s1.csv")
LEN_ALL_TASKS = sort_queue.shape[FIRST]
ALL_TASKS_RANGE_A = int(math.floor(LEN_ALL_TASKS/3))-1
ALL_TASKS_RANGE_B = ALL_TASKS_RANGE_A *2

#    def __init__(self,id,subject, description,allotted_time,assignee, priority,status,general_location,location_in_queue,sprint ):

def set_task(priority,row,location_in_queue):
    id = priority + str(location_in_queue)
    subject = sort_queue.loc[row, SUBJECT]
    description = sort_queue.loc[row,DESCRIPTION],
    allotted_time = sort_queue.loc[row,ESTIMATED_TIME]
    assignee= sort_queue.loc[row,ASSIGNEE]
    status = sort_queue.loc[row,STATUS]
    general_location = row
    if status == TETSING or REVIEW:
        sprint = PREV
    else:
        sprint = CURRENT
    locals()[id] = Task(id,subject, description,allotted_time,assignee, priority,status,general_location,location_in_queue,sprint)
    all_tasks.append(locals()[id])


for idx, row in sort_queue.loc[FIRST:ALL_TASKS_RANGE_A].iterrows():
    set_task('A', idx, idx)


count_B =0
for idx, row in sort_queue.loc[ALL_TASKS_RANGE_A:ALL_TASKS_RANGE_B].iterrows():
    set_task('B', idx, count_B)
    count_B += 1


count_C =0
for idx, row in sort_queue.loc[ALL_TASKS_RANGE_B:LEN_ALL_TASKS].iterrows():
    set_task('C', idx, count_C)
    count_C += 1


for task in all_tasks:
    print (task.subject)

