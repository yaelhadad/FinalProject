from task import Task
import math
import Defs

all_tasks = []


class GenerateTask:

    def __init__(self, tasks_file):
        self.tasks_file = tasks_file
        self.sort_queue_initial = self.tasks_file.sort_values(by=[Defs.PRIORITY])
        self.sort_queue = self.sort_queue_initial.reset_index()
        self.LEN_ALL_TASKS = self.sort_queue.shape[Defs.FIRST]
        self.ALL_TASKS_RANGE_A = int(math.floor(self.LEN_ALL_TASKS / 3))
        self.ALL_TASKS_RANGE_B = self.ALL_TASKS_RANGE_A * 2
        self.all_tasks = []
        self.run()

    def set_task(self, priority, row, location_in_queue):
        name = priority + str(location_in_queue)
        identify = self.sort_queue.loc[row, Defs.ID]
        subject = self.sort_queue.loc[row, Defs.SUBJECT]
        description = self.sort_queue.loc[row, Defs.DESCRIPTION]
        allotted_time = self.sort_queue.loc[row, Defs.ESTIMATED_TIME] + self.sort_queue.loc[row, Defs.Review_TIME]
        assignee = self.sort_queue.loc[row, Defs.ASSIGNEE]
        status = self.sort_queue.loc[row, Defs.STATUS]
        general_location = row
        if status == Defs.PROGRESSIVE or status == Defs.REVIEW:
            sprint = Defs.PREV
        else:
            sprint = Defs.CURRENT
        locals()[name] = Task(name, identify, subject, description, allotted_time, assignee, priority, status,
                              general_location,location_in_queue,sprint)
        self.all_tasks.append(locals()[name])

    def sel_all_tasks_by_priority(self, start_range, end_range, priority, general_index, priority_index):
        for general_index, row in self.sort_queue.loc[start_range: end_range - Defs.PREV_INDEX].iterrows():
            self.set_task(priority, general_index, priority_index)
            priority_index += 1
        return general_index

    def run(self):

        # Set the tasks with priority A
        last_task_group1 = self.sel_all_tasks_by_priority(Defs.FIRST, self.ALL_TASKS_RANGE_A, Defs.PRIORITY_A,
                                                          Defs.FIRST, Defs.FIRST)
        # Set the tasks with priority B
        count = Defs.FIRST
        last_task_group2 = self.sel_all_tasks_by_priority(self.ALL_TASKS_RANGE_A, self.ALL_TASKS_RANGE_B,Defs.PRIORITY_B,
                                                          last_task_group1, count)
        # Set the tasks with priority B
        count = Defs.FIRST
        last_task_group3 = self.sel_all_tasks_by_priority(self.ALL_TASKS_RANGE_B, self.LEN_ALL_TASKS,Defs.PRIORITY_C,
                                                          last_task_group2, count)


        ### Testing
        # for task in self.all_tasks:
        #     print(task.identifier)
        #     print (task.name)
        #     print(task.subject)
