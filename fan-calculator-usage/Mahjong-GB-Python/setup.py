import os
from setuptools import setup, Extension

module = Extension('MahjongGB', sources=[
    'mahjong.cpp',
    ], language='c++', extra_compile_args = ["-std=c++11"])

setup(name='MahjongGB', ext_modules = [module])
