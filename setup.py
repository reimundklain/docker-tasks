#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='docker-tasks',
    version='0.0.1-0',
    author='Reimund Klain',
    author_email='reimund.klain@condevtec.de',

    url='https://github.com/daymien/docker-tasks',
    license='BSD',
    description='',
    long_description=__doc__,
    keywords=['docker', 'cron', 'command-line', 'CLI'],

    packages=find_packages(),
    scripts=[],
    entry_points={
        'console_scripts': [
            'docker-tasks = docker_backup:main',
        ]
    },

    install_requires=[
        'docker-py',
        'requests'
    ],
    #extras_require={
    #    'yaml': ['pyyaml',]
    #},
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',

    platforms='any',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        #'Programming Language :: Python :: 3',
    ],
)