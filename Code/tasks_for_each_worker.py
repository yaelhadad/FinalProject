from constants import Constants
import sqlalchemy
from login import db, Assigned


class TaskAssigned:

    def __init__(self, config_file, all_workers):
        self.config_file = config_file
        self.workers = all_workers
        self.results_of_assign = {}

    def generate_tasks(self):
        print(type(self.config_file))
        # db.session.query(Assigned).delete()
        # db.session.commit()
        #sql_Delete_query = """DROP TABLE assigned"""
        dfs = dict(tuple(self.config_file.groupby(Constants.NAME)))
        engine = sqlalchemy.create_engine('sqlite:///Users_Info.db')
        self.config_file.to_sql('assigned122687', engine)
        print(dfs)
        #self.results_of_assign = dfs
        for worker in self.workers.values():
            print(worker.name)
            try:
                df = dfs[worker.name]
                df.to_csv(r"C:\Users\Yael Hadad\PycharmProjects\FinalProject\Code\results\%s.csv"
                          % worker.name)
            except:
                print(f'{worker.name} did not get tasks')

        for worker in self.workers.values():
            worker.print_current()
