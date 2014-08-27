from abc import ABCMeta, abstractmethod


class RakeBase:

    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def calc_weights(self):
        pass
