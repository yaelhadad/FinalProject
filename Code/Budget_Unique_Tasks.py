import Defs


class BudgetUnique:

    def __init__(self, config_file):
        self.config_file = config_file

    def run(self):
        self.config_file = self.config_file.sort_values(by=[Defs.NAME, Defs.TASK], ascending=False)
        all_workers = (self.config_file[Defs.NAME].unique())
        for worker in all_workers:
            df = self.config_file.loc[self.config_file[Defs.NAME] == worker]
            count_budget = 0
            for idx, row in df.iterrows():
                if row.loc[Defs.IS_UNIQUE]:
                    count_budget = count_budget + float(row.loc[Defs.ALLOTTED_TIME])
                else:
                    self.config_file.at[idx, Defs.BUDGET_UNIQUE] = str(count_budget)
        self.config_file.to_csv(
             r"C:\Users\Yael Hadad\PycharmProjects\FinalProject\Try_Pandas\sprint_23_9\BUDGET_BUGS.csv")
        return self.config_file
