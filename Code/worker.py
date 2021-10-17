
class Worker:

    def __init__(self, name, role, password, expertise, availability, availability_start_sprint, count_current_hours,
                 current_tasks):

        self.name = name
        self.role = role
        self.password = password
        self.expertise = expertise
        self.availability = availability
        self.availability_initial = availability
        self.availability_start_sprint = availability_start_sprint
        self.count_current_hours = count_current_hours
        self.current_tasks = current_tasks

    def update_assigned_task(self, task):
        if task.priority == 'A':
            self.availability_start_sprint = str(float(self.availability_start_sprint) - float(task.allotted_time))
        self.availability = str(float(self.availability)- float(task.allotted_time))
        self.count_current_hours = str(float(self.count_current_hours)+ float(task.allotted_time))
        self.current_tasks.append(task.identifier)

    def verify_optional_task_before_devide(self, task, budget):
        optional_availability = float(self.availability) - float(task.allotted_time)
        if optional_availability < 0:
            return False
        if task.priority == 'A':
            optinal_avalialibilty_A = float(self.availability_start_sprint) - float(task.allotted_time)
            if optinal_avalialibilty_A < 0:
                return False
            A_budget = float(budget)
            if A_budget > float(optinal_avalialibilty_A):
                return False
        budget_general = float(budget)
        if budget_general > float(optional_availability):
            return False
        return True

    def enough_time(self, task):
        print (task.allotted_time)
        print (type(task.allotted_time))
        print(self.availability_start_sprint)
        print (type(self.availability_start_sprint))
        a =5
        if task.priority == 'A':
            optional_avalialibilty_A = float(self.availability_start_sprint) - (task.allotted_time)
            if optional_avalialibilty_A <= 0:
                return False
        optional_avalialibilty = float(self.availability) - (task.allotted_time)
        if optional_avalialibilty <= 0:
            return False
        return True

    def print_current(self):
        print("\n")
        print(self.name)
        print("avalibility", self.availability)
        print("initial avalibility", self.availability_initial)
        print("avalibility in the first week", self.availability_start_sprint)
        print("current_hours:", self.count_current_hours)
        budget = str(float(self.count_current_hours)/float(self.availability_initial)*100)
        print("budget is: %s" % (budget) + "%")
        print(self.current_tasks)
