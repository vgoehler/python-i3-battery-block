import subprocess
from datetime import time

from i3_battery_block import battery
from i3_battery_block.battery import distill_text
from i3_battery_block.battery import prepare_output
from i3_battery_block.font_awesome_glyphs import FA_BATTERY_LIST
from i3_battery_block.font_awesome_glyphs import FA_LAPTOP
from i3_battery_block.font_awesome_glyphs import FA_NO_BATTERY
from i3_battery_block.font_awesome_glyphs import FA_PLUG
from i3_battery_block.font_awesome_glyphs import FA_QUESTION
from i3_battery_block.html_formatter import color
from i3_battery_block.html_formatter import wrap_span
from i3_battery_block.html_formatter import wrap_span_battery_header
from i3_battery_block.html_formatter import wrap_span_bug
from i3_battery_block.html_formatter import wrap_span_fa


def test_get_power_status():
    # this should retrieve acpi output
    try:
        sut = battery.get_power_status()
        expected = subprocess.run("acpi", capture_output=True, universal_newlines=True)
        assert sut == expected.stdout, "both outputs should be from acpi and equal"
    except FileNotFoundError as e:
        # if no acpi is there (ci server) test for correct error message
        assert e.errno == 2, "extraordinary failure"


def test_distill_text_empty():
    # this should output text for no battery found
    no_battery = wrap_span(FA_NO_BATTERY, "red")
    expected = (no_battery, no_battery, 100)
    assert distill_text('') == expected, "no battery output should be given"


def test_prepare_output_charging():
    # first battery charging with 70% and second battery unknown with 0%
    sut = [
        {"state": 'Charging', 'percentage': 70, 'time': time.fromisoformat("01:33:02"), 'unavailable': False},
        {"state": 'Unknown', 'percentage': 0, 'time': None, 'unavailable': False},
    ]
    expected = [wrap_span_battery_header(1) + wrap_span_fa(FA_PLUG, "yellow") + wrap_span_fa(FA_BATTERY_LIST[3]),
                wrap_span_battery_header(2) + wrap_span_fa(FA_QUESTION) + wrap_span_fa(FA_BATTERY_LIST[0]),
                wrap_span("35%", color(35)),
                wrap_span("(01:33)")
                ]
    input_list = []
    prepare_output(sut, input_list, [])
    assert input_list == expected, "output is not according to specifications"


def test_prepare_output_full():
    # first battery Full and second battery unknown with 100%
    sut = [
        {"state": 'Full', 'percentage': 100, 'time': None, 'unavailable': False},
        {"state": 'Unknown', 'percentage': 100, 'time': None, 'unavailable': False},
    ]
    expected = [wrap_span_battery_header(1) + wrap_span_fa(FA_PLUG) + wrap_span_fa(FA_BATTERY_LIST[4]),
                wrap_span_battery_header(2) + wrap_span_fa(FA_QUESTION) + wrap_span_fa(FA_BATTERY_LIST[4]),
                wrap_span("100%", color(100)),
                ]
    input_list = []
    prepare_output(sut, input_list, [])
    assert input_list == expected, "output is not according to specifications"


def test_prepare_output_discharging():
    # first battery discharging with 70% and second battery unknown with 0%
    sut = [
        {"state": 'Discharging', 'percentage': 70, 'time': time.fromisoformat("01:33:02"), 'unavailable': False},
        {"state": 'Unknown', 'percentage': 0, 'time': None, 'unavailable': False},
    ]
    expected = [wrap_span_battery_header(1) + wrap_span_fa(FA_LAPTOP) + wrap_span_fa(FA_BATTERY_LIST[3]),
                wrap_span_battery_header(2) + wrap_span_fa(FA_QUESTION) + wrap_span_fa(FA_BATTERY_LIST[0]),
                wrap_span("35%", color(35)),
                wrap_span("(01:33)"),
                ]
    input_list = []
    prepare_output(sut, input_list, [])
    assert input_list == expected, "output is not according to specifications"


def test_for_remove_of_battery_bug():
    # first battery discharging with 70% and second battery unknown with 0%
    sut = [
        {"state": 'Full', 'percentage': 100, 'time': None, 'unavailable': False},
        {"state": 'Unknown', 'percentage': 0, 'time': None, 'unavailable': True},
        {"state": 'Unknown', 'percentage': 88, 'time': None, 'unavailable': False},
    ]
    expected = [wrap_span_battery_header(1) + wrap_span_fa(FA_PLUG) + wrap_span_fa(FA_BATTERY_LIST[4]),
                wrap_span_battery_header(2) + wrap_span_fa(FA_QUESTION) + wrap_span_fa(FA_BATTERY_LIST[4]),
                wrap_span("94%", color(94)),
                ]
    input_list = []
    prepare_output(sut, input_list, [])
    assert input_list == expected, "output is not according to specifications"


def test_for_remove_of_battery_bug_with_indicator():
    # first battery discharging with 70% and second battery unknown with 0%
    sut = [
        {"state": 'Full', 'percentage': 100, 'time': None, 'unavailable': False},
        {"state": 'Unknown', 'percentage': 0, 'time': None, 'unavailable': True},
        {"state": 'Unknown', 'percentage': 88, 'time': None, 'unavailable': False},
    ]
    expected = [wrap_span_bug(),
                wrap_span_battery_header(1) + wrap_span_fa(FA_PLUG) + wrap_span_fa(FA_BATTERY_LIST[4]),
                wrap_span_battery_header(2) + wrap_span_fa(FA_QUESTION) + wrap_span_fa(FA_BATTERY_LIST[4]),
                wrap_span("94%", color(94)),
                ]
    input_list = []
    prepare_output(sut, input_list, [], show_bug=True)
    assert input_list == expected, "output is not according to specifications"


def test_average_without_bug():
    assert battery.__calculate_avg_percentage(150, 2, False) == 75, "average is wrong"


def test_average_with_bug():
    assert battery.__calculate_avg_percentage(150, 3, True) == 75, "average is wrong"
