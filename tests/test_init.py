import PandasRake


def test_version():
    assert PandasRake.__version__ is not None, "no version found"
