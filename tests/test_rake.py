import unittest

import pandas as pd

from PandasRake.rake import PandasRake

class TestPandasRake(unittest.TestCase):

    def setUp(self):
        self.recodes = { "Age": lambda age: age + 1 }
        self.target_pops = {}
        self.raker = PandasRake(pd.read_csv('PandasRake/data/People.csv')
                                ,self.recodes ,self.target_pops)

    def test_recode(self):

        self.raker.recode()
        assertEqual(self.raker.df['Age'].values[0]==81)