import os
import pandas

THIS_DIRECTORY, _ = os.path.split(__file__)


def load_people():
    path = os.path.join(THIS_DIRECTORY, "People.csv")
    return pandas.read_csv(path)
