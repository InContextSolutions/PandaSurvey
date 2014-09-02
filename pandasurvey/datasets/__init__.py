import os
import pandas

THIS_DIRECTORY, _ = os.path.split(__file__)


def load_people():
    path = os.path.join(THIS_DIRECTORY, "People.csv")
    return pandas.read_csv(path)


def load_rengine_weights():
    path = os.path.join(THIS_DIRECTORY, "study_1614.csv")
    return pandas.read_csv(path)


def load_target_weights():
    path = os.path.join(THIS_DIRECTORY, "target_weights_1614.csv")
    targets = pandas.read_csv(path)
    ret = {}
    for i in targets.iterrows():
        if i[1]['RespondentGroup'] not in ret:
            ret[i[1]['RespondentGroup']] = {}
        ret[i[1]['RespondentGroup']][i[1]['Value']] = i[1]['Target']
    for i in ret['Cell']:
        ret['Cell'][i] = 1. / len(ret['Cell'])
    return ret


def load_teniters():
    path = os.path.join(THIS_DIRECTORY, "teniter_cellweights.csv")
    return pandas.read_csv(path)


def load_thirtyiters():
    path = os.path.join(THIS_DIRECTORY, "thirtyiter_weights.csv")
    return pandas.read_csv(path)
