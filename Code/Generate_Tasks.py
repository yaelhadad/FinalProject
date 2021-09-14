import pandas as pd
from task import Task
import math

PRIORITY       = 'Queue'
SUBJECT        = "Subject"
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

#df = pd.read_csv("result.csv")

class Gen_Task:

    def __init__(self, tasks_file):
        self.tasks_file = tasks_file
        self.sort_queue_initial = self.tasks_file.sort_values(by=[PRIORITY])
        self.sort_queue = self.sort_queue_initial.reset_index()
        self.LEN_ALL_TASKS = self.sort_queue.shape[FIRST]
        self.ALL_TASKS_RANGE_A = int(math.floor(self.LEN_ALL_TASKS/3))
        self.ALL_TASKS_RANGE_B = self.ALL_TASKS_RANGE_A * 2
        self.all_tasks =[]


    def set_task(self,priority, row, location_in_queue):
        id = priority + str(location_in_queue)
        subject = self.sort_queue.loc[row, SUBJECT]
        description = self.sort_queue.loc[row,DESCRIPTION],
        allotted_time = self.sort_queue.loc[row,ESTIMATED_TIME]
        assignee = self.sort_queue.loc[row,ASSIGNEE]
        status = self.sort_queue.loc[row,STATUS]
        general_location = row
        if status == TETSING or status == REVIEW:
            sprint = PREV
        else:
            sprint = CURRENT
        locals()[id] = Task(id,subject, description,allotted_time,assignee, priority,status,general_location,location_in_queue,sprint)
        self.all_tasks.append(locals()[id])


    def run(self):
        for idx, row in self.sort_queue.loc[FIRST:self.ALL_TASKS_RANGE_A].iterrows():
            self.set_task('A', idx, idx)


        count_B =0
        for idx, row in self.sort_queue.loc[self.ALL_TASKS_RANGE_A:self.ALL_TASKS_RANGE_B].iterrows():
            self.set_task('B', idx, count_B)
            count_B += 1


        count_C =0
        for idx, row in self.sort_queue.loc[self.ALL_TASKS_RANGE_B:self.LEN_ALL_TASKS].iterrows():
            self.set_task('C', idx, count_C)
            count_C += 1


        ### Testing
        for task in self.all_tasks:
            print(task.id)
            print (task.subject)


