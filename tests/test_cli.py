import logging

import pytest

from i3_battery_block import cli


def test_compact():
    sut = cli.CLI()
    sut.parse(args=['-c'])
    assert sut.args.compact is True, "Compact flag should be true"


def test_compact_negated():
    sut = cli.CLI()
    sut.parse(args=[])
    assert sut.args.compact is False, "Compact flag should be false"


def test_log_level_set():
    sut = cli.CLI()
    sut.parse(args=['-l=warning'])
    assert sut.get_log_level == logging.WARNING, "log level should be warning"


def test_log_level_wrong():
    sut = cli.CLI()
    with pytest.raises(SystemExit):
        sut.parse(args=['--loglevel=fubar'])
