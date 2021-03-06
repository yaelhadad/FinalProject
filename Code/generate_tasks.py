from task import Task
import math
from constants import Constants


def is_blank(cell_value):
    myString = str(cell_value)
    if myString and myString.strip() and myString != "nan":
        # myString is not None AND myString is not empty or blank
        return False
    # myString is None OR myString is empty or blank
    return True


class GenerateTask:

    def __init__(self, tasks_file):
        self.tasks_file = tasks_file
        self.sort_queue = self.tasks_file.sort_values(by=[Constants.PRIORITY]).reset_index()
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
        allotted_time = float(self.sort_queue.loc[row, Constants.ESTIMATED_TIME]) + float(
            self.sort_queue.loc[row, Constants.Review_TIME])
        assignee = self.sort_queue.loc[row, Constants.ASSIGNEE]
        status = self.sort_queue.loc[row, Constants.STATUS]
        general_location = row
        if is_blank(assignee):
            already_assigned = False
        else:
            already_assigned = True

        return Task(name, identify, subject, description, allotted_time, assignee, priority, status,
                    general_location, location_in_queue, already_assigned)

    def set_all_tasks_by_priority(self, start_range, end_range, priority, general_index, priority_index, prev_idx):
        for general_index, row in self.sort_queue.loc[start_range: end_range - prev_idx].iterrows():
            current_task = self.set_task(priority, general_index, priority_index)
            priority_index += 1
            self.all_tasks[current_task.name] = current_task
        return general_index

    def run(self):

        # Handling case that there are only 1/2 tasks.
        if self.LEN_ALL_TASKS < 3:
            last_task_group1 = self.set_all_tasks_by_priority(Constants.FIRST, self.ALL_TASKS_RANGE_A,
                                                              Constants.PRIORITY_A, Constants.FIRST,
                                                              Constants.FIRST_ONE, 0)
            if self.LEN_ALL_TASKS == 1:
                return
            last_task_group2 = self.set_all_tasks_by_priority(1, 2,
                                                              Constants.PRIORITY_B, last_task_group1, 1, 1)

            return

        # Handling case that there are more than 2 tasks.
        # Set the tasks with priority A
        last_task_group1 = self.set_all_tasks_by_priority(Constants.FIRST, self.ALL_TASKS_RANGE_A, Constants.PRIORITY_A,
                                                          Constants.FIRST, Constants.FIRST_ONE, Constants.PREV_INDEX)

        # Set the tasks with priority B
        count = Constants.FIRST_ONE
        last_task_group2 = self.set_all_tasks_by_priority(self.ALL_TASKS_RANGE_A, self.ALL_TASKS_RANGE_B,
                                                          Constants.PRIORITY_B, last_task_group1, count,
                                                          Constants.PREV_INDEX)

        # Set the tasks with priority C
        count = Constants.FIRST_ONE
        last_task_group3 = self.set_all_tasks_by_priority(self.ALL_TASKS_RANGE_B, self.LEN_ALL_TASKS,
                                                          Constants.PRIORITY_C, last_task_group2, count,
                                                          Constants.PREV_INDEX)
