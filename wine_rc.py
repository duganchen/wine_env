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

        path = '"{0}"'.format(':'.join([os.path.join('$W', 'bin'), '$PATH']))
        wine_server = '"{0}"'.format(os.path.join('$W', 'bin', 'wineserver'))
        wine_loader = '"{0}"'.format(os.path.join('$W', 'bin', 'wine'))
        wine_dll_path = '"{0}"'.format(
            os.path.join('$W', 'lib', 'wine', 'fakedlls')
        )
        ld_library_path = '"{0}"'.format(
            ':'.join([os.path.join('$W', 'lib'), '$LD_LIBRARY_PATH'])
        )

        environment['WINESERVERPATH'] = '"{0}"'.format('$W')
        environment['PATH'] = path
        environment['WINESERVER'] = wine_server
        environment['WINELOADER'] = wine_loader
        environment['WINEDLLPATH'] = wine_dll_path
        environment['LD_LIBRARY_PATH'] = ld_library_path
        environment['WINEPREFIX'] = '"{0}"'.format(self._prefix)

        return environment


class RunRC(WineRC):

    def get_rc(self):
        env = self.get_env()
        io = StringIO()
        if self._wine:
            io.write('W={}\n'.format(self._wine))
            io.write('\n')
        for key, value in env.iteritems():
            io.write('export {0}={1}\n'.format(key, value))
        script = io.getvalue()
        return script


class UncorkRC(WineRC):

    def get_rc(self):
        env = self.get_env()

        io = StringIO()

        if self._wine:
            io.write('W={}\n'.format(self._wine))
            io.write('\n')

        io.write('declare -f cork > /dev/null\n')
        io.write('if [ $? = 0 ]; then\n')
        io.write('\tcork\n')
        io.write('fi\n')
        io.write('\n')
        for key, value in env.iteritems():
            io.write('_OLD_{0}="${0}"\n'.format(key))
            io.write('export {0}={1}\n'.format(key, value))

        io.write('\n')

        io.write('cork() {\n')
        io.write('\n')
        corker = os.path.join(self._prefix, 'bin', 'corkrc')
        io.write('\t. {0}\n'.format(corker))
        io.write('\n')

        for key in ('PS1', 'WD'):
            io.write('\tif [ "$_OLD_{0}" = "" ]; then\n'.format(key))
            io.write('\t\tunset {0}\n'.format(key))
            io.write('\telse\n')
            io.write('\t\texport {0}="$_OLD_{1}"\n'.format(key, key))
            io.write('\tfi\n')
            io.write('\tunset _OLD_{0}\n'.format(key))
            io.write('\n')

        io.write('\tunset -f cork\n')
        io.write('\tunset W\n')
        io.write('\tunset -f goc\n')

        io.write('}\n')

        io.write('\n')
        io.write('_OLD_PS1="$PS1"\n')
        io.write('PS1="({0})$PS1"\n'.format(self._bottle))
        io.write('_OLD_WD=$(pwd)\n')
        io.write('cd {0}\n'.format(self._prefix))
        io.write('\n')
        io.write('goc() {\n')
        io.write('\tcd $WINEPREFIX/drive_c\n')
        io.write('}\n')
        return io.getvalue()


class CorkRC(WineRC):

    def get_rc(self):
        env = self.get_env()

        io = StringIO()

        for key in env.keys():
            io.write('if [ "$_OLD_{0}" = "" ]; then\n'.format(key))
            io.write('\tunset {0}\n'.format(key))
            io.write('else\n')
            io.write('\texport {0}="$_OLD_{1}"\n'.format(key, key))
            io.write('fi\n')
            io.write('unset _OLD_{0}\n'.format(key))
            io.write('\n')

        return io.getvalue()
