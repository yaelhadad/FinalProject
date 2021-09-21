NAME = 'Name'


class TaskAssigned:

    def __init__(self, config_file, all_workers):
        self.config_file = config_file
        self.workers = all_workers

    def generate_tasks(self):
        dfs = dict(tuple(self.config_file.groupby(NAME)))
        for worker in self.workers:
            df = dfs[worker.name]
            df.to_csv(r"C:\Users\Yael Hadad\Desktop\She codes\Final project\Tests\results\%s.csv"
                      % worker.name)
        for worker in self.workers:
            worker.print_current()