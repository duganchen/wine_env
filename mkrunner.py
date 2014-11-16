#!/usr/bin/env python

import argparse
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('bottle', help='The name of the Wine bottle, e.g. PvZ')
    parser.add_argument(
        '--wine', help='The path to the Wine executable to use'
    )
    args = parser.parse_args()

    prefix = os.path.join(
        '$HOME', '.local', 'share', 'wineprefixes', args.bottle)

    if args.wine:
        print wine_template.format(
            W=os.path.expanduser(os.path.dirname(args.wine)),
            prefix=prefix)
    else:
        print bottle_template.format(prefix=prefix)


bottle_template = """#!/usr/bin/env bash
export WINEPREFIX={prefix}
wine $@"""

wine_template = """#!/usr/bin/env bash
export WINEVERPATH={W}
export PATH={W}:$PATH
export WINESERVER={W}/bin/wineserver
export WINELOADER={W}/bin/wine
export WINEDLLPATH={W}/lib/wine/fakedlls
export LD_LIBRARY_PATH={W}/lib:$LD_LIBRARY_PATH
export WINEPREFIX={prefix}
wine $@"""


if __name__ == '__main__':
    main()
