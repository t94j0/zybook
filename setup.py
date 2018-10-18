#!/usr/bin/env python

from distutils.core import setup

setup(name='zybook',
      version='1.0',
      description='Solves ZyBooks Answers',
      author='Max Harley',
      author_email='maxh@maxh.io',
      url='http://github.com/t94j0/zybook',
      license='wtfpl',
      scripts=['zybook'],
      install_requires=['parse','argparse','requests'],
      python_requires='>=3'
     )
