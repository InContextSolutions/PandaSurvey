import pandas as pd
import numpy
import matplotlib.pyplot as pl
from pandasurvey.datasets import *


def bootstrap(sample_size, df, key_column='TicketIdent', weight_column='nweight'):
    if weight_column in df.columns.tolist():
        wt = df[[weight_column]].values.ravel()
        wt /= wt.sum()
        idx = numpy.random.choice(
            range(len(df)), size=sample_size, replace=True, p=wt)
    else:
        idx = numpy.random.choice(
            range(len(df)), size=sample_size, replace=True)

    if key_column is not None:
        keys = [k.upper()
                for k in df[[key_column]].iloc[idx].values.ravel()]
    else:
        index = df.index.tolist()
        keys = [index[i] for i in idx]
    return keys


def merged_datasets_by_path(path_one, path_two, key_column):
    my_res = pd.read_csv(path_one)
    the_res = pd.read_csv(path_two)
    return pd.merge(
        my_res, the_res, left_on=key_column, right_on=key_column)


def bootrapped_weight_propoortions(df, key_column, weight_column, proportion_column, target_value):

    keys = bootstrap(
        len(df), df, weight_column='weight', key_column="RespondentKey")
    own_temp = [df[df.RespondentKey == k][
        [weight_column, proportion_column]].values for k in keys]
    temp =[]
    for i in own_temp:
        if i[0][1] == target_value:
            temp.append(i[0][0])
    return sum(temp) / sum(map(lambda i: i[0][0], own_temp)) 

def bootstrapped_proportions(df, key_column, proportion_column, target_value ):

    keys = bootstrap(
        len(df), df, weight_column='NA', key_column="RespondentKey")
    own_temp = [df[df.RespondentKey == k][
        [ proportion_column]].values for k in keys]
    return own_temp.count(target_value)*1./len(df) 

def compare_weight_proportions():
    pass

def main():
    #modulize and stuff

    tots = merged_datasets_by_path('pandasurvey/datasets/www.csv',
                                   'pandasurvey/datasets/study_1614.csv',
                                    "RespondentKey")
    own = []
    report = []
    original_sample = []
    demographic = 'Gender'
    target_demographic_value = 2
    for i in range(200):

        own.append(bootrapped_weight_propoortions(tots, 'RespondentKey', 'weight', demographic, target_demographic_value))

        report.append(bootrapped_weight_propoortions(tots, 'RespondentKey', 'Weight', demographic, target_demographic_value))

        original_sample.append(bootstrapped_proportions(tots, 'RespondentKey', demographic, target_demographic_value))


    targets = load_target_weights()
    target_proportion = targets[demographic][target_demographic_value]
    f, (ax1, ax2, ax3) = pl.subplots(3, sharex=True, sharey=True)
    f.suptitle('Gender proportions bootstrapped: Target proportion : ' + str(target_proportion) )
    ax1.hist(own,color ='crimson')
    ax1.set_title('pandasurvey mean: ' + str(numpy.mean(own))+" | median : " + str(numpy.median(own)) + " | std : " + str(numpy.std(own)) )
    ax2.hist(report, color = 'burlywood')
    ax2.set_title('Report Engine' + str(numpy.mean(report))+" | median : " + str(numpy.median(report)) + " | std : " + str(numpy.std(report)))
    ax3.hist(original_sample, color = 'chartreuse')
    ax3.set_title('Sample Proportions' + str(numpy.mean(original_sample))+" | median : " + str(numpy.median(original_sample)) + " | std : " + str(numpy.std(original_sample)))
    f.subplots_adjust(hspace=2)
    pl.show()


if __name__ == '__main__':
    main()
