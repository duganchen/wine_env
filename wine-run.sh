#!/usr/bin/env bash

set -o posix
set -e

if [ "$#" -lt 2 ]; then
    echo Usage: wine-run bottle command [args]
    echo E.g. wine-run PvZ winecfg
    echo e.g. wine-run PvZ wine notepad
    echo e.g. wine-run PvZ wine iexplore http://www.google.ca/
    echo e.g. wine-run PvZ winetricks --no-isolate steam
    exit 1
fi

if [ -f "$WINEPREFIX/bin/uncorkrc" ]; then
	. "$WINEPREFIX/bin/uncorkrc"
fi

RUNRC=~/.local/share/wineprefixes/$1/bin/runrc

if [ ! -f $RUNRC ];  then
    echo "$RUNRC not found."
    exit 1
fi

. ~/.local/share/wineprefixes/$1/bin/runrc

args=( $@ )
$2 ${args[@]:2}
