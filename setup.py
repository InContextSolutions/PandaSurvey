from setuptools import setup, find_packages


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
    version="0.11",
    author="InContext Solutions",
    author_email="quant@incontextsolutions.com",
    url="http://www.incontextsolutions.com/",
    download_url="https://github.com/InContextSolutions/PandaSurvey/tarball/v0.1",
    description="Survey weighting utility for the Pandas DataFrame",
    keywords=['raking', 'Pandas', 'survey'],
    packages=find_packages(),
    setup_requires=['nose'],
    install_requires=install_requires,
    tests_require=tests_require,
    entry_points={},
    classifiers=[]
)
