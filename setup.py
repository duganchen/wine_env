from distutils.core import setup
import itertools
import os
import shutil

if not os.path.isdir('scripts'):
    os.makedirs('scripts')

raw_scripts = ('mkcorkrc.py', 'mkuncorkrc.py', 'mkrunrc.py', 'bottle-run.sh')
all_scripts = [
    os.path.join('scripts', os.path.splitext(script)[0]) for
    script in raw_scripts
]

for src, dst in itertools.izip(raw_scripts, all_scripts):
    shutil.copyfile(src, dst)

setup(
    name='wine_env',
    version='1.0',
    py_modules=['wine_rc'],
    scripts=all_scripts,
    data_files=[('bin', ['bottler.sh'])]
)
