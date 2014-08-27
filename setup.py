import os
from setuptools import setup
import pandasurvey


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


install_requires = [
    'numpy',
    'pandas'
]

tests_require = [
    'nose',
    'coverage'
]

setup(
    name="pandasurvey",
    version=pandasurvey.__version__,
    author="InContext Solutions",
    author_email="tristan.wietsma@incontextsolutions.com",
    url="http://www.incontextsolutions.com/",
    description="A survey weighting utility for use with Pandas dataframes",
    packages=["pandasurvey"],
    long_description=read('README.md'),
    setup_requires=['nose'],
    install_requires=install_requires,
    tests_require=tests_require,
    entry_points={},
)
