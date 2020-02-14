import logging

import pytest

from i3_battery_block_vgg import __version__
from i3_battery_block_vgg import cli


def test_compact():
    sut = cli.CLI()
    sut.parse(args=['-c'])
    assert sut.args.compact is True, "Compact flag should be true"


def test_compact_negated():
    sut = cli.CLI()
    sut.parse(args=[])
    assert sut.args.show_bug is False, "show bug flag should be false"


def test_show_bug():
    sut = cli.CLI()
    sut.parse(args=['--show_bug'])
    assert sut.args.show_bug is True, "show bug flag should be true"


def test_show_bug_negated():
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


def test_version_output(capsys):
    sut = cli.CLI()
    with pytest.raises(SystemExit) as e:
        sut.parse(args=['--version'])
    assert "0" in str(e.value)  # error code is zero
    output = capsys.readouterr()
    assert str.find(output.out, __version__) != -1
