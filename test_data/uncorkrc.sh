if type cork &> /dev/null; then
	cork
fi

cork() {

	if [ -n "$_OLD_WINEVERPATH" ]; then
		WINEVERPATH="$_OLD_WINEVERPATH"
		export WINEVERPATH
		unset _OLD_WINEVERPATH
	else
		unset WINEVERPATH
	fi

	if [ -n "$_OLD_PATH" ]; then
		PATH="$_OLD_PATH"
		export PATH
		unset _OLD_PATH
	fi

	if [ -n "$_OLD_WINESERVER" ]; then
		WINESERVER="$_OLD_WINESERVER"
		export WINESERVER
		unset _OLD_WINESERVER
	else
		unset WINESERVER
	fi

	if [ -n "$_OLD_WINELOADER" ]; then
		WINELOADER="$_OLD_WINELOADER"
		export WINELOADER
		unset _OLD_WINELOADER
	else
		unset WINELOADER
	fi

	if [ -n "$_OLD_WINEDLLPATH" ]; then
		WINEDLLPATH="$_OLD_WINEDLLPATH"
		export WINEDLLPATH
		unset _OLD_WINEDLLPATH
	else
		unset WINEDLLPATH
	fi

	if [ -n "$_OLD_LD_LIBRARY_PATH" ]; then
		LD_LIBRARY_PATH="$_OLD_LD_LIBRARY_PATH"
		export LD_LIBRARY_PATH
		unset _OLD_LD_LIBRARY_PATH
	else
		unset LD_LIBRARY_PATH
	fi

	if [ -n "$_OLD_WINEPREFIX" ]; then
		WINEPREFIX="$_OLD_WINEPREFIX"
		export WINEPREFIX
		unset _OLD_WINEPREFIX
	else
		unset WINEPREFIX
	fi

	if [ -z "$WINE_ENV_DISABLE_PROMPT" ]; then
		PS1="$_OLD_PS1"
		export PS1
		unset _OLD_PS1
	fi

	unset W
	unset BOTTLE
	unset -f goc
	unset -f cork
}

if [ -n "$WINEVERPATH" ]; then
	if [ -z "$_OLD_WINEVERPATH" ]; then
		_OLD_WINEVERPATH="$WINEVERPATH"
		export _OLD_WINEVERPATH
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

goc() {
	cd "$WINEPREFIX/drive_c"
}
