import pandas as pd
import numpy as np


class PandasRake:

    def __init__(self, df, recodes, target_pop , convcrit=.01):

        self.df = df
        self.recodes = recodes
        self.target_pop = target_pop

    def raker(self):

        weights = numpy.ones(len(df))
        weight_diff = 99
        weight_diff_old = 9999999
        while weight_diff < weight_diff_old * (1 - convcrit):

            for var in target_pop:
                weights = rake_on_var( df, weights,)

    def rake_on_var(self, df , weights):
        pass

    def recode(self):

        for rec in self.recodes:
            self.df[rec] = self.df.apply( lambda row: self.recodes[rec](row[rec]), axis=1)



if __name__ == '__main__':
    unittest.main()

