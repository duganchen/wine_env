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

    wine_prefix = os.path.join(
        '$HOME', '.local', 'share', 'wineprefixes', args.bottle)

    if args.wine:

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
    else:
        print bottle_template.format(wine_prefix=wine_prefix)


bottle_template = """#!/usr/bin/env bash
export WINEPREFIX={wine_prefix}
wine $@"""

wine_template = """#!/usr/bin/env bash
export WINEVERPATH={wine_ver_path}
export PATH={path}
export WINESERVER={wine_server}
export WINELOADER={wine_loader}
export WINEDLLPATH={wine_dll_path}
export LD_LIBRARY_PATH={ld_library_path}
export WINEPREFIX={wine_prefix}
wine $@"""


if __name__ == '__main__':
    main()
