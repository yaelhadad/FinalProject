from worker import Worker
from task import Task

ASSIGNED = 'assigned'
FIRST = 0
NA = "N/A"
MANAGER = "Yael Hadad"
IMPOSSIBLE = "IMPOSSIBLE"

def update_workers(worker,task):
    all_possible_workers =all_workers.copy()
    all_possible_workers.remove(worker)
    for pos_worker in all_possible_workers:
        if task.id in pos_worker.optional_tasks:
            pos_worker.optional_tasks.remove(task.id)

def divide_task(worker,task):
    task.set_task(ASSIGNED, worker.name)
    worker.update_assigned_task(task)
    update_workers(worker, task)

def impossible_task(task):
    task.status = NA
    task.assignee = MANAGER

########## TEST1 - 3 WORKERS
A1 = Task('A1','ATEGen','BLA BLA', 6, None, 'A', 'New', 1,1,'current')
A2 = Task('A2','GENERAL','BLA BLA', 6, None, 'A', 'New',2,2,'current')
A3 = Task('A3','GENERAL','BLA BLA', 2, None, 'A', 'New',3,3,'current')
B1 = Task('B1','ATEGen','BLA BLA', 6, None, 'B', 'New',4,1,'current')
B2 = Task('B2','STILEDITOR','BLA BLA', 6, None, 'B', 'New',5,2,'current')
B3 = Task('B3','ATEGen','BLA BLA', 2, None, 'B', 'New',6,3,'current')
C1 = Task('C1','WAVER','BLA BLA', 6, None, 'C', 'New',7,1,'current')
C2 = Task('C2','VCDSTIL','BLA BLA', 10, None, 'B', 'New',8,2,'current')
worker_yael = Worker("Yael Hadad", ['ATEGen', 'SVFSTIL', 'STILEDITOR','WAVER', 'GENERAL'], 50, 14, 0, [],'12345',
                     [A1,A2,A3,B1,B2,B3,C1],[A2,A3,C1],0,0,0,0,)
worker_elad = Worker("Elad Motzny", ['CONVMGR', 'ATEGEN', 'STILEDITOR', 'VCDSTIL'], 50, 8, 0,[], '12344',
                    [A1,B1,B2,B3,C2],[C2],0,0,0,0)
worker_mayan = Worker("MAYYAN", ['CONVMGR', 'ATEGEN', 'STILEDITOR', 'VCDSTIL'], 50, 8, 0,[], '12344',
                    [B2],[],0,0,0,0)
all_tasks = [A1, A2, A3, B1, B2, B3,C1,C2]
all_workers = [worker_yael, worker_elad,worker_mayan]

########## TEST2 - 2 COMMON OPTINAL TASKS A1, B2 - THREAT CONFLICTS
A1 = Task('A1','ATEGen','BLA BLA', 4, None, 'A', 'New', 1,1,'current')
A2 = Task('A2','GENERAL','BLA BLA',1, None, 'A', 'New',2,2,'current')
A3 = Task('A3','GENERAL','BLA BLA',1, None, 'A', 'New',3,3,'current')
B1 = Task('B1','ATEGen','BLA BLA', 1, None, 'B', 'New',4,1,'current')
B2 = Task('B2','STILEDITOR','BLA BLA',3, None, 'B', 'New',5,2,'current')
B3 = Task('B3','ATEGen','BLA BLA',8, None, 'B', 'New',6,3,'current')


worker_yael = Worker("Yael Hadad", ['ATEGen', 'SVFSTIL', 'STILEDITOR','WAVER', 'GENERAL'] ,6, 3, 0, [],'12345',
                     [A1,A2,A3,B1,B2],[A2,A3,B1],0,0,0,0,)
worker_elad = Worker("Elad Motzny", ['CONVMGR', 'ATEGEN', 'STILEDITOR', 'VCDSTIL'], 12, 11, 0,[], '12344',
                    [A1,B2,B3],[B3],0,0,0,0)

all_tasks = [A1, A2, A3, B1, B2, B3]
all_workers = [worker_yael, worker_elad]



########## TEST3 - IMPOSSIIBLE TASKS
A1 = Task('A1','ATEGen','BLA BLA', 4, None, 'A', 'New', 1,1,'current')
A2 = Task('A2','GENERAL','BLA BLA',6, None, 'A', 'New',2,2,'current')
A3 = Task('A3','GENERAL','BLA BLA',1, None, 'A', 'New',3,3,'current')
B1 = Task('B1','ATEGen','BLA BLA', 1, None, 'B', 'New',4,1,'current')
B2 = Task('B2','STILEDITOR','BLA BLA',7, None, 'B', 'New',5,2,'current')
B3 = Task('B3','ATEGen','BLA BLA',8, None, 'B', 'New',6,3,'current')


worker_yael = Worker("Yael Hadad", ['ATEGen', 'SVFSTIL', 'STILEDITOR','WAVER', 'GENERAL'], 6, 3, 0, [],'12345',
                     [A1,A2,A3,B1,B2],[A2,A3,B1],0,0,0,0,)
worker_elad = Worker("Elad Motzny", ['CONVMGR', 'ATEGEN', 'STILEDITOR', 'VCDSTIL'], 5, 4, 0,[], '12344',
                    [A1,B2],[],0,0,0,0)

all_tasks = [A1, A2, A3, B1, B2, B3]
all_workers = [worker_yael, worker_elad]


for worker in all_workers:
    worker.print_current()

for task in all_tasks:
    # Check if the task is unique:
    found = False
    for worker in all_workers:
        if task in worker.unique_tasks:
            if worker.verify_unique_task_before_devide(task):
                divide_task(worker, task)
                worker.update_assigned_unique_task(task)
            else:
                impossible_task(task)
            found = True
            break
    if found:
        continue
    ###### Decide what to do if a task appear in the optional list of multiple workers: #####

    # Allocate the relevant workers
    # Extract the total hours of their unique tasks
    # Verify that if they will get the task, it will not effect their unique tasks
    all_optional_workers_unique_tasks_budget = {}
    for worker in all_workers:
        if task in worker.optional_tasks:
            if worker.verify_optional_task_before_devide(task):
                all_optional_workers_unique_tasks_budget[worker] = worker.calculate_unique_tasks_budget()
            else:
                worker.update_assigned_optional_task(task)


    #Decidenios
    #In case that only one worker has the minumum budget for uniuqe tasks
    if bool(all_optional_workers_unique_tasks_budget):
        min_num_unique = min(all_optional_workers_unique_tasks_budget.values())
    else:
        impossible_task(task)
        continue
    workers_with_less_unique = [k for k, v in all_optional_workers_unique_tasks_budget.items() if v == min_num_unique]
    if (len(workers_with_less_unique) == 1):
        divide_task(workers_with_less_unique[FIRST], task)

    else:
        ## In case of task with priority A prefer to asssinee it to the one with more avaliblity in first week
        all_optional_workers_sprint = {}
        possible_workers = [*all_optional_workers_unique_tasks_budget]
        for pos_worker in possible_workers:
            if task.priority == 'A':
                all_optional_workers_sprint[pos_worker] = pos_worker.availaiblity_start_sprint
            else:
                all_optional_workers_sprint[pos_worker] = pos_worker.availaiblity_sprint
        max_available = max(all_optional_workers_sprint.values())
        workers_with_max_availability = [k for k, v in all_optional_workers_sprint.items() if v == max_available]
        divide_task(workers_with_max_availability[FIRST], task)


for worker in all_workers:
    worker.print_current()

for task in all_tasks:
    if task.status == NA:
        print (IMPOSSIBLE, task.id)
