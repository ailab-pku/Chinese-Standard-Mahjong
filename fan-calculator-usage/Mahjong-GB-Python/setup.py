import os
from setuptools import setup, Extension

module = Extension('MahjongGB', sources=[
    'mahjong.cpp',
    ], language='c++')

setup(name='MahjongGB', ext_modules = [module])