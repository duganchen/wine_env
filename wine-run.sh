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

env -i _wine-run $@
