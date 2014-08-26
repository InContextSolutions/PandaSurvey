import numpy
import pandas


class Rake:

    def __init__(self, df, recodes, target_pop, epsilon=.01, maxiter=1000):
        self.df = df
        self.rows, self.cols = self.df.shape
        self.recodes = recodes
        self.target_pop = target_pop
        self.epsilon = epsilon
        self.maxiter = maxiter

    def rake(self):
        self.weights = pandas.DataFrame(self.df)
        self.weights['weight'] = numpy.ones(self.rows)
        self.count_totals = {i: self.df[i].value_counts() for i in self.df}

        weight_diff = 99
        weight_diff_old = 9999999
        it = 0
        while weight_diff < weight_diff_old * (1 - self.epsilon) and it < self.maxiter:
            it += 1

            for var in self.target_pop:
                for resp in self.weights:
                    self.weights = self.weights * sum(self.weights['weight'])

        return self.weights

    def rake_on_var(self, df, weights):
        pass

    def recode(self):

        for rec in self.recodes:
            self.df[rec] = self.df.apply(
                lambda row: self.recodes[rec](row[rec]), axis=1)
