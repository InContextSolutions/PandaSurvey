import numpy
from pandasurvey.base import SurveyWeightBase
from pandasurvey.mixins.recode import RecodeMixin


class SimpleRake(SurveyWeightBase, RecodeMixin):

    def __init__(self, df, proportions, recodes={}, epsilon=.01, maxiter=1000):
        self.df = df
        self.rows, self.cols = self.df.shape
        self.recodes = recodes
        self.proportions = proportions
        self.epsilon = epsilon
        self.maxiter = maxiter

    def calc(self):
        self.df['weight'] = numpy.ones(self.rows)

        def update_weights(row):
            if int(row[var]) in self.proportions[var]:
                return self.proportions[var][int(row[var])] * row['weight'] / (group_sums[int(row[var])] / self.rows)
            return row['weight']

        weight_diff = 99  # magic number...
        weight_diff_old = 9999999  # magic number...
        it = 0
        while weight_diff < weight_diff_old * (1 - self.epsilon) and it < self.maxiter:
            it += 1
            weight_old = self.df['weight'].values.tolist()

            for var in self.proportions:
                group_sums = {group[0]: group[1].sum()['weight'] for group in self.df.groupby(var)}
                self.df['weight'] = self.df.apply(update_weights, axis=1)

            weight_diff_old = weight_diff
            weight_diff = sum(abs(self.df['weight'].values - weight_old))

    def weighting_loss(self):
        return len(self.df.weight) * sum(self.df.weight.values ** 2) / self.df.weight.sum() ** 2 - 1
