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

        self.__wine = wine_executable
        if self.__wine:
            self.__wine = os.path.expanduser(self.__wine)

    def get_env(self):

        environment = {'WINEPREFIX': self._prefix}

        if not self.__wine:
            return environment

        wine_install_dir = os.path.dirname(os.path.dirname(self.__wine))
        path = ':'.join([os.path.dirname(self.__wine), '$PATH'])
        wine_server = os.path.join(wine_install_dir, 'bin', 'wineserver')
        wine_loader = os.path.join(wine_install_dir, 'bin', 'wine')
        wine_dll_path = os.path.join(
            wine_install_dir, 'lib', 'wine', 'fakedlls')
        ld_library_path = ':'.join(
            [os.path.join(wine_install_dir, 'lib'), '$LD_LIBRARY_PATH']
        )

        environment['WINESERVERPATH'] = wine_install_dir
        environment['PATH'] = path
        environment['WINESERVER'] = wine_server
        environment['WINELOADER'] = wine_loader
        environment['WINEDLLPATH'] = wine_dll_path
        environment['LD_LIBRARY_PATH'] = ld_library_path
        environment['WINEPREFIX'] = self._prefix

        return environment


class RunRC(WineRC):

    def get_rc(self):
        env = self.get_env()
        io = StringIO()
        for key, value in env.iteritems():
            io.write('export {0}={1}\n'.format(key, value))
        script = io.getvalue()
        return script


class UncorkRC(WineRC):

    def get_rc(self):
        env = self.get_env()

        io = StringIO()

        io.write('declare -f cork > /dev/null\n')
        io.write('if [ $? = 0 ]; then\n')
        io.write('\tcork\n')
        io.write('fi\n')
        io.write('\n')
        for key, value in env.iteritems():
            io.write('_OLD_{0}="${0}"\n'.format(key))
            io.write('export {0}="{1}"\n'.format(key, value))

        io.write('\n')

        io.write('function cork {\n')
        io.write('\n')
        uncorker = os.path.join(self._prefix, 'bin', 'corkrc')
        io.write('\t. {0}\n'.format(uncorker))
        io.write('\n')

        io.write('\tPS1="$_OLD_PS1"\n')
        io.write('\tunset _OLD_PS1\n')
        io.write('\n')
        io.write('\tcd $_OLD_WD\n')
        io.write('\tunset _OLD_WD\n')

        io.write('}\n')

        io.write('\n')
        io.write('_OLD_PS1="$PS1"\n')
        io.write('PS1="({0})$PS1"\n'.format(self._bottle))
        io.write('_OLD_WD=$(pwd)\n')
        io.write('cd {0}\n'.format(self._prefix))
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
