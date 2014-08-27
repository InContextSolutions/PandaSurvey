import numpy
import pandas
from PandasRake.base import RakeBase
from PandasRake.mixins.recode import RecodeMixin


class SimpleRake(RakeBase, RecodeMixin):

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
        temp_df['weight'] = numpy.ones(self.rows)

        weight_diff = 99
        weight_diff_old = 9999999
        it = 0
        while weight_diff < weight_diff_old * (1 - self.epsilon) and it < self.maxiter:
            it += 1
            weight_old = temp_df['weight'].values.tolist()

            for var in self.target_pop:
                h = temp_df.groupby(var)
                temp_df['weight'] = temp_df.apply(
                    lambda row: self.target_pop[var][row[var]] *
                    row['weight'] /
                    (h.get_group(row[var]).sum()['weight'] / self.rows),
                    axis=1
                )

            weight_diff_old = weight_diff
            weight_diff = sum(abs(temp_df['weight'].values - weight_old))

        self.weights = temp_df[[self.key_col, 'weight']]
        return self.weights
