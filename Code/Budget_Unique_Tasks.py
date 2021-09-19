NAME = 'Name'
TASK = 'Task'
IS_UNIQUE = "Is the task Unique?"
ALLOTTED_TIME = "Allotted time"
BUDGET_UNIQUE = 'Total time for less important unique tasks'


class BudgetUnique:

    def __init__(self, config_file):
        self.config_file = config_file

    def run(self):
        self.config_file = self.config_file.sort_values(by=[NAME, TASK], ascending=False)
        all_workers = (self.config_file[NAME].unique())
        for worker in all_workers:
            df = self.config_file.loc[self.config_file[NAME] == worker]
            count_budget = 0
            for idx, row in df.iterrows():
                if row.loc[IS_UNIQUE]:
                    count_budget = count_budget + float(row.loc[ALLOTTED_TIME])
                else:
                    self.config_file.at[idx, BUDGET_UNIQUE] = str(count_budget)
        self.config_file.to_csv(
             r"C:\Users\Yael Hadad\PycharmProjects\FinalProject\code_for_project\Tests\Test4\temp_db_table_gold.csv")
        return self.config_file
