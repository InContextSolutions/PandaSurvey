import unittest
import numpy
import PandaSurvey as ps
from PandaSurvey.simple import SimpleRake


class TestRake(unittest.TestCase):

    def setUp(self):
        self.recodes = {
            "Age": lambda age: int(age / 10),
            "MaritalStatus": lambda m: int(m / 2)
        }

        self.target_proportions = {
            "Gender": {
                1: .4916,
                2: .5084
            }
        }

        self.df = ps.load_people()

    def test_smoke(self):
        r = SimpleRake(self.df, self.target_proportions)
        self.assertIsNotNone(r)

    def test_recode(self):
        r = SimpleRake(self.df, self.target_proportions)
        r.recode(self.recodes)
        self.assertEqual(r.df['Age'].values[0], 8)
        self.assertEqual(r.df['MaritalStatus'].values[2], 2)


class TestSimpleRake(unittest.TestCase):

    def setUp(self):
        self.prop = ps.load_sample_proportions()
        self.df = ps.load_sample_study()
        self.wt = ps.load_sample_weights()
        self.rake = SimpleRake(self.df, self.prop)

    def calc_mse(self, df):
        results = []
        alt = []
        targets = []
        wt_sum = df['weight'].sum()
        alt_wt_sum = df['target_weight'].sum()
        for demo in self.prop:
            for value in self.prop[demo]:
                subset = df[self.df[demo] == int(value)]
                results.append(subset['weight'].sum() / wt_sum)
                alt.append(subset['target_weight'].sum() / alt_wt_sum)
                targets.append(self.prop[demo][value])

        targets = numpy.array(targets)
        results = numpy.array(results)
        alt = numpy.array(alt)

        mse = ((results - targets) ** 2).mean()
        altmse = ((alt - targets) ** 2).mean()
        return mse, altmse

    def test_calc_l1(self):
        df_out = self.rake.calc()
        df_out['target_weight'] = self.wt
        mse, altmse = self.calc_mse(df_out)
        self.assertLessEqual(mse, altmse)
        self.assertLessEqual(self.rake.loss(df_out.weight), 1e-3)

    def test_calc_l2(self):
        df_out = self.rake.calc(use_l2=True)
        df_out['target_weight'] = self.wt
        mse, altmse = self.calc_mse(df_out)
        self.assertLessEqual(mse, altmse)
        self.assertLessEqual(self.rake.loss(df_out.weight), 1e-3)
