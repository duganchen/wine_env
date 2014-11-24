#!/bin/sh


if [ "$#" -lt 2 ]; then
	cat <<- EOF
	Usage: bottle-run bottle command [args]
	E.g. bottle-run PvZ winecfg
	e.g. bottle-run PvZ wine notepad
	e.g. bottle-run PvZ wine iexplore http://www.google.ca/
	e.g. bottle-run PvZ winetricks --no-isolate steam
	EOF
    exit 1
fi

BOTTLE=$1

if [ ! -d "$HOME/.local/share/wineprefixes/$BOTTLE" ]; then
	cat <<- EOF
	Bottle "$BOTTLE" not found"
	Run "lsp" to list bottles
	Run "bottle" to create bottles
	EOF
	exit 1
fi

RUNRC="$HOME/.local/share/wineprefixes/$BOTTLE/bin/runrc.sh"

if [ ! -f "$RUNRC" ];  then
    echo "$RUNRC not found."
    echo "Please use mkbottle to recreate the bottle."
    exit 1
fi

# If we already have an environment loaded, clear it out.
if [ "$WINEPREFIX" != "" ] &&  [ -f "$WINEPREFIX/bin/uncorkrc.sh" ]; then
    . "$WINEPREFIX/bin/uncorkrc.sh"
fi

. "$RUNRC"

shift 1
"$@"
