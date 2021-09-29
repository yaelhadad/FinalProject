import sys
import numpy as np
import Defs

sys.tracebacklimit = 0


class Valid:
    def __init__(self, config_file, tasks_file):

        self.config_file = config_file
        self.tasks_file = tasks_file

    def valid_values(self):
        # validate inputs
        if not self.config_file[Defs.NAME].isin(Defs.ALL_WORKERS_IN_TEAM).all():
            raise ValueError("Worker is not defined in the team")
        if self.config_file[Defs.TOTAL].dtype not in (np.int64, np.float64):
            raise ValueError("Total hours are invalid")
        if self.config_file[Defs.TOTAL_START].dtype not in (np.int64, np.float64):
            raise ValueError("Total hours at the first week are invalid")
        # except AssertionError:
        #     print("nnn")

        # if float(row.loc[TOTAL_HOURS]) < float(row.loc[TOTAL_HOURS_START]):


