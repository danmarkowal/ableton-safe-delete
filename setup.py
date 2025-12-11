from setuptools import setup, find_packages

setup(
    name='alsafedel',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'alsafedel=alsafedel.main:main',
        ],
    },
)
