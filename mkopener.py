#!/usr/bin/env python

import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('bottle', help='The name of the Wine bottle, e.g. PvZ')
    parser.add_argument(
        '--wine', help='The path to the Wine executable to use'
    )
    args = parser.parse_args()

    set_wine = ''
    unset_wine = ''

    if args.wine is not None:
        if not os.path.isfile(args.wine):
            print 'Wine must be the path to an executable'
            sys.exit(1)

        set_wine = set_wine_template.format(path=os.path.dirname(args.wine))
        unset_wine = unset_wine_template

    print template.format(
        bottle=args.bottle, set_wine=set_wine, unset_wine=unset_wine
    )

template = """# This file must be used with "source bin/uncork" *from bash*
# you cannot run it directly

cork () {{

    # reset old environment variables

    unset WINEPREFIX

    # This should detect bash and zsh, which have a hash command that must
    # be called to get it to forget past commands.  Without forgetting
    # past commands the $PATH changes we made may not be respected
    if [ -n "$BASH" -o -n "$ZSH_VERSION" ] ; then
        hash -r 2>/dev/null
    fi

    if [ -n "$_OLD_BOTTLE_PS1" ] ; then
        PS1="$_OLD_BOTTLE_PS1"
        export PS1
        unset _OLD_BOTTLE_PS1
    fi

{unset_wine}

    if [ ! "$1" = "nondestructive" ] ; then
        # Self destruct!
        unset -f cork
    fi
}}

# unset irrelevant variables
cork nondestructive

_OLD_BOTTLE_PS1="$PS1"
PS1="({bottle})$PS1"
export PS1

WINEPREFIX=$HOME/.local/share/wineprefixes/{bottle}
export WINEPREFIX

{set_wine}

# This should detect bash and zsh, which have a hash command that must
# be called to get it to forget past commands.  Without forgetting
# past commands the $PATH changes we made may not be respected
if [ -n "$BASH" -o -n "$ZSH_VERSION" ] ; then
    hash -r 2>/dev/null
fi"""

set_wine_template = """_OLD_PATH="$PATH"
PATH={path}:$PATH
export PATH"""

unset_wine_template = """   if [ -n "$_OLD_PATH" ] ; then
        PATH="$_OLD_PATH"
        export PATH
        unset _OLD_PATH
    fi
"""


if __name__ == '__main__':
    main()
