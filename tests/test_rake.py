import unittest

import pandas as pd

from PandasRake.rake import PandasRake

class TestPandasRake(unittest.TestCase):

    def setUp(self):


        #recode age to 10 step size
        self.recodes = { "Age": lambda age: age /10, 
                         "MaritalStatus": lambda m : m /2}

        self.target_pops = {
                            0: .5, 1 : .2 

                            }
        self.raker = PandasRake(pd.read_csv('PandasRake/data/People.csv')
                                ,self.recodes ,self.target_pops)

    def test_recode(self):

        self.raker.recode()
        self.assertEqual(self.raker.df['Age'].values[0],8)
        self.assertEqual(self.raker.df['MaritalStatus'].values[2],2)


    def test_rake(self):

        self.assertEqual(len(self.raker.weights), len(self.raker.rake()))