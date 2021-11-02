import unittest
import pandas as pd
import numpy as np
from validate import ValidWorkersFile, ValidTasksFile
from generate_tasks import GenerateTask
from constants import Constants
from processing_workers_info import WorkerInfo
from pandas.testing import assert_frame_equal


class TestValidWorkersFile(unittest.TestCase):

    def test_1_task_workers_can_not_do_it_time(self):
        tasks = GenerateTask(
            pd.read_csv(f"{Constants.root_dir}/{Constants.generate_tasks}/{Constants.task_1_impossible_hours}"))
        impossible_tasks = WorkerInfo(pd.read_csv(f"{Constants.root_dir}/{Constants.worker_info}/{Constants.work_table_all}"),
                               tasks.all_tasks)
        df = pd.read_csv(f"{Constants.root_dir}/{Constants.worker_info_gold}/{Constants.impossible_task }")
        assert_frame_equal(df, impossible_tasks.all_impossible_tasks)



class TestGenerateTask(unittest.TestCase):

    def test_only_1_task(self):
        v = GenerateTask(pd.read_csv(f"{Constants.root_dir}/{Constants.generate_tasks}/{Constants.tasks_1}"))
        self.assertEqual([*v.all_tasks], ['A1'],
                         Constants.message_diff_tasks)

    def test_only_2_tasks(self):
        v = GenerateTask(pd.read_csv(f"{Constants.root_dir}/{Constants.generate_tasks}/{Constants.tasks_2}"))
        self.assertEqual([*v.all_tasks], ['A1', 'B1'],
                         Constants.message_diff_tasks)

    def test_3_tasks(self):
        v = GenerateTask(pd.read_csv(f"{Constants.root_dir}/{Constants.generate_tasks}/{Constants.tasks_3}"))
        self.assertEqual([*v.all_tasks], ['A1', 'B1', 'C1'],
                         Constants.message_diff_tasks)

    def test_7_tasks_not_divided_for_3_priority(self):
        v = GenerateTask(pd.read_csv(f"{Constants.root_dir}/{Constants.generate_tasks}/{Constants.tasks_7}"))
        self.assertEqual([*v.all_tasks], ['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'C3'],
                         Constants.message_diff_tasks)

    def test_8_tasks_not_divided_for_3_priority(self):
        v = GenerateTask(pd.read_csv(f"{Constants.root_dir}/{Constants.generate_tasks}/{Constants.tasks_8}"))
        self.assertEqual([*v.all_tasks], ['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'C3', 'C4'],
                         Constants.message_diff_tasks)

    def test_9_tasks_divide_for_3_priority(self):
        v = GenerateTask(pd.read_csv(f"{Constants.root_dir}/{Constants.generate_tasks}/{Constants.tasks_9}"))
        self.assertEqual([*v.all_tasks], ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'],
                         Constants.message_diff_tasks)

    def test_9_tasks_same_priority(self):
        v = GenerateTask(
            pd.read_csv(f"{Constants.root_dir}/{Constants.generate_tasks}/{Constants.tasks_9_same_priority}"))
        self.assertEqual([*v.all_tasks], ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'],
                         Constants.message_diff_tasks)


class TestWorkerInfo(unittest.TestCase):
    def test_heartbeat(self):
        tasks = GenerateTask(
            pd.read_csv(f"{Constants.root_dir}/{Constants.generate_tasks}/{Constants.tasks_9_same_priority}"))
        pos_tasks = WorkerInfo(pd.read_csv(f"{Constants.root_dir}/{Constants.worker_info}/{Constants.work_table}"),
                               tasks.all_tasks)
        df = pd.read_csv(f"{Constants.root_dir}/{Constants.worker_info_gold}/{Constants.proc_tasks9}")
        assert_frame_equal(df, pos_tasks.df_tasks_db)

    def test_1_task_some_workers_can_do_it(self):
        tasks = GenerateTask(
            pd.read_csv(f"{Constants.root_dir}/{Constants.generate_tasks}/{Constants.tasks_1}"))
        pos_tasks = WorkerInfo(pd.read_csv(f"{Constants.root_dir}/{Constants.worker_info}/{Constants.work_table}"),
                               tasks.all_tasks)
        df = pd.read_csv(f"{Constants.root_dir}/{Constants.worker_info_gold}/{Constants.proc_tasks1}")
        assert_frame_equal(df, pos_tasks.df_tasks_db)

    def test_1_task_all_workers_can_do_it(self):
        tasks = GenerateTask(
            pd.read_csv(f"{Constants.root_dir}/{Constants.generate_tasks}/{Constants.tasks_1}"))
        pos_tasks = WorkerInfo(pd.read_csv(f"{Constants.root_dir}/{Constants.worker_info}/{Constants.work_table_all}"),
                               tasks.all_tasks)
        df = pd.read_csv(f"{Constants.root_dir}/{Constants.worker_info_gold}/{Constants.proc_tasks1_all}")
        assert_frame_equal(df, pos_tasks.df_tasks_db)

    def test_1_task_workers_can_not_do_it_time(self):
        tasks = GenerateTask(
            pd.read_csv(f"{Constants.root_dir}/{Constants.generate_tasks}/{Constants.task_1_impossible_hours}"))
        impossible_tasks = WorkerInfo(pd.read_csv(f"{Constants.root_dir}/{Constants.worker_info}/{Constants.work_table_all}"),
                               tasks.all_tasks)
        df = pd.read_csv(f"{Constants.root_dir}/{Constants.worker_info_gold}/{Constants.impossible_task }")
        assert_frame_equal(df, impossible_tasks.all_impossible_tasks)

    # def test_1_task_workers_can_not_do_it_expertise(self):
    #     tasks = GenerateTask(
    #         pd.read_csv(f"{Constants.root_dir}/{Constants.generate_tasks}/{Constants.task_1_impossible_expertise}"))
    #     with self.assertRaises(ValueError):
    #         pos_tasks = WorkerInfo(
    #             pd.read_csv(f"{Constants.root_dir}/{Constants.worker_info}/{Constants.work_table_all}"),
    #             tasks.all_tasks)

# class TestAssigned(unittest.TestCase):
#     def test_heartbeat_already_assigned(self):



if __name__ == '__main__':
    unittest.main()
