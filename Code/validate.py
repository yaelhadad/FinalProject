import sys
import numpy as np
from constants import Constants

sys.tracebacklimit = 0


class Valid:
    EMPTY_ERROR_MESSAGE = "Input table is empty"
    def __init__(self, df):
        self.df = df

    def is_empty(self):
        if self.df.empty:
            raise ValueError(self.EMPTY_ERROR_MESSAGE)


class ValidWorkersFile(Valid):
    def valid_values(self):
        self.is_empty()
        # validate inputs
        if not self.df[Constants.NAME].isin(Constants.ALL_WORKERS_IN_TEAM).all():
            raise ValueError("Worker is not defined in the team")
        if self.df[Constants.TOTAL].dtype not in (np.int64, np.float64):
            raise ValueError("Total hours are invalid")
        if self.df[Constants.TOTAL_START].dtype not in (np.int64, np.float64):
            raise ValueError("Total hours at the first week are invalid")
        # except AssertionError:
        #     print("nnn")

        # if float(row.loc[TOTAL_HOURS]) < float(row.loc[TOTAL_HOURS_START]):


class ValidTasksFile(Valid):
    def valid_values(self):
        self.is_empty()


class ValidPosTasks(ValidTasksFile):
    EMPTY_ERROR_MESSAGE = "All the tasks are impossible for the workers"


