from i3_battery_block_vgg.battery import refine_input
from i3_battery_block_vgg.state import State
from i3_battery_block_vgg.timeparser import parse_time


def test_refine_input_discharge():
    status_line = 'Battery 1: Discharging, 88%, 00:50:14 remaining'
    expected = {'state': State.DISCHARGING, 'percentage': 88, 'time': parse_time('00:50:14'), 'unavailable': False}
    assert refine_input(status_line) == expected, "re matching is broken"


def test_refine_input_charge():
    status_line = 'Battery 2: Charging, 88%, 00:09:24 until charged'
    expected = {'state': State.CHARGING, 'percentage': 88, 'time': parse_time('00:09:24'), 'unavailable': False}
    assert refine_input(status_line) == expected, "re matching is broken"


def test_refine_input_charge_no_time():
    status_line = 'Battery 2: Charging, 100%, until charged'
    expected = {'state': State.CHARGING, 'percentage': 100, 'time': None, 'unavailable': False}
    assert refine_input(status_line) == expected, "re matching is broken"


def test_refine_input_charge_zero_rate():
    status_line = 'Battery 2: Charging, 88%, charging at zero rate - will never fully charge.'
    expected = {'state': State.CHARGING, 'percentage': 88, 'time': None, 'unavailable': False}
    assert refine_input(status_line) == expected, "re matching is broken"


def test_refine_input_unknown():
    status_line = "Battery 1: Unknown, 0%, rate information unavailable"
    expected = {'state': State.UNKNOWN, 'percentage': 0, 'time': None, 'unavailable': True}
    assert refine_input(status_line) == expected, "re matching is broken"


def test_refine_input_unknown_no_additional_text():
    status_line = 'Battery 2: Unknown, 5%'
    expected = {'state': State.UNKNOWN, 'percentage': 5, 'time': None, 'unavailable': False}
    assert refine_input(status_line) == expected, "re matching is broken"


def test_refine_input_full():
    status_line = "Battery 0: Full, 100%"
    expected = {'state': State.FULL, 'percentage': 100, 'time': None, 'unavailable': False}
    assert refine_input(status_line) == expected, "re matching is broken"
