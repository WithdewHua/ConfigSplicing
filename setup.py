# -*- coding:utf-8 -*-
#

from setuptools import setup

setup(
    name='ConfigSplicing',
    version='0.2',
    py_modules=['main', 'nodes', 'rules', 'functions'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        cs=main:main
    ''',
)

