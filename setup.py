from setuptools import setup
import shutil

shutil.copyfile('bottle-run.sh', 'bottle-run')

setup(
    name='wine_env',
    version='1.0',
    packages=['wine_env'],
    entry_points={
        'console_scripts': [
            'mkcorkrc = wine_env.mkcorkrc:main',
            'mkuncorkrc = wine_env.mkuncorkrc:main',
            'mkrunrc = wine_env.mkrunrc:main'
        ]
    },
    scripts=('bottle-run',),
    data_files=[
        ('/usr/bin', ['bottler.sh', 'wine_env_complete.sh'])]
)
