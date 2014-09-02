import sys
import math
from functools import partial
import numpy
import pandas
from pandasurvey.base import SurveyWeightBase
from pandasurvey.mixins.recode import RecodeMixin
from pandasurvey.mixins.ezpandas import PandasMixin


class SimpleRake(SurveyWeightBase, RecodeMixin, PandasMixin):

    """ Class for simple Raking procedure
    Parameters
    ----------
    df : Pandas.DataFrame
        A dataframe with the appropriate demographics
    target_pop : dict
        Dictionary with demographics as keys pointed at dictionary 
        with demographic values pointed at the target proportions
        Ex.
        {
        'Gender':
            {
            1: .5,
            2: .5
            }
        }
    key_col: string
        column to be used as key column
    recodes: dict
        Dictionary with demographics as keys pointed at function
        to apply to demographic values
        Ex.
        {
        'Age':
        lambda age: age/20
        }
    epsilon: float
        accuaracy wanted
    maxiter: int
        max iterations desired
    """

    def __init__(self, df, target_pop, key_col, recodes=None, epsilon=.01, maxiter=1000):

        self.df = df
        self.rows, self.cols = self.df.shape
        if recodes is None:
            self.recodes = {}
        else:
            self.recodes = recodes
        self.target_pop = target_pop
        self.target_pop = target_pop
        self.epsilon = epsilon
        self.maxiter = maxiter
        self.key_col = key_col

    def calc(self):
        temp_df = self.df.copy().dropna()
        self.rows = len(temp_df)
        temp_df['weight'] = numpy.ones(self.rows)

        def my_func(row):
            if int(row[var]) in self.target_pop[var]:
                return self.target_pop[var][int(row[var])] * row['weight'] / (group_sums[int(row[var])] / self.rows)
            return row['weight']

        weight_diff = 99
        weight_diff_old = 9999999
        it = 0
        self.weight_its_hist = []
        while weight_diff < weight_diff_old * (1 - self.epsilon) and it < self.maxiter:
            it += 1
            weight_old = temp_df['weight'].values.tolist()

            for var in self.target_pop:
                group_sums = {group[0]: group[1].sum()['weight'] for group in temp_df.groupby(var)}

                temp_df['weight'] = temp_df.apply(my_func, axis=1)

            weight_diff_old = weight_diff
            weight_diff = sum(abs(temp_df['weight'].values - weight_old))
            self.weight_its_hist.append(weight_diff)
            print temp_df['weight']

        self.weights = temp_df[[self.key_col, 'weight']]
        return self.weights

    def weighting_loss(self):
        return len(self.weights) * sum(self.weights['weight'].values ** 2) / self.weights.sum()['weight'] ** 2 - 1
