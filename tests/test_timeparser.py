from datetime import time

import pytest

from i3_battery_block_vgg.timeparser import __parse_time_manually
from i3_battery_block_vgg.timeparser import parse_time


@pytest.mark.parametrize(
    "time_input, expected",
    [
        ("12:13", time(hour=12, minute=13)),
        ("12:13:14", time(hour=12, minute=13, second=14)),
        ('00:54:00', time(hour=0, minute=54, second=0))
    ]
)
def test_manually_time_parsing(time_input: str, expected: time):
    assert __parse_time_manually(time_input) == expected, "manual time parsing has gone wrong"


@pytest.mark.parametrize(
    "time_input, expected",
    [
        ("12:13", time(hour=12, minute=13)),
        ("12:13:14", time(hour=12, minute=13, second=14)),
        ('00:54:00', time(hour=0, minute=54, second=0))
    ]
)
def test_time_parsing(time_input: str, expected: time):
    assert parse_time(time_input) == expected, "time parsing has gone wrong"
