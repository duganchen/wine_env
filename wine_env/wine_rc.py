#!/usr/bin/env mpcpython

import argparse
from cStringIO import StringIO
import os
import sys


class Main(object):

    def __init__(self, rc_cls):
        self.__rc_cls = rc_cls

    def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'bottle', help='The name of the Wine bottle, e.g. PvZ'
        )
        parser.add_argument(
            '--wine', help='The path to the Wine executable to use'
        )
        args = parser.parse_args()

        if args.wine:

            if not os.path.isfile(args.wine):
                print 'Wine must be the path to an executable'
                sys.exit(1)

        wine_rc = self.__rc_cls(args.bottle, args.wine)

        print wine_rc.get_rc()


class WineRC(object):

    def __init__(self, bottle, wine_executable=None):

        self._prefix = os.path.join(
            '$HOME', '.local', 'share', 'wineprefixes', bottle
        )

        self._bottle = bottle

        self._wine = wine_executable
        if self._wine:
            self._wine = os.path.dirname(
                os.path.dirname(os.path.expanduser(self._wine))
            )

    def get_env(self):

        environment = {'WINEPREFIX': self._prefix}

        if not self._wine:
            return environment

        path = '"{}"'.format(':'.join([os.path.join('$W', 'bin'), '$PATH']))
        wine_server = '"{}"'.format(os.path.join('$W', 'bin', 'wineserver'))
        wine_loader = '"{}"'.format(os.path.join('$W', 'bin', 'wine'))
        wine_dll_path = '"{}"'.format(
            os.path.join('$W', 'lib', 'wine', 'fakedlls')
        )
        ld_library_path = '"{}"'.format(
            ':'.join([os.path.join('$W', 'lib'), '$LD_LIBRARY_PATH'])
        )

        environment['WINESERVERPATH'] = '"{}"'.format('$W')
        environment['PATH'] = path
        environment['WINESERVER'] = wine_server
        environment['WINELOADER'] = wine_loader
        environment['WINEDLLPATH'] = wine_dll_path
        environment['LD_LIBRARY_PATH'] = ld_library_path
        environment['WINEPREFIX'] = '"{}"'.format(self._prefix)

        return environment

    @staticmethod
    def get_all_keys():
        return (
            'WINESERVERPATH', 'PATH', 'WINESERVER', 'WINELOADER',
            'WINEDLLPATH', 'LD_LIBRARY_PATH', 'WINEPREFIX'
        )


class RunRC(WineRC):

    def get_rc(self):
        env = self.get_env()
        io = StringIO()
        if self._wine:
            io.write('W={}\n'.format(self._wine))
            io.write('\n')
        for key, value in env.iteritems():
            io.write('{}={}\n'.format(key, value))
            io.write('export {}\n'.format(key))
        script = io.getvalue()
        return script


class UncorkRC(WineRC):

    def get_rc(self):
        env = self.get_env()

        io = StringIO()

        if self._wine:
            io.write('W={}\n'.format(self._wine))
            io.write('\n')

        io.write('if type cork &> /dev/null; then\n')
        io.write('\tcork\n')
        io.write('fi\n')
        io.write('\n')
        for key, value in env.iteritems():
            io.write('_OLD_{}="${}"\n'.format(key, key))
            io.write('{}={}\n'.format(key, value))
            io.write('export {}\n'.format(key))

        io.write('BOTTLE="{}"\n'.format(self._bottle))
        io.write('export BOTTLE\n')
        io.write('\n')

        io.write('cork() {\n')
        io.write('\n')
        corker = os.path.join(self._prefix, 'bin', 'corkrc.sh')
        io.write('\t. "{}"\n'.format(corker))
        io.write('\n')

        io.write('\tif [ -n "$_OLD_WD" ]; then\n')
        io.write('\t\tcd "$_OLD_WD"\n')
        io.write('\tfi\n')
        io.write('\n')

        io.write('\tif [ -z "$WINE_ENV_DISABLE_PROMPT" ]; then\n')
        io.write('\t\tPS1="$_OLD_PS1"\n')
        io.write('\t\texport PS1\n')
        io.write('\t\tunset _OLD_PS1\n')
        io.write('\tfi\n')
        io.write('\n')

        io.write('\tif [ -z "$_OLD_WD" ]; then\n')
        io.write('\t\tunset WD\n')
        io.write('\telse\n')
        io.write('\t\tWD="$_OLD_WD"\n')
        io.write('\t\texport WD\n')
        io.write('\tfi\n')
        io.write('\tunset _OLD_WD\n')
        io.write('\n')

        io.write('\tunset W\n')
        io.write('\tunset BOTTLE\n')
        io.write('\tunset -f goc\n')
        io.write('\tunset -f cork\n')

        io.write('}\n')

        io.write('\n')
        io.write('if [ -z "$WINE_ENV_DISABLE_PROMPT" ]; then\n')
        io.write('\t_OLD_PS1="$PS1"\n')
        io.write('\tPS1="({})$PS1"\n'.format(self._bottle))
        io.write('fi\n')
        io.write('\n')
        io.write('_OLD_WD="$(pwd)"\n')
        io.write('cd "{}"\n'.format(self._prefix))
        io.write('\n')
        io.write('goc() {\n')
        io.write('\tcd "$WINEPREFIX/drive_c"\n')
        io.write('}\n')
        return io.getvalue()


class CorkRC(WineRC):

    def get_rc(self):
        env = self.get_env()

        io = StringIO()

        for key in env.keys():
            io.write('if [ -z "$_OLD_{}" ]; then\n'.format(key))
            io.write('\tunset {}\n'.format(key))
            io.write('else\n')
            io.write('\t{}="$_OLD_{}"\n'.format(key, key))
            io.write('\texport {}\n'.format(key))
            io.write('fi\n')
            io.write('unset _OLD_{}\n'.format(key))
            io.write('unset BOTTLE\n')
            io.write('\n')

        return io.getvalue()
