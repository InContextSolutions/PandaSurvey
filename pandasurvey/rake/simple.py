import math
import numpy
import pandas
import matplotlib.pyplot as pl
from pandasurvey.base import SurveyWeightBase
from pandasurvey.mixins.recode import RecodeMixin
from pandasurvey.mixins.ezpandas import PandasMixin


class SimpleRake(SurveyWeightBase, RecodeMixin, PandasMixin):

    def __init__(self, df, recodes, target_pop, key_col, epsilon=.01, maxiter=1000):
        self.df = df
        self.rows, self.cols = self.df.shape
        self.recodes = recodes
        self.target_pop = target_pop
        self.epsilon = epsilon
        self.maxiter = maxiter
        self.key_col = key_col

    def calc(self):
        temp_df = pandas.DataFrame(self.df)
        self.rows = len(temp_df)
        temp_df['weight'] = numpy.ones(self.rows)

        weight_diff = 99
        weight_diff_old = 9999999
        it = 0
        while weight_diff < weight_diff_old * (1 - self.epsilon) and it < self.maxiter:
            it += 1
            weight_old = temp_df['weight'].values.tolist()
            for i in weight_old:
                if math.isnan(i):
                    return weight_old

            for var in self.target_pop:
                h = temp_df.groupby(var)
                print temp_df[['StudyTicketId', 'weight']]
                print var

                def my_func(row):
                    if int(row[var]) in self.target_pop[var]:
                        return self.target_pop[var][int(row[var])] * row['weight'] / (h.get_group(int(row[var])).sum()['weight'] / self.rows)
                    return row['weight']
                temp_df['weight'] = temp_df.apply(my_func, axis=1)

            weight_diff_old = weight_diff
            weight_diff = sum(abs(temp_df['weight'].values - weight_old))
            print "iterations   : ", it
            print weight_diff, weight_diff_old * (1 - self.epsilon)
        self.weights = temp_df[[self.key_col, 'weight']]
        return self.weights
    """
    def compare_things(self, iterations):
        # move to tests and most likely broken, had moved to compare.py
        own = []
        report = []
        for i in range:
            keys = self.bootstrap(self.df, weight_column='weight')
            own_temp = numpy.mean(
                [self.df.at[k, 'Gender'] * self.df.at[k, 'weight'] for k in keys])
            own.append(own_temp)

            keys = self.bootstrap(self.df, weight_column='Weight')
            report_temp = numpy.mean(
                [self.df.at[k, 'Gender'] * self.df.at[k, 'Weight'] for k in keys])
            report.append(report_temp)

        o = pl.figure(1)
        o.hist(own)

        r = pl.figure(2)
        r.hist(report)

        pl.show()

        pass
    """
    def weighting_loss(self):
        return len(self.weights) * sum(self.weights['weight'].values ** 2) / self.weights.sum()['weight'] ** -1
