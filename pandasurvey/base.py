from abc import ABCMeta, abstractmethod


class SurveyWeightBase:

    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def calc(self):
        pass
