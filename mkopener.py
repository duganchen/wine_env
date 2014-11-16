#!/usr/bin/env python

# Note: this uses some code from VirtualEnv.

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

    wine_prefix = os.path.join(
        '$HOME', '.local', 'share', 'wineprefixes', args.bottle)

    if args.wine is not None:
        if not os.path.isfile(args.wine):
            print 'Wine must be the path to an executable'
            sys.exit(1)

        wine_ver_path = os.path.expanduser(
            os.path.dirname(os.path.dirname(args.wine)))

        path = ':'.join([os.path.join(wine_ver_path, 'bin'), '$PATH'])
        wine_server = os.path.join(wine_ver_path, 'bin', 'wineserver')
        wine_loader = os.path.join(wine_ver_path, 'bin', 'wine')
        wine_dll_path = os.path.join(wine_ver_path, 'lib', 'wine', 'fakedlls')
        ld_library_path = ':'.join(
            [os.path.join(wine_ver_path, 'lib'), '$LD_LIBRARY_PATH']
        )

        print wine_template.format(
            wine_ver_path=wine_ver_path,
            path=path,
            wine_server=wine_server,
            wine_loader=wine_loader,
            wine_dll_path=wine_dll_path,
            ld_library_path=ld_library_path,
            wine_prefix=wine_prefix)


    print template.format(
        bottle=args.bottle, set_wine=set_wine, unset_wine=unset_wine
    )


wine_template = """# This file must be used with "source bin/uncork" *from bash*
# you cannot run it directly

cork () {{

    # reset old environment variables

    unset WINEPREFIX
    unset WINEVERPATH
    unset WINESERVER
    unset WINELOADER
    unset WINEDLLPATH

    # This should detect bash and zsh, which have a hash command that must
    # be called to get it to forget past commands.  Without forgetting
    # past commands the $PATH changes we made may not be respected
    if [ -n "$BASH" -o -n "$ZSH_VERSION" ] ; then
        hash -r 2>/dev/null
    fi

    if [ -n "$_OLD_BOTTLE_PS1" ] ; then
        export PS1="$_OLD_BOTTLE_PS1"
        unset _OLD_BOTTLE_PS1
    fi

    if [ -n "$_OLD_PATH" ] ; then
        export PATH="$_OLD_PATH"
        unset _OLD_PATH
    fi

    if [ -n "$_OLD_LD_LIBRARY_PATH" ] ; then
        export LD_LIBRARY_PATH="$_OLD_LD_LIBRARY_PATH"
        unset _OLD_LD_LIBRARY_PATH
    fi

    if [ -n "$_OLD_CWD" ] ; then
        cd $_OLD_CWD
        unset _OLD_CWD
    fi

    if [ ! "$1" = "nondestructive" ] ; then
        # Self destruct!
        unset -f cork
    fi
}}

# unset irrelevant variables
cork nondestructive

_OLD_BOTTLE_PS1="$PS1"
export PS1="({bottle})$PS1"

export WINEPREFIX={wine_prefix}

export WINEVERPATH={wine_ver_path}
export WINESERVER={wine_server}
export WINELOADER={wine_loader}
export WINEDLLPATH={wine_dll_path}

_OLD_PATH="$PATH"
export PATH={path}

_OLD_LD_LIBRARY_PATH="$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH={ld_library_path}

_OLD_CWD=$(pwd)
cd $WINEPREFIX

# This should detect bash and zsh, which have a hash command that must
# be called to get it to forget past commands.  Without forgetting
# past commands the $PATH changes we made may not be respected
if [ -n "$BASH" -o -n "$ZSH_VERSION" ] ; then
    hash -r 2>/dev/null
fi

# Note: This file is based on code from VirualEnv."""


bottle_template = """# This file must be used with "source bin/uncork" *from bash*
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
        export PS1="$_OLD_BOTTLE_PS1"
        unset _OLD_BOTTLE_PS1
    fi

    if [ -n "$_OLD_CWD" ] ; then
        cd $_OLD_CWD
        unset _OLD_CWD
    fi

    if [ ! "$1" = "nondestructive" ] ; then
        # Self destruct!
        unset -f cork
    fi
}}

# unset irrelevant variables
cork nondestructive

_OLD_BOTTLE_PS1="$PS1"
export PS1="({bottle})$PS1"

export WINEPREFIX={wine_prefix}

_OLD_CWD=$(pwd)
cd $WINEPREFIX

# This should detect bash and zsh, which have a hash command that must
# be called to get it to forget past commands.  Without forgetting
# past commands the $PATH changes we made may not be respected
if [ -n "$BASH" -o -n "$ZSH_VERSION" ] ; then
    hash -r 2>/dev/null
fi
"""


if __name__ == '__main__':
    main()
