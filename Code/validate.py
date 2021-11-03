import sys
import numpy as np
import pandas as pd
from constants import Constants

sys.tracebacklimit = 0


class Valid:
    EMPTY_ERROR_MESSAGE = "Input table is empty"

    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)


    def is_empty(self):
        print(self.df)
        if self.df.empty:
            raise ValueError(self.EMPTY_ERROR_MESSAGE)


class ValidWorkersFile(Valid):
    def valid_values(self):
        self.is_empty()
        # validate inputs
        if not self.df[Constants.NAME].isin(Constants.ALL_WORKERS_IN_TEAM).all():
            raise ValueError("Worker is not defined in the team")
        if self.df[Constants.TOTAL].str.isdigit().all():
            raise ValueError("Total hours are invalid")
        if self.df[Constants.TOTAL_START].str.isdigit().all():
            raise ValueError("Total hours are invalid")

        # if float(row.loc[TOTAL_HOURS]) < float(row.loc[TOTAL_HOURS_START]):


class ValidTasksFile(Valid):
    def valid_values(self):
        self.is_empty()


class ValidPosTasks(ValidTasksFile):
    EMPTY_ERROR_MESSAGE = "All the tasks are impossible for the workers"
