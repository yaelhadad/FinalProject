from constants import Constants


class BudgetUnique:

    def __init__(self, config_file):
        self.config_file = config_file
        self.run()

    def run(self):
        self.config_file = self.config_file.sort_values(by=[Constants.NAME, Constants.TASK], ascending=False)
        all_workers = (self.config_file[Constants.NAME].unique())
        for worker in all_workers:
            possible_tasks_for_worker = self.config_file.loc[self.config_file[Constants.NAME] == worker]
            count_budget = 0
            for idx, row in possible_tasks_for_worker.iterrows():
                # In case that the task is unique you should sum it
                if row.loc[Constants.IS_UNIQUE]:
                    count_budget = count_budget + float(row.loc[Constants.ALLOTTED_TIME])
                else:
                    # In case that the task is not unique you should write the summery for the less important tasks
                    self.config_file.at[idx, Constants.BUDGET_UNIQUE] = str(count_budget)
        # self.config_file.to_csv(
        #     r"C:\Users\Yael Hadad\Desktop\She codes\project_demo\appendix\Artzy family - appendix\results\budget.csv",
        #     index=False)