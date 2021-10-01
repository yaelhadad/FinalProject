import unittest
from validate import Valid
from generate_tasks import GenerateTask
import pandas as pd
import Defs


class TestValid(unittest.TestCase):

    def test1(self):
        v = Valid(pd.read_csv(f"{Defs.root_dir}/{Defs.valid_workers_info}/{Defs.workers_info_not_found}"))
        with self.assertRaises(ValueError):
            v.valid_values()

class TestGenerateTask(unittest.TestCase):
    def test1(self):
        v = GenerateTask(pd.read_csv(f"{Defs.root_dir}/{Defs.generate_tasks}/{Defs.tasks_8}"))
if __name__ == '__main__':
    unittest.main()
