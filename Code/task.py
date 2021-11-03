class Task:

    def __init__(self, name, identifier, subject, description, allotted_time, assignee, priority, status,
                 general_location, location_in_queue, already_assigned):
        self.name = name
        self.identifier = identifier
        self.subject = subject
        self.description = description
        self.allotted_time = allotted_time
        self.assignee = assignee
        self.priority = priority
        self.general_location = general_location
        self.location_in_queue = location_in_queue
        self.status = status
        self.already_assigned = already_assigned

    def set_task(self, status, assignee):
        self.status = status
        self.assignee = assignee
