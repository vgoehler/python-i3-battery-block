import subprocess

import pytest

from i3_battery_block_vgg import battery
from i3_battery_block_vgg.battery import discern_system_states
from i3_battery_block_vgg.battery import prepare_output
from i3_battery_block_vgg.font_awesome_glyphs import FA_BATTERY_LIST
from i3_battery_block_vgg.font_awesome_glyphs import FA_LAPTOP
from i3_battery_block_vgg.font_awesome_glyphs import FA_PLUG
from i3_battery_block_vgg.font_awesome_glyphs import FA_QUESTION
from i3_battery_block_vgg.html_formatter import color
from i3_battery_block_vgg.html_formatter import wrap_span
from i3_battery_block_vgg.html_formatter import wrap_span_battery_header
from i3_battery_block_vgg.html_formatter import wrap_span_bug
from i3_battery_block_vgg.html_formatter import wrap_span_fa
from i3_battery_block_vgg.state import State
from i3_battery_block_vgg.timeparser import parse_time


def test_get_power_status():
    # this should retrieve acpi output
    try:
        sut = battery.get_power_state()
        expected = subprocess.run("acpi", capture_output=True, universal_newlines=True)
        assert sut == expected.stdout, "both outputs should be from acpi and equal"
    except FileNotFoundError as e:
        # if no acpi is there (ci server) test for correct error message
        assert e.errno == 2, "extraordinary failure"


def test_prepare_output_charging():
    # first battery charging with 70% and second battery unknown with 0%
    sut = [
        {"state": State.CHARGING, 'percentage': 70, 'time': parse_time("01:33:02"), 'unavailable': False},
        {"state": State.UNKNOWN, 'percentage': 0, 'time': None, 'unavailable': False},
    ]
    expected = [wrap_span_battery_header(1) + wrap_span_fa(FA_PLUG, "yellow") + ' ' + wrap_span_fa(FA_BATTERY_LIST[3])
                + ' ',
                wrap_span_battery_header(2) + wrap_span_fa(FA_QUESTION) + ' ' + wrap_span_fa(FA_BATTERY_LIST[0]) + ' ',
                wrap_span("35%", color(35)),
                wrap_span("(01:33)")
                ]
    input_list = []
    prepare_output(sut, input_list, [])
    assert input_list == expected, "output is not according to specifications"


def test_prepare_output_charging_small():
    sut = [
        {"state": State.CHARGING, 'percentage': 70, 'time': parse_time("01:33:02"), 'unavailable': False},
        {"state": State.UNKNOWN, 'percentage': 0, 'time': None, 'unavailable': False},
    ]
    expected = [wrap_span_fa(FA_PLUG, "yellow"),
                wrap_span_fa(FA_BATTERY_LIST[1], col=color(35)),
                wrap_span("(01:33)")
                ]
    input_list = []
    prepare_output(sut, [], input_list)
    assert input_list == expected, "output is not according to specifications"


def test_prepare_output_charging_small_any_order():
    sut = [
        {"state": State.UNKNOWN, 'percentage': 0, 'time': None, 'unavailable': False},
        {"state": State.CHARGING, 'percentage': 70, 'time': parse_time("01:33:02"), 'unavailable': False},
    ]
    expected = [wrap_span_fa(FA_PLUG, "yellow"),
                wrap_span_fa(FA_BATTERY_LIST[1], col=color(35)),
                wrap_span("(01:33)")
                ]
    input_list = []
    prepare_output(sut, [], input_list)
    assert input_list == expected, "output is not according to specifications"


def test_prepare_output_full():
    # first battery Full and second battery unknown with 100%
    sut = [
        {"state": State.FULL, 'percentage': 100, 'time': None, 'unavailable': False},
        {"state": State.UNKNOWN, 'percentage': 100, 'time': None, 'unavailable': False},
    ]
    expected = [wrap_span_battery_header(1) + wrap_span_fa(FA_PLUG) + ' ' + wrap_span_fa(FA_BATTERY_LIST[4]) + ' ',
                wrap_span_battery_header(2) + wrap_span_fa(FA_QUESTION) + ' ' + wrap_span_fa(FA_BATTERY_LIST[4]) + ' ',
                wrap_span("100%", color(100)),
                ]
    input_list = []
    prepare_output(sut, input_list, [])
    assert input_list == expected, "output is not according to specifications"


def test_prepare_output_full_small():
    sut = [
        {"state": State.FULL, 'percentage': 100, 'time': None, 'unavailable': False},
        {"state": State.UNKNOWN, 'percentage': 100, 'time': None, 'unavailable': False},
    ]
    expected = [wrap_span_fa(FA_PLUG),
                wrap_span_fa(FA_BATTERY_LIST[4], col=color(100)),
                ]
    input_list = []
    prepare_output(sut, [], input_list)
    assert input_list == expected, "output is not according to specifications"


def test_prepare_output_full_small_any_order():
    sut = [
        {"state": State.UNKNOWN, 'percentage': 100, 'time': None, 'unavailable': False},
        {"state": State.FULL, 'percentage': 100, 'time': None, 'unavailable': False},
    ]
    expected = [wrap_span_fa(FA_PLUG),
                wrap_span_fa(FA_BATTERY_LIST[4], col=color(100)),
                ]
    input_list = []
    prepare_output(sut, [], input_list)
    assert input_list == expected, "output is not according to specifications"


