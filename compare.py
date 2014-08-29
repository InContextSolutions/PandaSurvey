import math
import pandas as pd
import numpy
import scipy.stats as stats
import matplotlib.pyplot as pl
from pandasurvey.datasets import *
from pandasurvey.utils.bootstrap import *



def plot_gender_prop():

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

def weight_regress():

    thirty = pd.merge( load_thirtyiters(),load_rengine_weights(), on="RespondentKey" )
    pl.plot(thirty['weight'].tolist(), thirty['Weight'].tolist(), 'rs')
    slope, intercept, r_value, p_value, std_err = stats.linregress(thirty['weight'].tolist(), thirty['Weight'].tolist())
    pl.title('R value : '+ str(r_value))
    pl.show()

def main():
    #modulize and stuff
    weight_regress()


if __name__ == '__main__':
    main()
