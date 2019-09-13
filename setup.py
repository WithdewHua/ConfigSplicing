# -*- coding:utf-8 -*-
#

from setuptools import setup

setup(
    name='ConfigSplicing',
    version='0.3',
    py_modules=['main', 'getnodes', 'getrules', 'functions', 'config'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        cs=main:main
    ''',
)

