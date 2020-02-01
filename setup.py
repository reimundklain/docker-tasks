#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="docker-tasks",
    version="0.0.8",
    author="Reimund Klain",
    author_email="reimund.klain@condevtec.de",
    url="https://github.com/daymien/docker-tasks",
    license="BSD",
    description="Utilze docker exec to run commands on yaml base config",
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    keywords=["docker", "tasks", "cron", "command-line", "CLI"],
    packages=find_packages(),
    scripts=[],
    entry_points={"console_scripts": ["docker-tasks = docker_tasks:main"]},
    install_requires=["docker", "pyaml"],
    zip_safe=False,
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    platforms="any",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)
