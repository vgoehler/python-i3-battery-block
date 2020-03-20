from datetime import time
from typing import List

import pytest

from i3_battery_block_vgg.battery_timer import battery_timer


@pytest.mark.parametrize(
    "capacities, percentages, expected, nr_for_in_time, in_time",
    [
        ([2000, 2000], [1, 1], "02:00", 0, time(hour=1)),
        ([1000, 2000], [1, 1], "03:00", 0, time(hour=1)),
        ([1000, 2000], [1, 1], "01:30", 1, time(hour=1)),
        ([2000], [1], "01:00", 0, time(hour=1)),
        ([2000, 2000], [0.5, 0.5], "02:00", 0, time(hour=1)),
        ([1000, 2000], [0.5, 0.5], "03:00", 0, time(hour=1)),
        ([1000, 2000], [0.5, 0.5], "01:30", 1, time(hour=1)),
        ([2000, 2000], [0.25, 0.5], "03:00", 0, time(hour=1)),
        ([2000, 2000], [0.5, 0.25], "01:30", 0, time(hour=1)),
        ([2000, 2000], [0, 0.5], "01:00", 1, time(hour=1)),
        ([2000, 2000], [0.5, 0], "01:00", 0, time(hour=1)),
        ([1000, 10], [1, 1], "> 1 day", 1, time(hour=1)),
    ]
)
def test_calculate_time(capacities: List[int], percentages: List[float],
                        expected: str, nr_for_in_time: int, in_time: time):
    sut = battery_timer()
    sut.time = in_time
    sut.battery_nr_for_time = nr_for_in_time
    sut.capacities = capacities
    sut.percentages = percentages
    assert sut.calculate_time() == expected


@pytest.mark.parametrize(
    "batteries, exp_nr_time, exp_time, exp_cap, exp_per",
    [
        ([{"time": time(hour=1), "full_capacity": 1000, "percentage": 100}], 0, time(hour=1), [1000], [1]),
        ([{"time": time(hour=1), "full_capacity": 1000, "percentage": 100},
          {"time": None, "full_capacity": 1100, "percentage": 0}], 0, time(hour=1), [1000, 1100], [1, 0]),
        ([{"time": None, "full_capacity": 900, "percentage": 100},
          {"time": time(hour=1), "full_capacity": 1000, "percentage": 100}], 1, time(hour=1), [900, 1000], [1, 1]),
    ]
)
def test_set_timer(batteries, exp_nr_time, exp_time, exp_cap, exp_per):
    sut = battery_timer()
    for battery in batteries:
        sut.set_timer(battery)
    assert sut.time == exp_time
    assert sut.battery_nr_for_time == exp_nr_time
    assert sut.capacities == exp_cap
    assert sut.percentages == exp_per


def test_for_set_time_true():
    sut = battery_timer()
    sut.time = time(hour=1)
    assert sut.time_is_set


def test_for_set_time_false():
    sut = battery_timer()
    assert not sut.time_is_set


def test_average_without_bug():
    sut = battery_timer()
    sut.percentages = [.75, .75]
    assert sut.calculate_avg_percentage() == 75, "average is wrong"


def test_average_with_no_percentages():
    sut = battery_timer()
    assert sut.calculate_avg_percentage() == 0, "average is wrong"
