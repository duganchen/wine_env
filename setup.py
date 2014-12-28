from setuptools import setup

setup(
    name='wine_env',
    version='1.0',
    packages=['wine_env'],
    entry_points={
        'console_scripts': [
            'mkcorkrc = wine_env.mkcorkrc.main',
            'mkuncorkrc = wine_env.mkuncorkrc.main',
            'mkrunrc = wine_env.mkrunrc.main'
        ]
    },
    scripts=(
        'bottle-run.sh',
        'bottler.sh',
        'wine_env_complete.sh'
    )
)
