from setuptools import setup, find_packages
import os

version = '0.1'

long_description = (
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='gw20e.linkchecker',
      version=version,
      description="A simple linkchecker based on scrapy",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Goldmund, Wyldebeast & Wunderliebe',
      author_email='info@gw20e.com',
      url='http://www.gw20e.com/',
      license='gpl',
      namespace_packages=['gw20e'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'scrapy',
      ],
      entry_points={'scrapy': ['settings = gw20e.linkchecker.settings']},
      )
