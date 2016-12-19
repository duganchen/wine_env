from wine_env import wine_rc
import os


def get_path(filename):
    directory = os.path.dirname(__file__)
    return os.path.join(directory, 'test_data', filename)


def test_runrc():
    rc = wine_rc.RunRC('bottle')
    with open(get_path('runrc.sh')) as f:
        expected = f.read()
    assert expected == rc.get_rc()


def test_runrc_exe():
    rc = wine_rc.RunRC('bottle', '/path/to/wine64-1.4/bin/wine')
    with open(get_path('runrc_exe.sh')) as f:
        expected = f.read()
    assert expected == rc.get_rc()


def test_uncorkc():
    rc = wine_rc.UncorkRC('bottle')
    with open(get_path('uncorkrc.sh')) as f:
        expected = f.read()
    assert expected == rc.get_rc()


def test_uncorkc_exe():
    rc = wine_rc.UncorkRC('bottle', '/path/to/wine-1.7.3/bin/wine')
    with open(get_path('uncorkrc_exe.sh')) as f:
        expected = f.read()
    assert expected == rc.get_rc()


def test_corkrc():
    rc = wine_rc.CorkRC('bottle')
    with open(get_path('corkrc.sh')) as f:
        expected = f.read()
    assert expected == rc.get_rc()


def test_corkrc_exe():

    rc = wine_rc.CorkRC('bottle', '/path/to/wine-1.7.3/bin/wine')
    with open(get_path('corkrc_exe.sh')) as f:
        expected = f.read()
    assert expected == rc.get_rc()
