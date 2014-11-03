"""PandaSurvey includes two unique datasets for testing purpuses: `People` and a sample study. The `People` file is from the 2010 US Census. The sample study is from a small survey performed at InContext Solutions in 2014 (specific survey details withheld)"""

import os
import pandas


def _path(name):
    root, _ = os.path.split(__file__)
    return os.path.join(root, name)


def load_people():
    """Returns the `People` dataset as a DataFrame. The data consists of 9999 individuals with age, disability status, marital status, race, and gender demographic information. Columns and their codes are described below:

    - Age
        - Non-negative integer
        - May include zeros
    - Disability
        - 1: Disabled
        - 2: Not disabled
    - MarritalStatus
        - 1: Married
        - 2: Widowed
        - 3: Divorced
        - 4: Separated
        - 5: Never married or under 15 years old
    - Race
        - 1: White alone
        - 2: Black or African American alone
        - 3: American Indian alone
        - 4: Alaska Native alone
        - 5: American Indian and Alaska Native tribes specified; or American Indian or Alaska native, not specified and no other races
        - 6: Asian alone
        - 7: Native Hawaiian and Other Pacific Islander alone
        - 8: Some other race alone
        - 9: Two or more major race groups
    - Gender
        - 1: Male
        - 2: Female
    """
    return pandas.read_csv(_path("People.csv"))


def load_sample_study():
    """Returns a sample dataset describing demographics in coded format from 2092 respondents. The study consists of 7 cells and demographics considered include age, gender, income, hispanic, and race."""
    df = pandas.read_csv(_path("SampleStudy.csv"))
    del df['Weight']
    return df


def load_sample_weights():
    """Returns individual weights from the sample survey calculated via a raking method previously implemented in R."""
    df = pandas.read_csv(_path("SampleStudy.csv"))
    return df['Weight']


def load_sample_proportions():
    """Returns the target sample proportions that correspond to the sample survey.

    +-------------+-------------+-------------------+
    | Demographic | Coded Value | Target Proportion |
    +=============+=============+===================+
    | Age         | 1           | 0.07              |
    +-------------+-------------+-------------------+
    | Age         | 2           | 0.22              |
    +-------------+-------------+-------------------+
    | Age         | 3           | 0.2               |
    +-------------+-------------+-------------------+
    | Age         | 4           | 0.2               |
    +-------------+-------------+-------------------+
    | Age         | 5           | 0.21              |
    +-------------+-------------+-------------------+
    | Gender      | 1           | 0.5               |
    +-------------+-------------+-------------------+
    | Gender      | 2           | 0.5               |
    +-------------+-------------+-------------------+
    | Income      | 1           | 0.17              |
    +-------------+-------------+-------------------+
    | Income      | 2           | 0.21              |
    +-------------+-------------+-------------------+
    | Income      | 3           | 0.25              |
    +-------------+-------------+-------------------+
    | Income      | 4           | 0.16              |
    +-------------+-------------+-------------------+
    | Income      | 5           | 0.11              |
    +-------------+-------------+-------------------+
    | Hispanic    | 1           | 0.09              |
    +-------------+-------------+-------------------+
    | Hispanic    | 2           | 0.91              |
    +-------------+-------------+-------------------+
    | Race        | 0           | 0.15              |
    +-------------+-------------+-------------------+
    | Race        | 1           | 0.85              |
    +-------------+-------------+-------------------+
    """
    weights = {}
    with open(_path("SampleWeights.csv")) as csv_in:
        for line in csv_in:
            demo, category, proportion = line.split(',')
            if demo not in weights:
                weights[demo] = {}
            weights[demo][int(category)] = float(proportion)
    return weights
