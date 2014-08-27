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
        fractions = {}
        for cols in self.weights:
            if 'key' not in cols.lower():
                fractions[cols] = {}
                for group in self.weights.groupby(cols):
                    fractions[cols][group[0]] = len(group[1]) * 1. / self.rows

        self.weights['weight'] = numpy.ones(self.rows)
        weight_diff = 99
        weight_diff_old = 9999999
        it = 0
        while weight_diff < weight_diff_old * (1 - self.epsilon) and it < self.maxiter:
            it += 1
            weight_old = self.weights['weight'].values.tolist()

            for var in self.target_pop:
                self.weights['weight'] = self.weights.apply(
                    lambda row: self.target_pop[var][row[var]] * row[
                        'weight'] / fractions[var][row[var]], axis=1
                )

            weight_diff_old = weight_diff
            weight_diff = sum(abs(self.weights['weight'].values - weight_old))

        if it == self.maxiter:
            print 'iterlimit'
        print 'itttt   ', it
        return self.weights[['PrimaryKey', 'weight']]

    def recode(self):

        for rec in self.recodes:
            self.df[rec] = self.df.apply(
                lambda row: self.recodes[rec](row[rec]), axis=1)
