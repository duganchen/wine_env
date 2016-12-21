set W /path/to/wine-1.7.3

set -gx LD_LIBRARY_PATH $W/lib $LD_LIBRARY_PATH
set -gx PATH $W/bin $PATH
set -gx WINEDLLPATH $W/lib/wine/fakedlls
set -gx WINELOADER $W/bin/wine
set -gx WINEPREFIX $HOME/.local/share/wineprefixes/bottle
set -gx WINESERVER $W/bin/wineserver
set -gx WINESERVERPATH $W
