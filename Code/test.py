import unittest
import pandas as pd
from validate import Valid
from generate_tasks import GenerateTask
from constants import Constants


class TestValid(unittest.TestCase):

    def test1(self):
        v = Valid(
            pd.read_csv(f"{Constants.root_dir}/{Constants.valid_workers_info}/{Constants.workers_info_not_found}"))
        with self.assertRaises(ValueError):
            v.valid_values()


class TestGenerateTask(unittest.TestCase):

    def test_only_1_task(self):
        v = GenerateTask(pd.read_csv(f"{Constants.root_dir}/{Constants.generate_tasks}/{Constants.tasks_1}"))
        self.assertEqual([*v.all_tasks], ['A1'],
                         Constants.message_diff_tasks)

    def test_only_2_task(self):
        v = GenerateTask(pd.read_csv(f"{Constants.root_dir}/{Constants.generate_tasks}/{Constants.tasks_2}"))
        self.assertEqual([*v.all_tasks], ['A1', 'B1'],
                         Constants.message_diff_tasks)

    def test_only_3_task(self):
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
        v = GenerateTask(pd.read_csv(f"{Constants.root_dir}/{Constants.generate_tasks}/{Constants.tasks_9_same_priority}"))
        self.assertEqual([*v.all_tasks], ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'],
                         Constants.message_diff_tasks)

if __name__ == '__main__':
    unittest.main()
