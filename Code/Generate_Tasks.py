from task import Task
import math

PRIORITY = 'Queue'
SUBJECT = "Subject"
DESCRIPTION = 'Description'
ESTIMATED_TIME = 'Allotted time'
Review_TIME = "Review Time"
ASSIGNEE = 'Assignee'
STATUS = 'Status'
PREV = 'Previous'
CURRENT = 'Current'
PROGRESSIVE = 'Progressive'
REVIEW = 'Review'
FIRST = 0
ID = "ID"
PRIORITY_A = 'A'
PRIORITY_B = 'B'
PRIORITY_C = 'C'
PREV_INDEX = 1
all_tasks = []


class GenerateTask:

    def __init__(self, tasks_file):
        self.tasks_file = tasks_file
        self.sort_queue_initial = self.tasks_file.sort_values(by=[PRIORITY])
        self.sort_queue = self.sort_queue_initial.reset_index()
        self.LEN_ALL_TASKS = self.sort_queue.shape[FIRST]
        self.ALL_TASKS_RANGE_A = int(math.floor(self.LEN_ALL_TASKS / 3))
        self.ALL_TASKS_RANGE_B = self.ALL_TASKS_RANGE_A * 2
        self.all_tasks = []
        self.run()

    def set_task(self, priority, row, location_in_queue):
        name = priority + str(location_in_queue)
        identify = self.sort_queue.loc[row, ID]
        subject = self.sort_queue.loc[row, SUBJECT]
        description = self.sort_queue.loc[row, DESCRIPTION]
        allotted_time = self.sort_queue.loc[row, ESTIMATED_TIME] + self.sort_queue.loc[row, Review_TIME]
        assignee = self.sort_queue.loc[row, ASSIGNEE]
        status = self.sort_queue.loc[row, STATUS]
        general_location = row
        if status == PROGRESSIVE or status == REVIEW:
            sprint = PREV
        else:
            sprint = CURRENT
        locals()[name] = Task(name, identify, subject, description, allotted_time, assignee, priority, status,
                              general_location,location_in_queue,sprint)
        self.all_tasks.append(locals()[name])

    def sel_all_tasks_by_priority(self, start_range, end_range, priority, general_index, priority_index):
        for general_index, row in self.sort_queue.loc[start_range: end_range - PREV_INDEX].iterrows():
            self.set_task(priority, general_index, priority_index)
            priority_index += 1
        return general_index

    def run(self):

        # Set the tasks with priority A
        last_task_group1 = self.sel_all_tasks_by_priority(FIRST, self.ALL_TASKS_RANGE_A, PRIORITY_A,
                                                          FIRST, FIRST)
        # Set the tasks with priority B
        count = FIRST
        last_task_group2 = self.sel_all_tasks_by_priority(self.ALL_TASKS_RANGE_A, self.ALL_TASKS_RANGE_B,PRIORITY_B,
                                                          last_task_group1, count)
        # Set the tasks with priority B
        count = FIRST
        last_task_group3 = self.sel_all_tasks_by_priority(self.ALL_TASKS_RANGE_B, self.LEN_ALL_TASKS,PRIORITY_C,
                                                          last_task_group2, count)

        ### Testing
        # for task in self.all_tasks:
        #     print(task.identifier)
        #     print (task.name)
        #     print(task.subject)
