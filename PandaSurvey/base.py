from abc import ABCMeta, abstractmethod


class SurveyWeightBase:

    """Abstract base class for survey weighting method."""

    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def calc(self):
        """Calculation step must be implemented here."""
        pass

    def loss(self, weights):
        """Describes the inflation in the variance of sample estimates that can be attributed to weighting. See *Applied Survey Data Analysis* (2010) by Heeringa et al. for more information."""
        n = len(weights)
        return ((weights ** 2).sum() / weights.sum() ** 2) * n - 1
