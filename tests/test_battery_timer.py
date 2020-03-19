from datetime import time
from typing import List

import pytest

from i3_battery_block_vgg.battery_timer import battery_timer


@pytest.mark.parametrize(
    "capacities, expected, in_time",
    [
        ([2000, 2000], "02:00", time(hour=1)),
        ([2000], "01:00", time(hour=1)),
    ]
)
def test_calculate_time(capacities: List, expected: str, in_time: time):
    sut = battery_timer()
    sut.time = in_time
    sut.capacities = capacities
    assert sut.calculate_time() == expected
