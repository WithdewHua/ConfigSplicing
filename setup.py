# -*- coding:utf-8 -*-
#

from setuptools import setup

setup(
    name='ConfigSplicing',
    version='0.4',
    py_modules=['main', 'getnodes', 'getrules', 'functions', 'config', 'proxygroup'],
    install_requires=[
        'Click',
        'ruamel.yaml'
    ],
    entry_points='''
        [console_scripts]
        cs=main:main
    ''',
)

