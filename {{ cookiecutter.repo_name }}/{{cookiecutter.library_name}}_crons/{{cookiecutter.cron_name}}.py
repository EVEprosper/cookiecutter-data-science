"""launcher/wrapper for executing CLI"""
import logging
import os

from plumbum import cli

import prosper.common.prosper_cli as p_cli

from {{cookiecutter.library_name}} import _version, exceptions


HERE = os.path.abspath(path.dirname(__file__))
PROGNAME = '{{cookiecutter.cron_name}}'

class {{cookiecutter.cron_name}}CLI(p_cli.ProsperApplication):
    PROGNAME = PROGNAME
    VERSION = _version.__version__

    config_path = os.path.join(HERE, 'app.cfg')

    def main(self):
        """launcher logic"""
        self.logger.info('hello world')

def run_main():  # pragma: no cover
    """entry point for launching app"""
    {{cookiecutter.cron_name}}CLI.run()

if __name__ == '__main__':  # pragma: no cover
    run_main()
