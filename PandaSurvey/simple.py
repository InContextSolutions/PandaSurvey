import numpy
import pandas
from .base import SurveyWeightBase


BIG_M = 100000
EPSILON = 1e-6
MAX_ITER = 1000


class SimpleRake(SurveyWeightBase):

    """Rake weighting implementation.

    :param pandas.DataFrame df: The observations to be weighted.
    :param dict proportions: A dictionary of the target proportions for each demographic and response.
    :param float epsilon: Convergence threshold for the raking procedure.
    :param int maxiter: Maximum number of iterations for the raking procedure.
    """

    def __init__(self, df, proportions, epsilon=EPSILON, maxiter=MAX_ITER):
        self.df = df
        self.rows, self.cols = self.df.shape
        self.proportions = proportions
        self.demos = self.proportions.keys()
        self.epsilon = epsilon
        self.maxiter = maxiter

    def calc(self, use_l2=False):
        """Calculates individual weights.

        :param boolean use_l2: Determines if convergence is measured using the L2 norm of the change in weights. By default, the L1 norm is used.
        """
        warning_state = pandas.options.mode.chained_assignment
        pandas.options.mode.chained_assignment = None

        delta = BIG_M
        delta0 = BIG_M + 1
        num_iters = 0

        new_df = self.df.copy()
        new_df['weight'] = numpy.ones(self.rows)

        def _update(row, mass, var, total_mass):
            value = int(row[var])
            return self.proportions[var][value] * row['weight'] / (mass[value] / total_mass)

        try:
            while delta < delta0 * (1 - self.epsilon) and num_iters < self.maxiter:
                wt = new_df['weight'].copy(deep=True)

                for var in self.proportions:
                    sub_df = new_df[new_df[var].isin([i for i in self.proportions[var] if self.proportions[var][i] > 0.0])].copy(deep=True)
                    mass = {group[0]: group[1].sum()['weight'] for group in sub_df.groupby(var)}
                    total_mass = sub_df.weight.sum()
                    sub_df['weight'] = sub_df.apply(_update, axis=1, mass=mass, var=var, total_mass=total_mass)
                    new_df.update(sub_df)

                delta0 = delta

                if use_l2:
                    delta = ((new_df['weight'] - wt) ** 2).sum()
                else:
                    delta = (new_df['weight'] - wt).abs().sum()
                num_iters += 1
        finally:
            pandas.options.mode.chained_assignment = warning_state

        return new_df
