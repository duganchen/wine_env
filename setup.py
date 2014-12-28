from setuptools import setup, find_packages

setup(
    name='wine_env',
    version='1.0',
    packages=find_packages(),
    scripts=(
        'mkcorkrc.py',
        'mkuncorkrc.py',
        'mkrunrc.py',
        'bottle-run.sh',
        'bottler.sh',
        'wine_env_complete.sh'
    )
)
