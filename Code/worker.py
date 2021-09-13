REV_PER_HOUR = 0.5
from functools import reduce
class Worker:

    def __init__(self, name, role,password, expertise, availability, availability_start_sprint, count_current_hours,
              current_tasks ):

        self.name = name
        self.role = role
        self.password = password
        self.expertise = expertise
        self.availability = availability
        self.availability_start_sprint = availability_start_sprint
        self.count_current_hours = count_current_hours
        self.current_tasks = current_tasks




    # def __init__(self, name, expertise, availaiblity, availaiblity_start_sprint, count_current_work_hours,
    #           current_tasks, password, optional_tasks, unique_tasks, rev_hours=0, dedicated_hours=0, qa_hours=0, total_prev_hours=0):
    #
    #     self.name = name
    #     self.password = password
    #     self.expertise = expertise
    #     self.availaiblity_start_sprint =availaiblity_start_sprint
    #     self.count_current_work_hours =count_current_work_hours
    #     self.current_tasks= current_tasks
    #     self.optional_tasks =optional_tasks
    #     self.unique_tasks =unique_tasks
    #     self.availaiblity = availaiblity
    #     self.dedicated_hours =dedicated_hours
    #     self.total_prev_hours =total_prev_hours
    #     self.rev_hours = rev_hours
    #     self.qa_hours = qa_hours


    # def __init__(self, name,password, rev_hours=0, qa_hours =0, new_hours=0, inprog_hours=0):
    #
    #     self.name = name
    #     self.password = password
    #     self.rev_hours = rev_hours
    #     self.qa_hours = qa_hours
    #     self.new_hours = new_hours
    #     self.inprog_hours = inprog_hours


    def update_review_time(self,num_tasks):
        self.rev_hours = num_tasks * REV_PER_HOUR

    def update_qa_time(self,qa_time):
        self.qa_hours = qa_time

    def update_assigned_unique_task(self,task):
       self.unique_tasks.remove(task)

    def update_assigned_optional_task(self,task):
       self.optional_tasks.remove(task)

    def update_assigned_task(self, task):
        if task.priority == 'A':
            self.availaiblity_start_sprint -= task.allotted_time
        self.availaiblity -= task.allotted_time
        self.count_current_work_hours +=task.allotted_time
        self.current_tasks.append(task.id)

    def calculate_unique_tasks_budget(self):
        return sum(i.allotted_time for i in self.unique_tasks)

    def verify_unique_task_before_devide(self, task):
        availability = self.availaiblity - task.allotted_time
        if task.priority == 'A':
            avalialibilty_A = self.availaiblity_start_sprint - task.allotted_time
            if avalialibilty_A < 0:
                return False
        if availability < 0:
            return False
        return True


    def verify_optional_task_before_devide(self, task):
        optional_availability = self.availaiblity - task.allotted_time
        A_budget = 0
        if task.priority == 'A':
            optinal_avalialibilty_A = self.availaiblity_start_sprint - task.allotted_time
            A_budget = self.caluculate_conflict_A()
            if A_budget > optinal_avalialibilty_A:
                return False
        budget = self.caluculate_conflict()
        if budget > optional_availability:
            return False
        return True

    def caluculate_conflict_A(self):
        count_A_tasks = 0
        for un_task in self.unique_tasks:
            if un_task.priority == 'A':
                count_A_tasks +=un_task.allotted_time
        return count_A_tasks

    def caluculate_conflict(self):
        count_tasks = 0
        for un_task in self.unique_tasks:
           count_tasks +=un_task.allotted_time
        return count_tasks

    def enough_time(self, task):
        if task.priority == 'A':
            optinal_avalialibilty_A = self.availability_start_sprint - task.allotted_time
            if optinal_avalialibilty_A <= 0:
                return False
        optinal_avalialibilty = self.availability - task.allotted_time
        if optinal_avalialibilty <= 0:
            return False
        return True

    def print_current(self):
        print (self.name)
        print ("avalibilty",self.availaiblity)
        print("start",self.availaiblity_start_sprint)
        print ("current_hours",self.count_current_work_hours)
        print(self.current_tasks)
        print (self.calculate_unique_tasks_budget())
