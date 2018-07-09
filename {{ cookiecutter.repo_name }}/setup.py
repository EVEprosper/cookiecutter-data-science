"""wheel setup for Prosper common utilities"""
import codecs
import importlib
import os

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

HERE = os.path.abspath(os.path.dirname(__file__))


__package_name__ = '{{cookiecutter.repo_name}}'
__library_name__ = '{{cookiecutter.library_name}}'
__cron_name__ = __library_name__ + '_crons'


def get_version(package_name):
    """find __version__ for making package

    Args:
        package_name (str): path to _version.py folder (abspath > relpath)

    Returns:
        str: __version__ value

    """
    module = package_name + '._version'
    package = importlib.import_module(module)

    version = package.__version__

    return version


class PyTest(TestCommand):
    """PyTest cmdclass hook for test-at-buildtime functionality

    http://doc.pytest.org/en/latest/goodpractices.html#manual-integration

    """
    user_options = [
        ('pytest-args=', 'a', 'Arguments to pass to pytest'),
        ('secret-cfg=', None, 'Secret credentials.ini file to apply to app.cfg'),
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.secret_cfg = None
        self.pytest_args = [
            'tests',
            '-rx',
            '--cov=' + __library_name__,
            '--cov=' + __cron_name__,
            '--cov-report=term-missing',
            '--cov-config=.coveragerc',
        ]

    def run_tests(self):
        import shlex
        import pytest
        pytest_commands = []
        if self.secret_cfg:
            pytest_commands.append('--secret-cfg=' + self.secret_cfg)
        try:
            pytest_commands.extend(shlex.split(self.pytest_args))
        except AttributeError:
            pytest_commands = self.pytest_args
        errno = pytest.main(pytest_commands)
        exit(errno)

class TravisTest(PyTest):
    """wrapper for quick-testing for devs"""
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.secret_cfg = None
        self.pytest_args = [
            'tests',
            '-rx',
            '--junitxml=junit.xml',
            '--cov=' + __library_name__,
            '--cov=' + __cron_name__,
            '--cov-report=term-missing',
            '--cov-config=.coveragerc',
        ]

with codecs.open('README.rst', 'r', 'utf-8') as readme_fh:
    README = readme_fh.read()

setup(
    name=__package_name__,
    version=get_version(__library_name__),
    description='{{ cookiecutter.description }}',
    author='{{ cookiecutter.author_name }}',
    license='{% if cookiecutter.open_source_license == 'MIT' %}MIT{% elif cookiecutter.open_source_license == 'BSD-3-Clause' %}BSD-3{% endif %}',
    packages=find_packages(),
    python_requires='>=3.6',
    include_package_data=True,
    package_data={
        '': ['LICENSE', 'README.rst'],
        __library_name__: ['version.txt'],
        __cron_name__: ['app.cfg'],
    },
    entry_points={
        'console_scripts': [
            '{{cookiecutter.cron_name}}={}.{{cookiecutter.cron_name}}:run_main'.format(__cron_name__),
        ],
    },
    install_requires=[
        'pandas',
        'ProsperCommon',
        'ProsperDatareader',
        'plumbum',
        'requests',
    ],
    tests_require=[
        'pytest',
        'pytest_cov',
    ],
    extras_require={
        'dev':[
            'awscli',
            'jupyter',
            'sphinx',
            'sphinxcontrib-napoleon',
            'semantic-version',
        ]
    },
    cmdclass={
        'test':PyTest,
        'travis': TravisTest,
    },
)
