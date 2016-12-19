from wine_env import wine_rc

def test_runrc():

    expected = """WINEPREFIX=$HOME/.local/share/wineprefixes/bottle
export WINEPREFIX
"""
    rc = wine_rc.RunRC('bottle')
    assert expected == rc.get_rc()


def test_runrc_exe():

    expected = """W=/path/to/wine64-1.4

WINESERVER="$W/bin/wineserver"
export WINESERVER
LD_LIBRARY_PATH="$W/lib:$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH
WINELOADER="$W/bin/wine"
export WINELOADER
WINESERVERPATH="$W"
export WINESERVERPATH
WINEDLLPATH="$W/lib/wine/fakedlls"
export WINEDLLPATH
PATH="$W/bin:$PATH"
export PATH
WINEPREFIX="$HOME/.local/share/wineprefixes/bottle"
export WINEPREFIX
"""
    rc = wine_rc.RunRC('bottle', '/path/to/wine64-1.4/bin/wine')
    assert expected == rc.get_rc()

