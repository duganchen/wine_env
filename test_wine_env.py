from wine_env import wine_rc

def test_runrc():

    result = """WINEPREFIX=$HOME/.local/share/wineprefixes/bottle
export WINEPREFIX
"""
    rc = wine_rc.RunRC('bottle')
    assert result == rc.get_rc()
