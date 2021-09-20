REV_PER_HOUR = 0.5


class Worker:

    def __init__(self, name, role, password, expertise, availability, availability_start_sprint, count_current_hours,
                 current_tasks):

        self.name = name
        self.role = role
        self.password = password
        self.expertise = expertise
        self.availability = availability
        self.availability_start_sprint = availability_start_sprint
        self.count_current_hours = count_current_hours
        self.current_tasks = current_tasks


    def update_assigned_task(self, task):
        if task.priority == 'A':
            self.availability_start_sprint -= task.allotted_time
        self.availability -= task.allotted_time
        self.count_current_hours += task.allotted_time
        self.current_tasks.append(task.identifier)


    def verify_unique_task_before_devide(self, task):
        availability = self.availability - task.allotted_time
        if task.priority == 'A':
            avalialibilty_A = self.availability_start_sprint - task.allotted_time
            if avalialibilty_A < 0:
                return False
        if availability < 0:
            return False
        return True

    def verify_optional_task_before_devide(self, task):
        optional_availability = self.availability - task.allotted_time
        A_budget = 0
        if task.priority == 'A':
            optinal_avalialibilty_A = self.availability_start_sprint - task.allotted_time
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
                count_A_tasks += un_task.allotted_time
        return count_A_tasks

    def caluculate_conflict(self):
        count_tasks = 0
        for un_task in self.unique_tasks:
            count_tasks += un_task.allotted_time
        return count_tasks

    def enough_time(self, task):
        if task.priority == 'A':
            optional_avalialibilty_A = self.availability_start_sprint - task.allotted_time
            if optional_avalialibilty_A <= 0:
                return False
        optional_avalialibilty = self.availability - task.allotted_time
        if optional_avalialibilty <= 0:
            return False
        return True

    def print_current(self):
        print(self.name)
        print("availbilty", self.availability)
        print("start", self.availability_start_sprint)
        print("current_hours", self.count_current_hours)
        print(self.current_tasks)

