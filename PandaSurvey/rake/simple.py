import numpy
import pandas
from PandaSurvey.base import SurveyWeightBase
from PandaSurvey.mixins.recode import RecodeMixin


BIG_M = 99
EPSILON = 1e-3
MAX_ITER = 1000


class SimpleRake(SurveyWeightBase, RecodeMixin):

    def __init__(self, df, target_proportions, recodes={}, epsilon=EPSILON, maxiter=MAX_ITER):
        self.df = df
        self.rows, self.cols = self.df.shape
        self.recodes = recodes
        self.target_proportions = target_proportions
        self.demos = self.target_proportions.keys()
        self.epsilon = epsilon
        self.maxiter = maxiter

    def calc(self, L2=False):
        warning_state = pandas.options.mode.chained_assignment
        pandas.options.mode.chained_assignment = None

        delta = BIG_M
        delta0 = BIG_M + 1
        num_iters = 0

        new_df = self.df.copy()
        new_df['weight'] = numpy.ones(self.rows)

        def _update(row):
            value = int(row[var])
            return self.target_proportions[var][value] * row['weight'] / (mass[value] / self.rows)

        try:
            while delta < delta0 * (1 - self.epsilon) and num_iters < self.maxiter:
                wt = new_df['weight']

                for var in self.target_proportions:
                    mass = {group[0]: group[1].sum()['weight'] for group in new_df.groupby(var)}
                    sub_df = new_df[new_df[var].isin(self.target_proportions[var])]
                    sub_df['weight'] = sub_df.apply(_update, axis=1)
                    new_df.update(sub_df)

                delta0 = delta

                if L2:
                    delta = ((new_df['weight'] - wt) ** 2).sum()
                else:
                    delta = (new_df['weight'] - wt).abs().sum()

                num_iters += 1
        finally:
            pandas.options.mode.chained_assignment = warning_state

        new_df[self.demos] = new_df[self.demos].astype(int)
        return new_df
