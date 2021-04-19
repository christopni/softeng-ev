from setuptools import setup

setup(
    name='SoftengCli',
    version='1.0',
    py_modules=['ev_group50'],
    install_requires=[
            'Click', 'Requests', 'colorama',
    ],
    entry_points={
            'console_scripts': ['ev_group50=ev_group50:cli']
    },
)
