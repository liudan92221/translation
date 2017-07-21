#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import dirname, join
from setuptools import setup
import json

with open(join(dirname(__file__), 'package.json'), 'rb') as f:
  pkg = json.loads(f.read())

setup(
  name=pkg['name'],
  version=pkg['version'],
  url='#',
  description=pkg['description'],
  long_description=open('README.md').read(),
  author=pkg['author']['name'],
  author_email=pkg['author']['email'],
  maintainer=pkg['author']['name'],
  maintainer_email=pkg['author']['email'],
  license=pkg['license'],
  packages=['Translation'],
  install_requires=['inquirer', 'blessings', 'readchar', 'selenium', 'MacFSEvents'],
  include_package_data=True,
  zip_safe=False,
  entry_points={
    'console_scripts': [
      'translate = Translation.bin:execute',
      'words = Translation.bin:makeWordList',
      'copy = Translation.bin:copyWords',
      'join = Translation.bin:joinWords'
    ]
  },
  classifiers=[
    'Framework :: Translation',
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3'
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Software Development :: Libraries :: Python Modules',
  ],
)
