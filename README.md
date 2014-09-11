# PandaSurvey

[![Build Status](https://api.shippable.com/projects/5411f298814f6b1f6a9fa132/badge?branchName=master)](https://app.shippable.com/projects/5411f298814f6b1f6a9fa132/builds/latest)

Survey Weighting Methods for Pandas DataFrames

## Installation

```bash
git clone git@github.com:InContextSolutions/pandasurvey.git
pip install .
```

## Using SimpleRake

`SimpleRake` weights survey respondents such that the weighted demographic proportions match a target demographic. That is, weights are set to match marginal distributions. Graphically, for a 2-demographic space, this iterative process resembles scalar mulitplication along the `rim` of a contingency table. The process as implemented supports any number of demographic dimensions.

### Example: The `People` dataset

Two sample datasets are included in the distribution. The `People` dataset is drawn from the 2010 census. In this proof-on-concept, we import the dataset, define the target proportions, and execute the raking procedure. For column definitions, see the [datasets README](https://github.com/InContextSolutions/pandasurvey/blob/master/pandasurvey/datasets/README.md).

Note: In this example, we don't perform any recoding over the data (such as age) and only rake one dimension.

```python
from pandasurvey.rake.simple import SimpleRake
import pandasurvey.datasets as datasets

df_in = datasets.load_people()
print  '%.2f' % (df_in[df_in.Gender==1].shape[0]/9999.,)
# prints 0.49

target_proportions = {"Gender": {1: .2, 2: .8}}

rk = SimpleRake(df_in, target_proportions)
df_out = rk.calc()

print '%.2f' % (df_out[df_out.Gender==1]['weight'].sum()/9999.,)
# print 0.20
```
