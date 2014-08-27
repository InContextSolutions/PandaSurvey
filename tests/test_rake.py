import unittest
from PandasRake.simplerake import SimpleRake
from PandasRake.datasets import load_people


class TestPandasRake(unittest.TestCase):

    def setUp(self):
        self.recodes = {"Age": lambda age: age / 10,
                        "MaritalStatus": lambda m: m / 2}
        self.target_pops = {

            "Gender": {1: .4916, 2: .5084}
        }
        self.df = load_people()

    def test_smoke(self):
        r = SimpleRake(self.df, self.recodes, self.target_pops)
        self.assertIsNotNone(r)

    def test_recode(self):
        r = SimpleRake(self.df, self.recodes, self.target_pops)
        r.recode()
        self.assertEqual(r.df['Age'].values[0], 8)
        self.assertEqual(r.df['MaritalStatus'].values[2], 2)

    def test_rake(self):
        #
        # will build better test cases here
        #
        r = SimpleRake(self.df, self.recodes, self.target_pops, maxiter=10)
        r.recode()
        wt = r.calc()
        self.assertEqual(len(r.weights), len(wt))
