import math
from functools import partial
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
        temp_df = self.df.copy()
        self.rows = len(temp_df)
        temp_df['weight'] = numpy.ones(self.rows)

        weight_diff = 99
        weight_diff_old = 9999999
        it = 0
        self.weight_hist = []
        while weight_diff < weight_diff_old * (1 - self.epsilon) and it < self.maxiter:
            it += 1
            weight_old = temp_df['weight'].values.tolist()

            for var in self.target_pop:
                h = temp_df.groupby(var)
                group_sums = {group[0]: group[1].sum()['weight'] for group in temp_df.groupby(var)}

                def my_func(row):
                    if int(row[var]) in self.target_pop[var]:
                        return self.target_pop[var][int(row[var])] * row['weight'] / (group_sums[int(row[var])] / self.rows)
                    return row['weight']
                temp_df['weight'] = temp_df.apply(my_func, axis=1)

            weight_diff_old = weight_diff
            weight_diff = sum(abs(temp_df['weight'].values - weight_old))
            self.weight_hist.append(weight_diff)
            print "iterations   : ", it
            print weight_diff, weight_diff_old * (1 - self.epsilon)
        self.weights = temp_df[[self.key_col, 'weight']]
        return self.weights

    def weighting_loss(self):
        return len(self.weights) * sum(self.weights['weight'].values ** 2) / self.weights.sum()['weight'] ** -1
