# -*- coding: utf-8 -*-
"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mi3_battery_block` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``i3_battery_block.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``i3_battery_block.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import argparse
import logging
import os.path
from typing import IO


class CLI:
    """The command line interface"""

    def __init__(self):
        parser = argparse.ArgumentParser(description='CLI for i3 wm block battery',
                                         epilog='volker.goehler@informatik.tu-freiberg.de'
                                         )
        parser.add_argument('-c', '--compact', action='store_true' help="flag for compact mode, truncates all batteries into one") #TODO implement this
        parser.add_argument('-l', '--loglevel', help="log level", choices=["debug", "info", "warning", "error", "critical"],
                              type=str,
                              default="warning")


    def parse(self, args : list):
        self.args = parser.parse_args(args=args)

    @property
    def get_log_level(self) -> int:
        """ parses the input loglevel to the numeric value """
        return getattr(logging, self.args.logging.upper(), None)

    @property
    def is_compact(self) -> bool:
        return getattr(Compact, self.args.compact), None)


def main(args=None):
    cli = CLI()
    cli.parse(args=args)

    logging.basicConfig(level=cli.get_log_level)

    # TODO output logic here
    print(cli.args.names)

