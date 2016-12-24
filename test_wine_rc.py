from wine_env import wine_rc
import os

exe = '~/Software/wine-1.7.3/bin/wine'


def get_path(filename):
    directory = os.path.dirname(__file__)
    return os.path.join(directory, 'test_data', filename)


def test_runrc():
    rc = wine_rc.RunRC('bottle')
    with open(get_path('runrc.sh')) as f:
        expected = f.read()
    assert expected == rc.get_rc()


def test_runrc_exe():
    rc = wine_rc.RunRC('bottle', exe) 
    with open(get_path('runrc_exe.sh')) as f:
        expected = f.read()
    assert expected == rc.get_rc()


def test_uncorkc():
    rc = wine_rc.UncorkRC('bottle')
    with open(get_path('uncorkrc.sh')) as f:
        expected = f.read()
    assert expected == rc.get_rc()


def test_uncorkc_exe():
    rc = wine_rc.UncorkRC('bottle', exe) 
    with open(get_path('uncorkrc_exe.sh')) as f:
        expected = f.read()
    assert expected == rc.get_rc()


def test_corkrc():
    rc = wine_rc.CorkRC('bottle')
    with open(get_path('corkrc.sh')) as f:
        expected = f.read()
    assert expected == rc.get_rc()


def test_corkrc_exe():

    rc = wine_rc.CorkRC('bottle', exe)
    with open(get_path('corkrc_exe.sh')) as f:
        expected = f.read()
    assert expected == rc.get_rc()


def test_runrc_fish():
    rc = wine_rc.RunRCFish('bottle')
    with open(get_path('runrc.fish')) as f:
        expected = f.read()
    assert expected == rc.get_rc()


def test_runrc_exe_fish():
    rc = wine_rc.RunRCFish('bottle', exe) 
    with open(get_path('runrc_exe.fish')) as f:
        expected = f.read()
    assert expected == rc.get_rc()


def test_uncorkc_fish():
    rc = wine_rc.UncorkRCFish('bottle')
    with open(get_path('uncorkrc.fish')) as f:
        expected = f.read()
    assert expected == rc.get_rc()


def test_uncorkc_exe_fish():
    rc = wine_rc.UncorkRCFish('bottle', exe)
    with open(get_path('uncorkrc_exe.fish')) as f:
        expected = f.read()
    assert expected == rc.get_rc()


def test_corkrc_fish():
    rc = wine_rc.CorkRCFish('bottle')
    with open(get_path('corkrc.fish')) as f:
        expected = f.read()
    assert expected == rc.get_rc()


def test_corkrc_exe_fish():

    rc = wine_rc.CorkRCFish('bottle', exe)
    with open(get_path('corkrc_exe.fish')) as f:
        expected = f.read()
    assert expected == rc.get_rc()
