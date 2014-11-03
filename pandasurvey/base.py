from abc import ABCMeta, abstractmethod


class SurveyWeightBase:

    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def calc(self):
        pass

    def loss(self, weights):
        n = len(weights)
        return ((weights ** 2).sum() / weights.sum() ** 2) * n - 1
