#!/usr/bin/env bash

set -o posix
set -e

RUNRC=~/.local/share/wineprefixes/$1/bin/runrc

if [ ! -f $RUNRC ];  then
    echo "$RUNRC not found."
    exit 1
fi

. ~/.local/share/wineprefixes/$1/bin/runrc

args=( $@ )
$2 ${args[@]:2}
