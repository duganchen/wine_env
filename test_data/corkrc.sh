if [ -n "_OLD_{}" ]; then
	WINESERVERPATH="$_OLD_WINESERVERPATH"
	export WINESERVERPATH
	unset _OLD_WINESERVERPATH
else
	unset WINESERVERPATH
fi

if [ -n "_OLD_{}" ]; then
	PATH="$_OLD_PATH"
	export PATH
	unset _OLD_PATH
fi

if [ -n "_OLD_{}" ]; then
	WINESERVER="$_OLD_WINESERVER"
	export WINESERVER
	unset _OLD_WINESERVER
else
	unset WINESERVER
fi

if [ -n "_OLD_{}" ]; then
	WINELOADER="$_OLD_WINELOADER"
	export WINELOADER
	unset _OLD_WINELOADER
else
	unset WINELOADER
fi

if [ -n "_OLD_{}" ]; then
	WINEDLLPATH="$_OLD_WINEDLLPATH"
	export WINEDLLPATH
	unset _OLD_WINEDLLPATH
else
	unset WINEDLLPATH
fi

if [ -n "_OLD_{}" ]; then
	LD_LIBRARY_PATH="$_OLD_LD_LIBRARY_PATH"
	export LD_LIBRARY_PATH
	unset _OLD_LD_LIBRARY_PATH
else
	unset LD_LIBRARY_PATH
fi

if [ -n "_OLD_{}" ]; then
	WINEPREFIX="$_OLD_WINEPREFIX"
	export WINEPREFIX
	unset _OLD_WINEPREFIX
else
	unset WINEPREFIX
fi
