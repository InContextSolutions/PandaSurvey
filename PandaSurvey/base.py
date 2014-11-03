from abc import ABCMeta, abstractmethod


class SurveyWeightBase:

    """Abstract base class for survey weighting method."""

    __metaclass__ = ABCMeta

    def __init__(self, df, proportions, recodes={}):
        pass

    @abstractmethod
    def calc(self):
        """Calculation step must be implemented here."""
        pass

    def loss(self, weights):
        """Describes the inflation in the variance of sample estimates that can be attributed to weighting. See *Applied Survey Data Analysis* (2010) by Heeringa et al. for more information.

        :param numpy.array weights: array of individual weights
        """
        n = len(weights)
        return ((weights ** 2).sum() / weights.sum() ** 2) * n - 1

    def recode(self, encoders):
        """Recodes demographic information.

        :param dict encoders: Mapping of demographic keys to respective recoding function. Need only define those demographic dimensions that need to be recoded.
        """
        for demo in encoders:
            func = lambda row: encoders[demo](row[demo])
            self.df[demo] = self.df.apply(func, axis=1)