def test_prepare_output_discharging():
    # first battery discharging with 70% and second battery unknown with 0%
    sut = [
        {"state": State.DISCHARGING, 'percentage': 70, 'time': parse_time("01:33:02"), 'unavailable': False},
        {"state": State.UNKNOWN, 'percentage': 0, 'time': None, 'unavailable': False},
    ]
    expected = [wrap_span_battery_header(1) + wrap_span_fa(FA_LAPTOP) + ' ' + wrap_span_fa(FA_BATTERY_LIST[3]) + ' ',
                wrap_span_battery_header(2) + wrap_span_fa(FA_QUESTION) + ' ' + wrap_span_fa(FA_BATTERY_LIST[0]) + ' ',
                wrap_span("35%", color(35)),
                wrap_span("(01:33)"),
                ]
    input_list = []
    prepare_output(sut, input_list, [])
    assert input_list == expected, "output is not according to specifications"


def test_prepare_output_discharging_small():
    sut = [
        {"state": State.DISCHARGING, 'percentage': 70, 'time': parse_time("01:33:02"), 'unavailable': False},
        {"state": State.FULL, 'percentage': 100, 'time': None, 'unavailable': False},
        {"state": State.UNKNOWN, 'percentage': 0, 'time': None, 'unavailable': False},
    ]
    expected = [wrap_span_fa(FA_LAPTOP),
                wrap_span_fa(FA_BATTERY_LIST[2], col=color(57)),
                wrap_span("(01:33)"),
                ]
    input_list = []
    prepare_output(sut, [], input_list)
    assert input_list == expected, "output is not according to specifications"


def test_prepare_output_discharging_small_other_order():
    sut = [
        {"state": State.FULL, 'percentage': 100, 'time': None, 'unavailable': False},
        {"state": State.UNKNOWN, 'percentage': 0, 'time': None, 'unavailable': False},
        {"state": State.DISCHARGING, 'percentage': 70, 'time': parse_time("01:33:02"), 'unavailable': False},
    ]
    expected = [wrap_span_fa(FA_LAPTOP),
                wrap_span_fa(FA_BATTERY_LIST[2], col=color(57)),
                wrap_span("(01:33)"),
                ]
    input_list = []
    prepare_output(sut, [], input_list)
    assert input_list == expected, "output is not according to specifications"


def test_for_remove_of_battery_bug():
    # first battery discharging with 70% and second battery unknown with 0%
    sut = [
        {"state": State.FULL, 'percentage': 100, 'time': None, 'unavailable': False},
        {"state": State.UNKNOWN, 'percentage': 0, 'time': None, 'unavailable': True},
        {"state": State.UNKNOWN, 'percentage': 88, 'time': None, 'unavailable': False},
    ]
    expected = [wrap_span_battery_header(1) + wrap_span_fa(FA_PLUG) + ' ' + wrap_span_fa(FA_BATTERY_LIST[4]) + ' ',
                wrap_span_battery_header(2) + wrap_span_fa(FA_QUESTION) + ' ' + wrap_span_fa(FA_BATTERY_LIST[4]) + ' ',
                wrap_span("94%", color(94)),
                ]
    input_list = []
    prepare_output(sut, input_list, [])
    assert input_list == expected, "output is not according to specifications"


def test_for_remove_of_battery_bug_with_indicator():
    # first battery discharging with 70% and second battery unknown with 0%
    sut = [
        {"state": State.FULL, 'percentage': 100, 'time': None, 'unavailable': False},
        {"state": State.UNKNOWN, 'percentage': 0, 'time': None, 'unavailable': True},
        {"state": State.UNKNOWN, 'percentage': 88, 'time': None, 'unavailable': False},
    ]
    expected = [wrap_span_bug(),
                wrap_span_battery_header(1) + wrap_span_fa(FA_PLUG) + ' ' + wrap_span_fa(FA_BATTERY_LIST[4]) + ' ',
                wrap_span_battery_header(2) + wrap_span_fa(FA_QUESTION) + ' ' + wrap_span_fa(FA_BATTERY_LIST[4]) + ' ',
                wrap_span("94%", color(94)),
                ]
    input_list = []
    prepare_output(sut, input_list, [], show_bug=True)
    assert input_list == expected, "output is not according to specifications"


def test_average_without_bug():
    assert battery.__calculate_avg_percentage(150, 2, False) == 75, "average is wrong"


def test_average_with_bug():
    assert battery.__calculate_avg_percentage(150, 3, True) == 75, "average is wrong"


@pytest.mark.parametrize(
    "input_state, expected_state",
    [
        ([State.UNKNOWN], State.UNKNOWN),
        ([State.UNKNOWN, State.UNKNOWN, State.UNKNOWN], State.UNKNOWN),
        ([State.FULL], State.FULL),
        ([State.FULL, State.UNKNOWN, State.UNKNOWN], State.FULL),
        ([State.UNKNOWN, State.UNKNOWN, State.FULL], State.FULL),
        ([State.CHARGING], State.CHARGING),
        ([State.CHARGING, State.UNKNOWN, State.FULL], State.CHARGING),
        ([State.UNKNOWN, State.FULL, State.CHARGING], State.CHARGING),
        ([State.UNKNOWN, State.CHARGING], State.CHARGING),
        ([State.DISCHARGING], State.DISCHARGING),
        ([State.DISCHARGING, State.UNKNOWN, State.FULL], State.DISCHARGING),
        ([State.UNKNOWN, State.FULL, State.DISCHARGING], State.DISCHARGING),
        ([State.UNKNOWN, State.DISCHARGING], State.DISCHARGING),
    ]
)
def test_system_battery_status(input_state, expected_state):
    assert discern_system_states(input_state) == expected_state, "system battery state was not as expected."
