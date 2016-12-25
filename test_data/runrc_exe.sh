W=/home/dugan/Software/wine-1.7.3

LD_LIBRARY_PATH="$W/lib:$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH
PATH="$W/bin:$PATH"
export PATH
WINEDLLPATH="$W/lib/wine/fakedlls"
export WINEDLLPATH
WINELOADER="$W/bin/wine"
export WINELOADER
WINEPREFIX="$HOME/.local/share/wineprefixes/bottle"
export WINEPREFIX
WINESERVER="$W/bin/wineserver"
export WINESERVER
WINEVERPATH="$W"
export WINEVERPATH
