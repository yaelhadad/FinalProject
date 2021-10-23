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
        allotted_time = float(self.sort_queue.loc[row, Constants.ESTIMATED_TIME]) + float(self.sort_queue.loc[row, Constants.Review_TIME])
        assignee = self.sort_queue.loc[row, Constants.ASSIGNEE]
        status = self.sort_queue.loc[row, Constants.STATUS]
        general_location = row
        if assignee:
            already_assigned = True
        else:
            already_assigned = False
        return Task(name, identify, subject, description, allotted_time, assignee, priority, status,
                    general_location, location_in_queue, already_assigned)
        # locals()[name] = Task(name, identify, subject, description, allotted_time, assignee, priority, status,
        #                       general_location,location_in_queue,sprint)
        # self.all_tasks.append(locals()[name])

    def set_all_tasks_by_priority(self, start_range, end_range, priority, general_index, priority_index, prev_idx):
        for general_index, row in self.sort_queue.loc[start_range: end_range - prev_idx].iterrows():
            current_task = self.set_task(priority, general_index, priority_index)
            priority_index += 1
            # print("the task", current_task)
            self.all_tasks[current_task.name] = current_task
        return general_index

    def run(self):
        print (self.LEN_ALL_TASKS)
        if self.LEN_ALL_TASKS < 3 :
            last_task_group1 = self.set_all_tasks_by_priority(Constants.FIRST, self.ALL_TASKS_RANGE_A,
                                                              Constants.PRIORITY_A, Constants.FIRST, Constants.FIRST_ONE, 0)
            if self.LEN_ALL_TASKS == 1:
                return
            last_task_group2 = self.set_all_tasks_by_priority(1, 2,
                                                              Constants.PRIORITY_B, last_task_group1, 1,1)

            return


        # Set the tasks with priority A
        last_task_group1 = self.set_all_tasks_by_priority(Constants.FIRST, self.ALL_TASKS_RANGE_A, Constants.PRIORITY_A,
                                                          Constants.FIRST, Constants.FIRST_ONE,Constants.PREV_INDEX)
        print (last_task_group1)
        # print("self.ALL_TASKS_RANGE_A", self.ALL_TASKS_RANGE_A)
        # print ("aaa",self.all_tasks)
        # Set the tasks with priority B
        count = Constants.FIRST_ONE
        last_task_group2 = self.set_all_tasks_by_priority(self.ALL_TASKS_RANGE_A, self.ALL_TASKS_RANGE_B,
                                                          Constants.PRIORITY_B, last_task_group1, count, Constants.PREV_INDEX)

        # Set the tasks with priority B
        count = Constants.FIRST_ONE
        last_task_group3 = self.set_all_tasks_by_priority(self.ALL_TASKS_RANGE_B, self.LEN_ALL_TASKS,
                                                              Constants.PRIORITY_C, last_task_group2, count, Constants.PREV_INDEX)


        print("tasks", self.all_tasks)
        ### Testing
        # for task in self.all_tasks:
        #     print(task.identifier)
        #     print (task.name)
        #     print(task.subject)
