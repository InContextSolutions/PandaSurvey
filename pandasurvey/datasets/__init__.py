import os
import pandas

THIS_DIRECTORY, _ = os.path.split(__file__)


def load_people():
    path = os.path.join(THIS_DIRECTORY, "People.csv")
    return pandas.read_csv(path)


def load_sample_study():
    path = os.path.join(THIS_DIRECTORY, "SampleStudy.csv")
    df = pandas.read_csv(path)
    del df['Weight']
    return df


def load_sample_weights():
    path = os.path.join(THIS_DIRECTORY, "SampleStudy.csv")
    df = pandas.read_csv(path)
    return df['Weight']


def load_sample_proportions():
    path = os.path.join(THIS_DIRECTORY, "SampleWeights.csv")
    weights = {}
    with open(path) as csv_in:
        for line in csv_in:
            demo, category, proportion = line.split(',')
            if demo not in weights:
                weights[demo] = {}
            weights[demo][int(category)] = float(proportion)
    return weights
