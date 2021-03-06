#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'pandas',
    'scipy'
 ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Pierre Monferrand",
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience ::  Healthcare Industry',
        'Intended Audience ::  Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Basic hypothesis testing made simple",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='medstat',
    name='medstat',
    packages=find_packages(include=['medstat', 'medstat.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/monferrand/medstat',
    version='1.0.1',
    zip_safe=False,
)
