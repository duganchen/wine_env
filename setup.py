import os
import stat
from setuptools import setup
from setuptools.command import install
import shutil

shutil.copyfile('bottle-run.sh', 'bottle-run')

class Installer(install.install):
    """ http://stackoverflow.com/a/25761434/240515 """
    def run(self):
        install.install.run(self)

        for filepath in self.get_outputs():
            _, ext = os.path.splitext(filepath)
            if ext in ('.fish', '.sh', '.zsh'):
                mode = stat.S_IWUSR | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH
                os.chmod(filepath, mode)
setup(
    name='wine_env',
    version='1.0',
    packages=['wine_env'],
    cmdclass={'install': Installer},
    entry_points={
        'console_scripts': [
            'bottle = wine_env.bottle:main',
        ]
    },
    scripts=(
        'bottle-run',
        'bottler.sh',
        'bottler.fish',
        'wine_env_complete.sh',
        'wine_env_complete.zsh'
    ),
)
