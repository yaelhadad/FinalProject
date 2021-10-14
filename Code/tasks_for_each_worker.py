from constants import Constants


class TaskAssigned:

    def __init__(self, config_file, all_workers):
        self.config_file = config_file
        self.workers = all_workers

    def generate_tasks(self):
        dfs = dict(tuple(self.config_file.groupby(Constants.NAME)))
        for worker in self.workers.values():
            print(worker.name)
            try:
                df = dfs[worker.name]
                df.to_csv(r"C:\Users\User\PycharmProjects\FinalProject\Code\\results\%s.csv"
                          % worker.name)
            except:
                print(f'{worker.name} did not get tasks')

        for worker in self.workers.values():
            worker.print_current()
