from numpy import *
import scipy as scipy
from pandas import *
from pandasurvey.datasets import *

from rpy2.robjects.packages import importr

import rpy2.robjects as ro
import pandas.rpy.common as com


def test_anes_main():
    r_df = com.convert_to_r_dataframe(
        load_rengine_weights()[['AgeRecode', 'Gender',
                                'IncomeRecode', 'HispanicRecode', 'RaceRecoder1',
                                'Cell']].dropna())

    ro.globalenv['data'] = r_df
    ro.r('data')
    ro.r('AgeRecode <- c(.07,.22,.2,.2,.21,0,0)')
    ro.r('Gender <- c(.5,.5)')
    ro.r('IncomeRecode <- c(.17,.21,.25,.16,.11,0,0)')
    ro.r('HispanicRecode <- c(.09,.91)')
    ro.r('RaceRecoder1 <- c(.15,.85)')
    ro.r('Cell <- c(1/7,1/7,1/7,1/7,1/7,1/7,1/7)')
    ro.r('targets <- list(AgeRecode, Gender, IncomeRecode, RaceRecoder1, Cell)')
    ro.r('names(targets) <- c("AgeRecode", "Gender", "IncomeRecode", "RaceRecoder1", "Cell")')
    ro.r('library(anesrake)')
    ro.r('data$caseid <- 1:length(data$Gender)')
    print ro.r('anesrakefinder(targets, data, choosemethod="total")')
    print ro.r('outsave <- anesrake(targets, data, caseid = data$caseid, verbose = T )')
    print ro.r('summary(outsave)')


if __name__ == '__main__':
    unittest.main()
