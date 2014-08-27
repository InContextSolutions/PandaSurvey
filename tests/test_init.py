import pandasurvey


def test_version():
    assert pandasurvey.__version__ is not None, "no version found"
