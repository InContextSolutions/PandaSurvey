import unittest
import numpy
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


class TestSimpleRake(unittest.TestCase):

    def setUp(self):
        self.prop = datasets.load_sample_proportions()
        self.df = datasets.load_sample_study()
        self.wt = datasets.load_sample_weights()

    def test_calc(self):
        r = SimpleRake(self.df, self.prop, maxiter=10)
        df_out = r.calc()

        df_out['Weight'] = self.wt

        results = []
        alt = []
        targets = []
        wt_sum = df_out['weight'].sum()
        alt_wt_sum = df_out['Weight'].sum()
        for demo in self.prop:
            for value in self.prop[demo]:
                subset = df_out[r.df[demo] == int(value)]
                results.append(subset['weight'].sum() / wt_sum)
                alt.append(subset['Weight'].sum() / alt_wt_sum)
                targets.append(self.prop[demo][value])

        targets = numpy.array(targets)
        results = numpy.array(results)
        alt = numpy.array(alt)

        mse = ((results - targets) ** 2).mean()
        altmse = ((alt - targets) ** 2).mean()
        self.assertLessEqual(mse, altmse)
