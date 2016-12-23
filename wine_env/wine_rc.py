#!/usr/bin/env mpcpython

from __future__ import (
    division, absolute_import, print_function, unicode_literals
)

import argparse
from io import StringIO
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
                print('Wine must be the path to an executable')
                sys.exit(1)

        wine_rc = self.__rc_cls(args.bottle, args.wine)

        print(wine_rc.get_rc())


class WineRCBase(object):

    wine_server = os.path.join('$W', 'bin', 'wineserver')
    wine_loader = os.path.join('$W', 'bin', 'wine')
    wine_dll_path = os.path.join('$W', 'lib', 'wine', 'fakedlls')

    def get_all_keys(self):

        keys = ['WINESERVERPATH', 'PATH', 'WINESERVER', 'WINELOADER', 'WINEDLLPATH', 'LD_LIBRARY_PATH', 'WINEPREFIX']
        if self._win32:
            keys.append('WINEARCH')
        return keys

    def __init__(self, bottle, wine_executable=None, win32=False):

        self._prefix = os.path.join(
            '$HOME', '.local', 'share', 'wineprefixes', bottle
        )

        self._bottle = bottle

        self._wine = wine_executable
        if self._wine:
            self._wine = os.path.dirname(
                os.path.dirname(os.path.expanduser(self._wine))
            )

        self._win32 = win32

    def get_env(self):

        environment = {'WINEPREFIX': self._prefix}

        if self._win32:
            environment['WINEARCH'] = 'win32'

        if not self._wine:
            return environment

        environment.update(self._get_exe_env())
        return environment

    def _get_exe_env(self):
        raise NotImplementedError


class WineRC(WineRCBase):

    path = ':'.join([os.path.join('$W', 'bin'), '$PATH'])
    ld_library_path = ':'.join([os.path.join('$W', 'lib'), '$LD_LIBRARY_PATH'])

    def _get_exe_env(self):
        return {
            'WINESERVERPATH': '"$W"',
            'PATH': f'"{self.path}"',
            'WINESERVER': f'"{self.wine_server}"',
            'WINELOADER': f'"{self.wine_loader}"',
            'WINEDLLPATH': f'"{self.wine_dll_path}"',
            'LD_LIBRARY_PATH': f'"{self.ld_library_path}"',
            'WINEPREFIX': f'"{self._prefix}"'
        }


class WineRCFish(WineRCBase):

    path = ' '.join([os.path.join('$W', 'bin'), '$PATH'])
    ld_library_path = ' '.join([os.path.join('$W', 'lib'), '$LD_LIBRARY_PATH'])


    def _get_exe_env(self):

        return {
            'WINESERVERPATH': '$W',
            'PATH': self.path,
            'WINESERVER': self.wine_server,
            'WINELOADER': self.wine_loader,
            'WINEDLLPATH': self.wine_dll_path,
            'LD_LIBRARY_PATH': self.ld_library_path,
            'WINEPREFIX': self._prefix
        }

class RunRC(WineRC):

    def get_rc(self):
        env = self.get_env()
        string_io = StringIO()
        if self._wine:
            string_io.write('W={}\n'.format(self._wine))
            string_io.write('\n')
        for key in sorted(env.keys()):
            string_io.write('{}={}\n'.format(key, env[key]))
            string_io.write('export {}\n'.format(key))
        script = string_io.getvalue()
        return script


class UncorkRC(WineRC):

    def get_rc(self):
        env = self.get_env()

        string_io = StringIO()

        if self._wine:
            string_io.write('W={}\n'.format(self._wine))
            string_io.write('\n')

        string_io.write('if type cork &> /dev/null; then\n')
        string_io.write('\tcork\n')
        string_io.write('fi\n')
        string_io.write('\n')

        string_io.write('cork() {\n')
        string_io.write('\n')
        corker = os.path.join(self._prefix, 'bin', 'corkrc.sh')
        string_io.write('\t. "{}"\n'.format(corker))
        string_io.write('\n')

        string_io.write('\tif [ -n "$_OLD_WD" ]; then\n')
        string_io.write('\t\tcd "$_OLD_WD"\n')
        string_io.write('\tfi\n')
        string_io.write('\n')

        string_io.write('\tif [ -z "$WINE_ENV_DISABLE_PROMPT" ]; then\n')
        string_io.write('\t\tPS1="$_OLD_PS1"\n')
        string_io.write('\t\texport PS1\n')
        string_io.write('\t\tunset _OLD_PS1\n')
        string_io.write('\tfi\n')
        string_io.write('\n')

        string_io.write('\tif [ -z "$_OLD_WD" ]; then\n')
        string_io.write('\t\tcd $_OLD_WD\n')
        string_io.write('\t\tunset _OLD_WD\n')
        string_io.write('\tfi\n')
        string_io.write('\n')

        string_io.write('\tunset W\n')
        string_io.write('\tunset BOTTLE\n')
        string_io.write('\tunset -f goc\n')
        string_io.write('\tunset -f cork\n')

        string_io.write('}\n')
        string_io.write('\n')

        env = self.get_env()
        for key in self.get_all_keys():
            string_io.write('if [ -n "${}" ]; then\n'.format(key))
            string_io.write('\tif [ -z "$_OLD_{}" ]; then\n'.format(key))
            string_io.write('\t\t_OLD_{}="${}"\n'.format(key, key))
            string_io.write('\t\texport _OLD_{}\n'.format(key))
            string_io.write('\tfi\n')
            string_io.write('fi\n')

            if key in env:
                string_io.write('{}={}\n'.format(key, env[key]))
                string_io.write('export {}\n'.format(key))

            string_io.write('\n')

        string_io.write('BOTTLE="{}"\n'.format(self._bottle))
        string_io.write('export BOTTLE\n')
        string_io.write('\n')
        string_io.write('if [ -z "$WINE_ENV_DISABLE_PROMPT" ]; then\n')
        string_io.write('\t_OLD_PS1="$PS1"\n')
        string_io.write('\tPS1="({})$PS1"\n'.format(self._bottle))
        string_io.write('fi\n')
        string_io.write('\n')
        string_io.write('_OLD_WD="$(pwd)"\n')
        string_io.write('cd "{}"\n'.format(self._prefix))
        string_io.write('\n')
        string_io.write('goc() {\n')
        string_io.write('\tcd "$WINEPREFIX/drive_c"\n')
        string_io.write('}\n')
        return string_io.getvalue()


