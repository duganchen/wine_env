if type cork &> /dev/null; then
	cork
fi

cork() {

	. "$HOME/.local/share/wineprefixes/bottle/bin/corkrc.sh"

	if [ -n "$_OLD_WD" ]; then
		cd "$_OLD_WD"
	fi

	if [ -z "$WINE_ENV_DISABLE_PROMPT" ]; then
		PS1="$_OLD_PS1"
		export PS1
		unset _OLD_PS1
	fi

	if [ -z "$_OLD_WD" ]; then
		cd $_OLD_WD
		unset _OLD_WD
	fi

	unset W
	unset BOTTLE
	unset -f goc
	unset -f cork
}

if [ -n "$WINESERVERPATH" ]; then
	if [ -z "$_OLD_WINESERVERPATH" ]; then
		_OLD_WINESERVERPATH="$WINESERVERPATH"
		export _OLD_WINESERVERPATH
	fi
fi

if [ -n "$PATH" ]; then
	if [ -z "$_OLD_PATH" ]; then
		_OLD_PATH="$PATH"
		export _OLD_PATH
	fi
fi

if [ -n "$WINESERVER" ]; then
	if [ -z "$_OLD_WINESERVER" ]; then
		_OLD_WINESERVER="$WINESERVER"
		export _OLD_WINESERVER
	fi
fi

if [ -n "$WINELOADER" ]; then
	if [ -z "$_OLD_WINELOADER" ]; then
		_OLD_WINELOADER="$WINELOADER"
		export _OLD_WINELOADER
	fi
fi

if [ -n "$WINEDLLPATH" ]; then
	if [ -z "$_OLD_WINEDLLPATH" ]; then
		_OLD_WINEDLLPATH="$WINEDLLPATH"
		export _OLD_WINEDLLPATH
	fi
fi

if [ -n "$LD_LIBRARY_PATH" ]; then
	if [ -z "$_OLD_LD_LIBRARY_PATH" ]; then
		_OLD_LD_LIBRARY_PATH="$LD_LIBRARY_PATH"
		export _OLD_LD_LIBRARY_PATH
	fi
fi

if [ -n "$WINEPREFIX" ]; then
	if [ -z "$_OLD_WINEPREFIX" ]; then
		_OLD_WINEPREFIX="$WINEPREFIX"
		export _OLD_WINEPREFIX
	fi
fi
WINEPREFIX=$HOME/.local/share/wineprefixes/bottle
export WINEPREFIX

BOTTLE="bottle"
export BOTTLE

if [ -z "$WINE_ENV_DISABLE_PROMPT" ]; then
	_OLD_PS1="$PS1"
	PS1="(bottle)$PS1"
fi

_OLD_WD="$(pwd)"
cd "$HOME/.local/share/wineprefixes/bottle"

goc() {
	cd "$WINEPREFIX/drive_c"
}
