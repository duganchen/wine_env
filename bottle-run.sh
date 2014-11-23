#!/bin/sh

if [ "$#" -lt 2 ]; then
    echo Usage: bottle-run bottle command \[args\]
    echo E.g. bottle-run PvZ winecfg
    echo e.g. bottle-run PvZ wine notepad
    echo e.g. bottle-run PvZ wine iexplore http://www.google.ca/
    echo e.g. bottle-run PvZ winetricks --no-isolate steam
    exit 1
fi

# Will deal with this repetition later.

if [ ! -d "$HOME/.local/share/wineprefixes/$1" ]; then
    echo "$1 is not a bottle."
    echo Usage: bottle-run bottle command \[args\]
    echo E.g. bottle-run PvZ winecfg
    echo e.g. bottle-run PvZ wine notepad
    echo e.g. bottle-run PvZ wine iexplore http://www.google.ca/
    echo e.g. bottle-run PvZ winetricks --no-isolate steam
    exit 1
fi

RUNRC="$HOME/.local/share/wineprefixes/$1/bin/runrc"

if [ ! -f "$RUNRC" ];  then
    echo "$RUNRC not found."
    echo "Please use mkbottle to recreate the bottle."
    exit 1
fi

# If we already have an environment loaded, clear it out.
if [ -f "$WINEPREFIX/bin/uncorkrc" ]; then
    . "$WINEPREFIX/bin/uncorkrc"
fi

. "$HOME/.local/share/wineprefixes/$1/bin/runrc"

args=( $@ )
$2 ${args[@]:2}
