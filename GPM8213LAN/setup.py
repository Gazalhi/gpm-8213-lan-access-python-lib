# -*- coding: utf-8 -*-
"""
setup GPM-8213-LAN

@author: Hugo_MILAN
"""

from setuptools import find_packages,setup

setup(
      name='GPM8213LAN',
      version='0.1.0',
      author='Milan Hugo',
      author_email='hugo.milan@ens-paris-saclay.fr',
      description='GPM-8213 LAN Access on python',
      license='GPL',
      keywords='lib',
      packages=find_packages(include=['GPM8213LAN']),
      install_requires=[],
      setup_requires=['pytest-runner'],
      tests_require=['pytest==4.4.1'],
      test_suite='tests',
      )