# coding=utf-8
"""Import all *.py files in this folder.
"""
import os


for module in os.listdir(os.path.dirname(__file__)):
    if module.startswith('_') or module[-3:] != '.py':
        continue
    __import__(module[:-3], locals(), globals())
del module
