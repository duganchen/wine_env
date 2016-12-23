from io import StringIO
import os


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
            string_io.write(f'W={self._wine}\n')
            string_io.write('\n')
        for key in sorted(env.keys()):
            string_io.write(f'{key}={env[key]}\n')
            string_io.write(f'export {key}\n')
        script = string_io.getvalue()
        return script


class UncorkRC(WineRC):

    def get_rc(self):
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
        corker = os.path.join(self._prefix, 'bin', 'corkrc.sh')
        string_io.write(f'\t. "{corker}"\n')
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


class CorkRC(WineRC):

    def get_rc(self):

        string_io = StringIO()

        for key in self.get_all_keys():
            string_io.write('if [ -n "_OLD_{}" ]; then\n')
            string_io.write(f'\t{key}="$_OLD_{key}"\n')
            string_io.write(f'\texport {key}\n')
            string_io.write(f'\tunset _OLD_{key}\n')
            if key != 'PATH':
                string_io.write('else\n')
                string_io.write(f'\tunset {key}\n')
            string_io.write('fi\n')
            string_io.write('\n')

        return string_io.getvalue()


class RunRCFish(WineRCFish):

    def get_rc(self):
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

    def get_rc(self):

        string_io = StringIO()

        if self._wine:
            string_io.write(f'set W {self._wine}\n')
            string_io.write('\n')

        string_io.write('if functions -q cork\n')
        string_io.write('\tcork\n')
        string_io.write('end\n')
        string_io.write('\n')
        string_io.write('function cork\n')
        corker = os.path.join(self._prefix, 'bin', 'corkrc.fish')
        string_io.write(f'\tsource {corker}\n')
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
            string_io.write(f'if test -n "${key}"\n')
            string_io.write(f'\tif not set -q _OLD_{key}\n')
            string_io.write(f'\t\tset -gx _OLD_{key} ${key}\t\n')
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


class CorkRCFish(WineRCFish):

    def get_rc(self):
        string_io = StringIO()

        for key in self.get_all_keys():
            string_io.write(f'if set -q _OLD_{key}\n')
            string_io.write(f'\tset -gx {key} $_OLD_{key}\n')
            string_io.write(f'\tset -e _OLD_{key}\n')
            if key != 'PATH':
                string_io.write('else\n')
                string_io.write(f'\tset -e {key}\n')
            string_io.write('end\n')
            string_io.write('\n')

        return string_io.getvalue()
