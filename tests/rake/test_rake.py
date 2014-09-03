import unittest
from pandasurvey.rake.simple import SimpleRake
import pandasurvey.datasets as datasets


class TestRake(unittest.TestCase):

    def setUp(self):
        self.recodes = {
            "Age": lambda age: int(age / 10),
            "MaritalStatus": lambda m: int(m / 2)}
        self.target_proportions = {
            "Gender": {
                1: .4916,
                2: .5084}}
        self.df = datasets.load_people()

    def test_smoke(self):
        r = SimpleRake(self.df, self.target_proportions, recodes=self.recodes)
        self.assertIsNotNone(r)

    def test_recode(self):
        r = SimpleRake(self.df, self.target_proportions, recodes=self.recodes)
        r.recode()
        self.assertEqual(r.df['Age'].values[0], 8)
        self.assertEqual(r.df['MaritalStatus'].values[2], 2)
