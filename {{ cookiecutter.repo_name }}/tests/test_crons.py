"""test GetNews cli"""
import copy
import os

import helpers
from plumbum import local
import pytest

import {{cookiecutter.library_name}}_crons
from {{cookiecutter.library_name}}._version import __version__
class Test{{cookiecutter.cron_name}}:
    """validates GetNews cron"""
    cli = local['{{cookiecutter.cron_name}}']
    dummy_app = {{cookiecutter.library_name}}_crons.{{cookiecutter.cron_name}}.{{cookiecutter.cron_name}}CLI(__file__)

    def test_help(self):
        """validate -h works"""
        result = self.cli('-h')

        result = self.cli('--version')
        assert result.strip() == '{progname} {version}'.format(
            progname={{cookiecutter.library_name}}_crons.PROGNAME,
            version=__version__,
        )

