Getting Started
===============

Installation
------------

From Source
~~~~~~~~~~~

::

    git clone git@github.com:InContextSolutions/PandaSurvey.git
    cd PandaSurvey
    pip install .

From PyPI
~~~~~~~~~

::

    pip install PandaSurvey

Basic Usage
-----------

The goal of this utility is to calculate respondent weights that allow one to transform a dataset into something more appropriate for inference. Two sample datasets are included for testing purposes. As of this version of PandaSurvey, only raking has been implemented.

Example
~~~~~~~

We'll rake the included `People` dataset to match a target demographic consisting of 80% female and 50% married respondents. First, we import the `People` dataset and view summary information.

.. code-block:: ipython

    In [1]: from PandaSurvey import datasets

    In [2]: df = datasets.load_people()  

    In [3]: df.head(5)
    Out[3]: 
       Age  Disability  MaritalStatus  Race  Gender
    0   80           1              1     1       1
    1   60           2              1     1       2
    2   27           2              5     1       1
    3   59           2              1     1       1
    4   60           2              3     1       2

    In [4]: df = df[['Gender', 'MaritalStatus']]

    In [5]: df.head(5)
    Out[5]: 
        Gender  MaritalStatus
    0        1              1
    1        2              1
    2        1              5
    3        1              1
    4        2              3

    In [6]: import pandas

    In [7]: pandas.crosstab(df.Gender, df.MaritalStatus)
    Out[7]: 
    MaritalStatus     1    2    3   4     5
    Gender                                                         
    1              2159  125  388  62  2171
    2              2090  411  499  99  1995

From above, the unweighted sample is about evenly split on gender and slightly more than 40% of the respondents are married (status equals one).

We only care about married and unmarried status, so we can aggregate responses above one together. We're going to `recode` non-married responses to equal two. First, we create a SimpleRake object:

.. code-block:: ipython

    In [8]: from PandaSurvey.rake.simple import SimpleRake

    In [9]: rk = SimpleRake(df, {'Gender': {1: 0.20, 2: 0.80}, 'MaritalStatus': {1: 0.50, 2: 0.50}})

Note the second parameter we gave SimpleRake. That dictionary defines the target demographic we want to get after applying weights. Now that we have a SimpleRake object, we can recode:

.. code-block:: ipython

    In [10]: rk.recode({'MaritalStatus': lambda x: 1 + 1*(x != 1)})

    In [11]: pandas.crosstab(rk.df.Gender, rk.df.MaritalStatus)
    Out[11]: 
    MaritalStatus     1     2
    Gender                   
    1              2159  2746
    2              2090  3004

We've transformed our dataset and are ready to calculate weights.

.. code-block:: ipython

    In [12]: wt_df = rk.calc()

    In [13]: wt_df.head(5)
    Out[13]: 
       Gender  MaritalStatus    weight
    0       1              1  0.485772
    1       2              1  1.890296
    2       1              2  0.346333
    3       1              1  0.485772
    4       2              2  1.347693

When `calc` is called, the raking procedure iteratively updates weights (starting from uniform weighting) until the marginal distributions match the target proportions.

So, how did we do?

.. code-block:: ipython

    In [14]: wt_df[wt_df.Gender==2]['weight'].sum() / wt_df.weight.sum()
    Out[14]: 0.79999901598236345

    In [15]: wt_df[wt_df.MaritalStatus==1]['weight'].sum() / wt_df.weight.sum()
    Out[15]: 0.50000000000002287

    In [16]: rk.loss(wt_df.weight.values)
    Out[16]: 0.37643439668734002

We can see that the gender and marital status proportions are nearly equal to the target (within a reasonable convergence tolerance).

The last statement (`loss`) approximates the increase in variance due to weighting. We can approximate the design effect by adding one to the loss (about 1.38, in this case).
