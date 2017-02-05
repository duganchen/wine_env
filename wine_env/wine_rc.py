from io import StringIO
import os
from typing import List


class WineRCBase(object):

    wine_server = os.path.join('$W', 'bin', 'wineserver')
    wine_loader = os.path.join('$W', 'bin', 'wine')
    wine_dll_path = os.path.join('$W', 'lib', 'wine', 'fakedlls')

    def __init__(self, bottle: str, wine_executable=None):

        self._prefix = os.path.join(
            '$HOME', '.local', 'share', 'wineprefixes', bottle
        )

        self._bottle = bottle

        self._wine = wine_executable
        if self._wine:
            self._wine = os.path.dirname(
                os.path.dirname(os.path.expanduser(self._wine))
            )

    def get_all_keys(self) -> List[str]:

        return ['WINEVERPATH', 'PATH', 'WINESERVER', 'WINELOADER', 'WINEDLLPATH', 'LD_LIBRARY_PATH', 'WINEPREFIX']

    def get_env(self) -> dict:

        environment = {'WINEPREFIX': self._prefix}

        if not self._wine:
            return environment

        environment.update(self._get_exe_env())
        return environment

    def _get_exe_env(self):
        raise NotImplementedError


class WineRC(WineRCBase):

    path = ':'.join([os.path.join('$W', 'bin'), '$PATH'])
    ld_library_path = ':'.join([os.path.join('$W', 'lib'), '$LD_LIBRARY_PATH'])

    def _get_exe_env(self) -> dict:
        return {
            'WINEVERPATH': '"$W"',
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

    def _get_exe_env(self) -> dict:

        return {
            'WINEVERPATH': '$W',
            'PATH': self.path,
            'WINESERVER': self.wine_server,
            'WINELOADER': self.wine_loader,
            'WINEDLLPATH': self.wine_dll_path,
            'LD_LIBRARY_PATH': self.ld_library_path,
            'WINEPREFIX': self._prefix
        }

class RunRC(WineRC):

    def get_rc(self) -> str:
        env = self.get_env()
        string_io = StringIO()
        if self._wine:
            string_io.write(f'W={self._wine}\n')
            string_io.write('\n')
        for key in sorted(env.keys()):
            string_io.write(f'{key}={env[key]}\n')
            string_io.write(f'export {key}\n')
        script = string_io.getvalue()
        return script


class UncorkRC(WineRC):

    def get_rc(self) -> str:
        env = self.get_env()

        string_io = StringIO()

        if self._wine:
            string_io.write(f'W={self._wine}\n')
            string_io.write('\n')

        string_io.write('if type cork &> /dev/null; then\n')
        string_io.write('\tcork\n')
        string_io.write('fi\n')
        string_io.write('\n')

        string_io.write('cork() {\n')
        string_io.write('\n')

        for key in self.get_all_keys():
            string_io.write(f'\tif [ -n "_OLD_{key}" ]; then\n')
            string_io.write(f'\t\t{key}="$_OLD_{key}"\n')
            string_io.write(f'\t\texport {key}\n')
            string_io.write(f'\t\tunset _OLD_{key}\n')
            if key != 'PATH':
                string_io.write('\telse\n')
                string_io.write(f'\t\tunset {key}\n')
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
            string_io.write(f'if [ -n "${key}" ]; then\n')
            string_io.write(f'\tif [ -z "$_OLD_{key}" ]; then\n')
            string_io.write(f'\t\t_OLD_{key}="${key}"\n')
            string_io.write(f'\t\texport _OLD_{key}\n')
            string_io.write('\tfi\n')
            string_io.write('fi\n')

            if key in env:
                string_io.write(f'{key}={env[key]}\n')
                string_io.write(f'export {key}\n')

            string_io.write('\n')

        string_io.write(f'BOTTLE="{self._bottle}"\n')
        string_io.write('export BOTTLE\n')
        string_io.write('\n')
        string_io.write('if [ -z "$WINE_ENV_DISABLE_PROMPT" ]; then\n')
        string_io.write('\t_OLD_PS1="$PS1"\n')
        string_io.write(f'\tPS1="({self._bottle})$PS1"\n')
        string_io.write('fi\n')
        string_io.write('\n')
        string_io.write('_OLD_WD="$(pwd)"\n')
        string_io.write(f'cd "{self._prefix}"\n')
        string_io.write('\n')
        string_io.write('goc() {\n')
        string_io.write('\tcd "$WINEPREFIX/drive_c"\n')
        string_io.write('}\n')
        return string_io.getvalue()


class RunRCFish(WineRCFish):

    def get_rc(self) -> str:
        env = self.get_env()
        string_io = StringIO()
        if self._wine:
            string_io.write(f'set W {self._wine}\n')
            string_io.write('\n')
        for key in sorted(env.keys()):
            string_io.write(f'set -gx {key} {env[key]}\n')
        script = string_io.getvalue()
        return script


class UncorkRCFish(WineRCFish):

    def get_rc(self) -> str:

        string_io = StringIO()

        string_io.write('if functions -q cork\n')
        string_io.write('\tcork\n')
        string_io.write('end\n')
        string_io.write('\n')
        string_io.write('function cork\n')
        string_io.write('\n')

        for key in self.get_all_keys():
            string_io.write(f'\tif set -q _OLD_{key}\n')
            string_io.write(f'\t\tset -gx {key} $_OLD_{key}\n')
            string_io.write(f'\t\tset -e _OLD_{key}\n')
            if key != 'PATH':
                string_io.write('\telse\n')
                string_io.write(f'\t\tset -e {key}\n')
            string_io.write('\tend\n')
            string_io.write('\n')

        string_io.write('\tif set -q W\n')
        string_io.write('\t\tset -e W\n')
        string_io.write('\tend\n')
        string_io.write('\n')
        string_io.write('\tif set -q BOTTLE\n')
        string_io.write('\t\tset -e BOTTLE\n')
        string_io.write('\tend\n')
        string_io.write('\n')
        string_io.write('\tif set -q _OLD_PWD\n')
        string_io.write('\t\tcd "$_OLD_PWD"\n')
        string_io.write('\t\tset -e _OLD_PWD\n')
        string_io.write('\tend\n')
        string_io.write('\n')
        string_io.write('\tfunctions -e goc\n')
        string_io.write('\tfunctions -e cork\n')
        string_io.write('end\n')
        string_io.write('\n')

        env = self.get_env()

        if self._wine:
            string_io.write(f'set W {self._wine}\n')
            string_io.write('\n')

        for key in self.get_all_keys():
            string_io.write(f'if test -n "${key}"\n')
            string_io.write(f'\tif not set -q _OLD_{key}\n')
            string_io.write(f'\t\tset -gx _OLD_{key} ${key}\n')
            string_io.write('\tend\n')
            string_io.write('end\n')

            if key in env:
                string_io.write(f'set -gx {key} {env[key]}\n')

        string_io.write('\n')

        string_io.write('set -gx _OLD_PWD $PWD\n')
        string_io.write(f'cd {self._prefix}\n')
        string_io.write('\n')
        string_io.write('function goc\n')
        string_io.write('\tcd $WINEPREFIX/drive_c\n')
        string_io.write('end\n')
        return string_io.getvalue()