class CorkRC(WineRC):

    def get_rc(self):

        string_io = StringIO()

        for key in self.get_all_keys():
            string_io.write('if [ -n "_OLD_{}" ]; then\n')
            string_io.write('\t{}="$_OLD_{}"\n'.format(key, key))
            string_io.write('\texport {}\n'.format(key))
            string_io.write('\tunset _OLD_{}\n'.format(key))
            if key != 'PATH':
                string_io.write('else\n')
                string_io.write('\tunset {}\n'.format(key))
            string_io.write('fi\n')
            string_io.write('\n')

        return string_io.getvalue()


class RunRCFish(WineRCFish):

    def get_rc(self):
        env = self.get_env()
        string_io = StringIO()
        if self._wine:
            string_io.write('set W {}\n'.format(self._wine))
            string_io.write('\n')
        for key in sorted(env.keys()):
            string_io.write('set -gx {} {}\n'.format(key, env[key]))
        script = string_io.getvalue()
        return script


class UncorkRCFish(WineRCFish):

    def get_rc(self):

        string_io = StringIO()

        if self._wine:
            string_io.write('set W {}\n'.format(self._wine))
            string_io.write('\n')

        string_io.write('if functions -q cork\n')
        string_io.write('\tcork\n')
        string_io.write('end\n')
        string_io.write('\n')
        string_io.write('function cork\n')
        corker = os.path.join(self._prefix, 'bin', 'corkrc.fish')
        string_io.write('\tsource {}\n'.format(corker))
        string_io.write('\tcd "$_OLD_PWD"\n')
        string_io.write('\t\tset -e _OLD_PWD\n')
        string_io.write('\tif set -q W')
        string_io.write('\t\tset -e W\n')
        string_io.write('\tend\n')
        string_io.write('\tif set -q BOTTLE\n')
        string_io.write('\t\tset -e BOTTLE\n')
        string_io.write('\tend\n')
        string_io.write('\tfunctions -e goc\n')
        string_io.write('\tfunctions -e cork\n')
        string_io.write('end\n')
        string_io.write('\n')

        env = self.get_env()

        for key in self.get_all_keys():
            string_io.write('if test -n "${}"\n'.format(key))
            string_io.write('\tif not set -q _OLD_{}\n'.format(key))
            string_io.write('\t\tset -gx _OLD_{} ${}\t\n'.format(key, key))
            string_io.write('\tend\n')
            string_io.write('end\n')

            if key in env:
                string_io.write('set -gx {} {}\n'.format(key, env[key]))

        string_io.write('\n')

        string_io.write('set -gx _OLD_PWD $PWD\n')
        string_io.write('cd {}\n'.format(self._prefix))
        string_io.write('\n')
        string_io.write('function goc\n')
        string_io.write('\tcd $WINEPREFIX/drive_c\n')
        string_io.write('end\n')
        return string_io.getvalue()


class CorkRCFish(WineRCFish):

    def get_rc(self):
        string_io = StringIO()

        for key in self.get_all_keys():
            string_io.write('if set -q _OLD_{}\n'.format(key))
            string_io.write('\tset -gx {} $_OLD_{}\n'.format(key, key))
            string_io.write('\tset -e _OLD_{}\n'.format(key))
            if key != 'PATH':
                string_io.write('else\n')
                string_io.write('\tset -e {}\n'.format(key))
            string_io.write('end\n')
            string_io.write('\n')

        return string_io.getvalue()
