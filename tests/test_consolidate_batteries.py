import os

import pytest

from i3_battery_block_vgg.battery import consolidate_batteries
from i3_battery_block_vgg.state import State
from i3_battery_block_vgg.timeparser import parse_time

example_dir = os.path.join(os.getcwd(), 'tests', 'examples')


def read_file(filename: str) -> str:
    with open(os.path.join(example_dir, filename), 'r') as test_case:
        return "\n".join(test_case.readlines())


@pytest.mark.parametrize(
    "file_name, expected",
    [
        ('both_batteries_full.txt', [
            {'id': 0, 'state': State.FULL, 'percentage': 100, 'time': None,
             'unavailable': False, 'design_capacity': 1874, 'full_capacity': 1814},
            {'id': 1, 'state': State.FULL, 'percentage': 100, 'time': None,
             'unavailable': False, 'design_capacity': 1870, 'full_capacity': 1544}
        ]
         ),
        ('charging_buged_somewhat.txt', [
            {'id': 0, 'state': State.UNKNOWN, 'percentage': 79, 'time': None,
             'unavailable': False, 'design_capacity': 1977, 'full_capacity': 1803},
            {'id': 1, 'state': State.UNKNOWN, 'percentage': 0, 'time': None,
             'unavailable': True, 'design_capacity': None, 'full_capacity': None},
            {'id': 2, 'state': State.CHARGING, 'percentage': 100, 'time': None,
             'unavailable': False, 'design_capacity': 1860, 'full_capacity': 1512}
        ]
         ),
        ('charging_from_low_state_with_bug.txt', [
            {'id': 0, 'state': State.CHARGING, 'percentage': 76, 'time': parse_time('00:18:24'),
             'unavailable': False, 'design_capacity': 1873, 'full_capacity': 1708},
            {'id': 1, 'state': State.UNKNOWN, 'percentage': 0, 'time': None,
             'unavailable': True, 'design_capacity': None, 'full_capacity': None},
            {'id': 2, 'state': State.UNKNOWN, 'percentage': 4, 'time': None,
             'unavailable': False, 'design_capacity': 2160, 'full_capacity': 1756}
        ]
         ),
        ('discharge_bug_verbose.txt', [
            {'id': 0, 'state': State.UNKNOWN, 'percentage': 89, 'time': None,
             'unavailable': False, 'design_capacity': 1960, 'full_capacity': 1898},
            {'id': 1, 'state': State.DISCHARGING, 'percentage': 0, 'time': None,
             'unavailable': True, 'design_capacity': None, 'full_capacity': None},
            {'id': 2, 'state': State.CHARGING, 'percentage': 6, 'time': parse_time('00:54:00'),
             'unavailable': False, 'design_capacity': 2010, 'full_capacity': 1658}
        ]
         ),
        ('discharge_with_bug_verbose.txt', [
            {'id': 0, 'state': State.UNKNOWN, 'percentage': 95, 'time': None,
             'unavailable': False, 'design_capacity': 1924, 'full_capacity': 1755},
            {'id': 1, 'state': State.UNKNOWN, 'percentage': 0, 'time': None,
             'unavailable': True, 'design_capacity': None, 'full_capacity': None},
            {'id': 2, 'state': State.DISCHARGING, 'percentage': 90, 'time': parse_time('01:55:29'),
             'unavailable': False, 'design_capacity': 1985, 'full_capacity': 1614}
        ]
         ),
        ('one_battery_almost_discharged.txt', [
            {'id': 0, 'state': State.DISCHARGING, 'percentage': 94, 'time': parse_time('03:03:39'),
             'unavailable': False, 'design_capacity': 1988, 'full_capacity': 1813},
            {'id': 1, 'state': State.UNKNOWN, 'percentage': 0, 'time': None,
             'unavailable': True, 'design_capacity': None, 'full_capacity': None},
            {'id': 2, 'state': State.UNKNOWN, 'percentage': 5, 'time': None,
             'unavailable': False, 'design_capacity': 2173, 'full_capacity': 1768}
        ]
         ),
        ('recharging_wo_bug_ba1_empty.txt', [
            {'id': 0, 'state': State.CHARGING, 'percentage': 61, 'time': parse_time('00:19:47'),
             'unavailable': False, 'design_capacity': 1878, 'full_capacity': 1705},
            {'id': 1, 'state': State.UNKNOWN, 'percentage': 3, 'time': None,
             'unavailable': False, 'design_capacity': 2394, 'full_capacity': 1977}
        ]
         ),
    ]
)
def test_consolidate_both_full(file_name, expected):
    sut = consolidate_batteries(read_file(file_name))
    assert sut == expected, "read test case did not result in expected structure"
