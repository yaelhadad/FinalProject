REV_PER_HOUR = 0.5

class Worker:

    def __init__(self, name, expertise, impossible_tasks, availaiblity, availaiblity_start_sprint, count_current_work_hours,
              current_tasks, password, optional_tasks, unique_tasks, rev_hours=0, dedicated_hours=0, qa_hours=0, total_prev_hours=0):

        self.name = name
        self.password = password
        self.expertise = expertise
        self.impossible_tasks = impossible_tasks
        self.availaiblity_start_sprint =availaiblity_start_sprint
        self.count_current_work_hours =count_current_work_hours
        self.current_tasks= current_tasks
        self.optional_tasks =optional_tasks
        self.unique_tasks =unique_tasks
        self.availaiblity = availaiblity
        self.dedicated_hours =dedicated_hours
        self.total_prev_hours =total_prev_hours
        self.rev_hours = rev_hours
        self.qa_hours = qa_hours


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

    def update_assigneed_uniqe_task(self,task):
       self.unique_tasks.remove(task.id)

    def update_assigneed_task(self, task):
        if task.priority == 'A':
            self.availaiblity_start_sprint -= task.allotted_time
        self.availaiblity -= task.allotted_time
        self.count_current_work_hours +=task.allotted_time
        self.current_tasks.append(task.id)

    def print_current(self):
        print (self.name)
        print (self.availaiblity)
        print(self.availaiblity_start_sprint)
        print (self.count_current_work_hours)
        print(self.current_tasks)
