import os
import pandas
from collections import defaultdict

THIS_DIRECTORY, _ = os.path.split(__file__)


def load_people():
    path = os.path.join(THIS_DIRECTORY, "People.csv")
    return pandas.read_csv(path)

def load_rengine_weights():
    path = os.path.join(THIS_DIRECTORY, "study1614,csv")
    return pandas.read_csv(path)

def load_target_weights():
    path = os.path.join(THIS_DIRECTORY, "target_weights_1614.csv")
    targets = pandas.read_csv(path)
    ret_tar = {}
    pass
