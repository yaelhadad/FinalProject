from task import Task
import math
from constants import Constants


class GenerateTask:

    def __init__(self, tasks_file):
        self.tasks_file = tasks_file
        self.sort_queue_initial = self.tasks_file.sort_values(by=[Constants.PRIORITY])
        self.sort_queue = self.sort_queue_initial.reset_index()
        self.LEN_ALL_TASKS = self.sort_queue.shape[Constants.FIRST]
        self.ALL_TASKS_RANGE_A = int(math.floor(self.LEN_ALL_TASKS / 3))
        self.ALL_TASKS_RANGE_B = self.ALL_TASKS_RANGE_A * 2
        self.all_tasks = {}
        self.run()

    def set_task(self, priority, row, location_in_queue):
        name = priority + str(location_in_queue)
        identify = self.sort_queue.loc[row, Constants.ID]
        subject = self.sort_queue.loc[row, Constants.SUBJECT]
        description = self.sort_queue.loc[row, Constants.DESCRIPTION]
        allotted_time = self.sort_queue.loc[row, Constants.ESTIMATED_TIME] + self.sort_queue.loc[row, Constants.Review_TIME]
        assignee = self.sort_queue.loc[row, Constants.ASSIGNEE]
        status = self.sort_queue.loc[row, Constants.STATUS]
        general_location = row
        if status == Constants.PROGRESSIVE or status == Constants.REVIEW:
            sprint = Constants.PREV
        else:
            sprint = Constants.CURRENT
        return Task(name, identify, subject, description, allotted_time, assignee, priority, status,
                    general_location, location_in_queue, sprint)
        # locals()[name] = Task(name, identify, subject, description, allotted_time, assignee, priority, status,
        #                       general_location,location_in_queue,sprint)
        # self.all_tasks.append(locals()[name])

    def set_all_tasks_by_priority(self, start_range, end_range, priority, general_index, priority_index):
        for general_index, row in self.sort_queue.loc[start_range: end_range - Constants.PREV_INDEX].iterrows():
            current_task = self.set_task(priority, general_index, priority_index)
            priority_index += 1
            print(current_task)
            self.all_tasks[current_task.name] = current_task

        # for general_index, row in self.sort_queue.loc[start_range: end_range - Constants.PREV_INDEX].iterrows():
        #     self.set_task(priority, general_index, priority_index)
        #     priority_index += 1
        return general_index

    def run(self):

        # Set the tasks with priority A
        last_task_group1 = self.set_all_tasks_by_priority(Constants.FIRST, self.ALL_TASKS_RANGE_A, Constants.PRIORITY_A,
                                                          Constants.FIRST, Constants.FIRST)
        # Set the tasks with priority B
        count = Constants.FIRST
        last_task_group2 = self.set_all_tasks_by_priority(self.ALL_TASKS_RANGE_A, self.ALL_TASKS_RANGE_B,Constants.PRIORITY_B,
                                                          last_task_group1, count)
        # Set the tasks with priority B
        count = Constants.FIRST
        last_task_group3 = self.set_all_tasks_by_priority(self.ALL_TASKS_RANGE_B, self.LEN_ALL_TASKS,Constants.PRIORITY_C,
                                                          last_task_group2, count)

        print ("tasks" ,self.all_tasks)
        ### Testing
        # for task in self.all_tasks:
        #     print(task.identifier)
        #     print (task.name)
        #     print(task.subject)
