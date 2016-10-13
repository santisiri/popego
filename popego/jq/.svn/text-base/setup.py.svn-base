#!/usr/bin/python

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='jq',
    version='0.1',
    description='Simple JobQueue',
    author='Mariano Cortesi',
    author_email='mcortesi@gmail.com',
    license='Apache 2.0',
#    url='http://code.google.com/p/gdata-python-client/',
    install_requires= [
      "docutils==0.4",
      "SQLAlchemy==0.4.3",
      "Elixir==0.5.1",
      "zope.interface"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
#    package_dir = {'':'src/gdata', 'atom':'src/atom'}
)
