import os
from setuptools import setup, Extension

module = Extension('MahjongGB', sources=[
    'mahjong.cpp',
    '../ChineseOfficialMahjongHelper/Classes/mahjong-algorithm/fan_calculator.cpp',
    '../ChineseOfficialMahjongHelper/Classes/mahjong-algorithm/shanten.cpp'
    ], language='c++', extra_compile_args = ["-std=c++11"])

setup(name='MahjongGB', ext_modules = [module])