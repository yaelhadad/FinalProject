from worker import Worker
from task import Task
from conflict import Conflict


#def __init__(self,id,subject, description,allotted_time,assignee, priority,status,general_location,location_in_queue ,sprint):
#def __init__(self, name, expertise, impossible_tasks, availaiblity, availaiblity_start_sprint, count_current_work_hours,
 #            current_tasks, password, optional_tasks, unique_tasks, rev_hours=0, dedicated_hours=0, qa_hours=0, total_prev_hours=0):



def update_workers(all_workers,worker,task):
    all_possible_workers =all_workers.copy()
    all_possible_workers.remove(worker)
    for pos_worker in all_possible_workers:
        if task.id in pos_worker.optional_tasks:
            pos_worker.optional_tasks.remove(task.id)

found = False
worker_yael = Worker("Yael Hadad", ['ATEGen', 'SVFSTIL', 'STILEDITOR','WAVER', 'GENERAL'],['C2'], 60, 14, 0, [],'12345',
                     ['A1','A2','A3','B1','B2','B3','C1'],['A2','A3','C1'],0,0,0,0,)
worker_elad = Worker("Elad Motzny", ['CONVMGR', 'ATEGEN', 'STILEDITOR', 'VCDSTIL'],['A2','A3','C1'], 50, 8, 0,[], '12344',
                    ['A1','B1','B2','B3','C2'],['C2'],0,0,0,0)

task1 = Task('A1','ATEGen','BLA BLA', 6, None, 'A', 'New', 1,1,'current')
task2 = Task('A2','GENERAL','BLA BLA', 6, None, 'A', 'New',2,2,'current')
task3 = Task('A3','GENERAL','BLA BLA', 2, None, 'A', 'New',3,3,'current')
task4 = Task('B1','ATEGen','BLA BLA', 6, None, 'B', 'New',4,1,'current')
task5 = Task('B2','STILEDITOR','BLA BLA', 6, None, 'B', 'New',5,2,'current')
task6 = Task('B3','GENERAL','BLA BLA', 2, None, 'B', 'New',6,3,'current')
task7 = Task('C1','WAVER','BLA BLA', 6, None, 'C', 'New',7,1,'current')
task8 = Task('C2','VCDSTIL','BLA BLA', 2, None, 'B', 'New',8,2,'current')

all_tasks = [task1, task2, task3, task4, task5, task6, task7, task8]
all_workers = [worker_yael, worker_elad]

for task in all_tasks:
    # Check if the task is uniqe:
    for worker in all_workers:
        if task.id in  worker.unique_tasks:
            task.set_task('assigneed', worker.name)
            worker.update_assigneed_uniqe_task(task)
            worker.update_assigneed_task(task)
            update_workers(all_workers, worker, task)
            found = True
            break
    if found:
        continue
    # Decide what to do if more than 1 people can do the task:
    # Allocate the relvant workers
    all_optinal_workers_len_uniqe = {}
    all_optinal_workers_exeprt = {}
    for worker in all_workers:
        if task.id in worker.optional_tasks:
            all_optinal_workers_len_uniqe[worker] = len(worker.unique_tasks)
            all_optinal_workers_exeprt[worker] = worker.optional_tasks.index(task.id)
    #Decidenios
    min_num_uniqe = min(all_optinal_workers_len_uniqe.values())
    workers_with_less_uniqe = [k for k, v in all_optinal_workers_len_uniqe.items() if v == min_num_uniqe]
    if (len(workers_with_less_uniqe) == 1):
        task.set_task('assigneed', workers_with_less_uniqe[0].name)
        workers_with_less_uniqe[0].update_assigneed_task(task)
        update_workers(all_workers, workers_with_less_uniqe[0], task)

    else:
        pass
        ## In case of task with priority A prefer to asssinee it to the one with more avaliblity in first week
        ## prefer to asssinee it to the one with more avaliblity
        ## max in  all_optinal_workers_exeprt, if more than one - avialable
    task.print_task()

for worker in all_workers:
    worker.print_current()


