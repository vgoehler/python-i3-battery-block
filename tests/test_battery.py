import subprocess
from datetime import time

from i3_battery_block import battery
from i3_battery_block.battery import distill_text, refine_input
from i3_battery_block.font_awesome_glyphs import FA_NO_BATTERY, FA_BATTERY_LIST
from i3_battery_block.html_formatter import wrap_span, color


def test_get_power_status():
    # this should retrieve acpi output
    sut = battery.get_power_status()
    expected = subprocess.run("acpi", capture_output=True, universal_newlines=True)
    assert sut == expected.stdout, "both outputs should be from acpi and equal"


def test_distill_text_empty():
    # this should output text for no battery found
    expected = (wrap_span(FA_NO_BATTERY, "red"), 100)
    assert distill_text('') == expected, "no battery output should be given"


#def test_distill_text_discharge():
#    status = 'Battery 0: Full, 100%\n' \
#            'Battery 1: Discharging, 88%, 00:50:14 remaining\n'
#    expected = (wrap_span("0 %s 1 %s" % (FA_BATTERY_LIST[4], FA_BATTERY_LIST[3])) + wrap_span("94%%", color(94)), 94)
#    assert distill_text(status) == expected, "expected discharge text"


