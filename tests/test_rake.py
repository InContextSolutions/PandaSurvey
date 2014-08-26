import unittest

import pandas as pd

from PandasRake.rake import PandasRake

class TestPandasRake(unittest.TestCase):

    def setUp(self):
        self.recodes = { "Age": lambda age: age + 1 , 
                         "MaritalStatus": lambda m : m /2}
        self.target_pops = {}
        self.raker = PandasRake(pd.read_csv('PandasRake/data/People.csv')
                                ,self.recodes ,self.target_pops)

    def test_recode(self):

        self.raker.recode()
        self.assertEqual(self.raker.df['Age'].values[0],81)
        self.assertEqual(self.raker.df['MaritalStatus'].values[2],2)