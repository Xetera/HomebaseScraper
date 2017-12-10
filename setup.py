from setuptools import find_packages
from setuptools import setup

setup(
    name='HomebaseScraper',
    packages=find_packages(exclude=['tests*']),
)