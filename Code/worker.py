REV_PER_HOUR = 0.5

class Worker:


    def __init__(self, name,password, rev_hours=0, qa_hours =0, new_hours=0, inprog_hours=0):

        self.name = name
        self.password = password
        self.rev_hours = rev_hours
        self.qa_hours = qa_hours
        self.new_hours = new_hours
        self.inprog_hours = inprog_hours


    def update_review_time(self,num_tasks):

        self.rev_hours = num_tasks * REV_PER_HOUR


    def update_qa_time(self,qa_time):

        self.qa_hours = qa_time

    def update_new_time(self,new_time):

        self.new_hours = new_time

    def update_inprog_time(self, inprog_time):
            self.inprog_hours = inprog_time