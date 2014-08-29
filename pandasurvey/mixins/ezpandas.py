import numpy
import pandas


class PandasMixin:

    def read_csv(self, path):
        return pandas.read_csv(path)

    def read_json(self, path):
        return pandas.read_json(path)

    def bootstrap(self, df, key_column='TicketIdent', weight_column='nweight'):
        if weight_column in df.columns.tolist():
            wt = df[[weight_column]].values.ravel()
            wt /= wt.sum()
            idx = numpy.random.choice(
                range(len(df)), size=self.sample_size, replace=True, p=wt)
        else:
            idx = numpy.random.choice(
                range(len(df)), size=self.sample_size, replace=True)

        if key_column is not None:
            keys = [k.upper()
                    for k in df[[key_column]].iloc[idx].values.ravel()]
        else:
            index = df.index.tolist()
            keys = [index[i] for i in idx]
        return keys
