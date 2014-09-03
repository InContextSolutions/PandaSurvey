import unittest
import numpy as np
import pandas as pd
from pandasurvey.rake.simple import SimpleRake
import pandasurvey.datasets as datasets


class Test_Simple(unittest.TestCase):

    def test_simplerake_10iters(self):

        target_weights = datasets.load_target_weights()
        target_weights['StudyCellId'] = target_weights.pop('Cell')
        r = SimpleRake(
            datasets.load_rengine_weights(), target_weights, 'RespondentKey', maxiter=10)
        r.df.dropna(inplace=True)
        r.calc()
        compare_df = pd.merge(r.df, r.weights, on='RespondentKey')

        simple_sample = []
        report_sample = []
        targets = []
        for demo in target_weights:

            for value in target_weights[demo]:

                # for found proportions
                simple_sample.append(
                    compare_df.query(demo + "==" + str(value)).sum()['weight'] / compare_df.sum()['weight'])
                report_sample.append(
                    compare_df.query(demo + "==" + str(value)).sum()['Weight'] / compare_df.sum()['Weight'])
                targets.append(target_weights[demo][value])

        simple_mse = (
            (np.array(simple_sample) - np.array(targets)) ** 2).mean()
        report_mse = (
            (np.array(report_sample) - np.array(targets)) ** 2).mean()
        self.assertLessEqual(simple_mse, report_mse)
