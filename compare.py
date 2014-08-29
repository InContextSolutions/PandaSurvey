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
    orignal_sample = []
    for i in range(100):

        own.append(bootrapped_weight_propoortions(tots, 'RespondentKey', 'weight','Gender', 2))

        report.append(bootrapped_weight_propoortions(tots, 'RespondentKey', 'Weight','Gender', 2))

        orignal_sample.append(bootstrapped_proportions(tots, 'RespondentKey', 'Gender',2))

    print own
    print report
    print orignal_sample
    f, (ax1, ax2, ax3) = pl.subplots(3, sharex=True, sharey=True)
    f.suptitle('Gender proportions bootstrapped')
    ax1.hist(own)
    ax1.set_title('pandasurvey')
    ax2.hist(report)
    ax2.set_title('Report Engine')
    ax3.hist(orignal_sample)
    ax3.set_title('Sample Proportions')
    f.subplots_adjust(hspace=0)
    pl.show()


if __name__ == '__main__':
    main()
