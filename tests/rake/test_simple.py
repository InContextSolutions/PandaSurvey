import unittest
import numpy
from pandasurvey.rake.simple import SimpleRake
import pandasurvey.datasets as datasets


class TestSimpleRake(unittest.TestCase):

    def setUp(self):
        self.prop = datasets.load_sample_proportions()
        self.df = datasets.load_sample_study()
        self.wt = datasets.load_sample_weights()

    def test_calc(self):
        r = SimpleRake(self.df, self.prop, maxiter=10)
        r.calc()

        r.df['Weight'] = self.wt

        results = []
        alt = []
        targets = []
        wt_sum = r.df['weight'].sum()
        alt_wt_sum = r.df['Weight'].sum()
        for demo in self.prop:
            for value in self.prop[demo]:
                subset = r.df[r.df[demo] == int(value)]
                results.append(subset['weight'].sum() / wt_sum)
                alt.append(subset['Weight'].sum() / alt_wt_sum)
                targets.append(self.prop[demo][value])

        targets = numpy.array(targets)
        results = numpy.array(results)
        alt = numpy.array(alt)

        mse = ((results - targets) ** 2).mean()
        altmse = ((alt - targets) ** 2).mean()
        self.assertLessEqual(mse, altmse)
