from worker import Worker
from task import Task

ASSIGNED = 'assigned'
FIRST = 0

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

A1 = Task('A1','ATEGen','BLA BLA', 6, None, 'A', 'New', 1,1,'current')
A2 = Task('A2','GENERAL','BLA BLA', 6, None, 'A', 'New',2,2,'current')
A3 = Task('A3','GENERAL','BLA BLA', 2, None, 'A', 'New',3,3,'current')
B1 = Task('B1','ATEGen','BLA BLA', 6, None, 'B', 'New',4,1,'current')
B2 = Task('B2','STILEDITOR','BLA BLA', 6, None, 'B', 'New',5,2,'current')
B3 = Task('B3','ATEGen','BLA BLA', 2, None, 'B', 'New',6,3,'current')
C1 = Task('C1','WAVER','BLA BLA', 6, None, 'C', 'New',7,1,'current')
C2 = Task('C2','VCDSTIL','BLA BLA', 10, None, 'B', 'New',8,2,'current')


worker_yael = Worker("Yael Hadad", ['ATEGen', 'SVFSTIL', 'STILEDITOR','WAVER', 'GENERAL'],['C2'], 50, 14, 0, [],'12345',
                     [A1,A2,A3,B1,B2,B3,C1],[A2,A3,C1],0,0,0,0,)
worker_elad = Worker("Elad Motzny", ['CONVMGR', 'ATEGEN', 'STILEDITOR', 'VCDSTIL'],['A2','A3','C1'], 50, 8, 0,[], '12344',
                    [A1,B1,B2,B3,C2],[C2],0,0,0,0)
worker_mayan = Worker("MAYYAN", ['CONVMGR', 'ATEGEN', 'STILEDITOR', 'VCDSTIL'],['A2','A3','C1'], 50, 8, 0,[], '12344',
                    [B2],[],0,0,0,0)
all_tasks = [A1, A2, A3, B1, B2, B3,C1,C2]
all_workers = [worker_yael, worker_elad,worker_mayan]

for worker in all_workers:
    worker.print_current()

for task in all_tasks:
    # Check if the task is unique:
    found = False
    for worker in all_workers:
        if task in worker.unique_tasks:
            divide_task(worker, task)
            worker.update_assigned_unique_task(task)
            found = True
            break
    if found:
        continue
    ###### Decide what to do if more than 1 people can do the task: #####
    # Allocate the relevant workers and extract the total hours of their unique tasks
    all_optional_workers_unique_tasks_budget = {}
    for worker in all_workers:
        if task in worker.optional_tasks:
            all_optional_workers_unique_tasks_budget[worker] = worker.calculate_unique_tasks_budget()

    #Decidenios
    min_num_unique = min(all_optional_workers_unique_tasks_budget.values())
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
        workers_with_max_availabilty = [k for k, v in all_optional_workers_sprint.items() if v == max_available]
        divide_task(workers_with_max_availabilty[FIRST], task)


for worker in all_workers:
    worker.print_current()


