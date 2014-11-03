from setuptools import setup


install_requires = [
    'numpy',
    'pandas',
]

tests_require = [
    'nose',
    'coverage'
]

setup(
    name="PandaSurvey",
    version="0.100",
    author="InContext Solutions",
    author_email="quant@incontextsolutions.com",
    url="http://www.incontextsolutions.com/",
    description="A survey weighting utility for Pandas' DataFrames",
    packages=['PandaSurvey'],
    setup_requires=['nose'],
    install_requires=install_requires,
    tests_require=tests_require
)
