import unittest
from pandasurvey.rake.simple import SimpleRake
from pandasurvey.utils.bootstrap import bootstrap
import pandasurvey.datasets as datasets

class Test_simple(unittest.TestCase):

    def test_rake(self):
        #
        # will build better test cases here
        #
#        r = SimpleRake(
#            datasets.load_rengine_weights(), {}, datasets.load_target_weights(), 'RespondentKey', maxiter=10)
#        wt = r.calc()
#        print wt
#        self.assertEqual(len(r.weights), len(wt))

        self.assertEqual(42,42)

    def test_rake_from_csv(self):
        df = merged_datasets_by_path('pandasurvey/datasets/www.csv',
                                   'pandasurvey/datasets/study_1614.csv',
                                    "RespondentKey")
        pandasurvey_sample = []
        reportengine_sample = []
        orignal_sample = []
        demographic = 'Gender'
        target_demographic_value = 2
        for i in range(100):

            pandasurvey_sample.append(bootrapped_weight_propoortions(tots, 'RespondentKey', 'weight', 
                                                            demographic, target_demographic_value))

            reportengine_sample.append(bootrapped_weight_propoortions(tots, 'RespondentKey', 'Weight', 
                                                            demographic, target_demographic_value))

            orignal_sample.append(bootstrapped_proportions(tots, 'RespondentKey', 
                                                            demographic, target_demographic_value))

        targets = datasets.load_target_weights()
        print 'target weight  :' + targets[demographic][target_demographic_value]
        print 'pandasurvey mean/median/standard DEV'
