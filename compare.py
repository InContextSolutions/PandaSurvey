import pandas as pd
import numpy
import matplotlib.pyplot as pl


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
    temp =
    for i in own_temp:
        if i[0][1] == target_value:
            temp.append(i[0][0])
    return s / sum(map(lambda i: i[0][0], own_temp)) 

def bootstrapped_proportions(df, key_column, proportion_column, target_value ):

    keys = bootstrap(
        len(df), df, weight_column='NA', key_column="RespondentKey")
    own_temp = [df[df.RespondentKey == k][
        [ proportion_column]].values for k in keys]
    return len(df.query(proportion_column + "=="+str(target_value))/len(df) 

def compare_weight_proportions():
    pass

def main():
    #modulize and stuff

    tots = merged_datasets_by_path('pandasurvey/datasets/www.csv',
                                   'pandasurvey/datasets/study_1614.csv',
                                    "RespondentKey")
    own = []
    report = []
    for i in range(2):

        own.append(bootrapped_weight_propoortions(tots, 'RespondentKey', 'weight','Gender', 2))

        report.append(bootrapped_weight_propoortions(tots, 'RespondentKey', 'Weight','Gender', 2))

        orignal_sample(bootstrapped_proportions(tots, 'RespondentKey', ))

    print own
    print report
    f, (ax1, ax2) = pl.subplots(2, sharex=True, sharey=True)
    ax1.hist(own)
    ax1.set_title('first is the pandasurvey')
    ax2.hist(report)
    f.subplots_adjust(hspace=0)
    pl.show()


if __name__ == '__main__':
    main()
