# Copyright (C) 2016 James Murphy
# Licensed under the GPL version 2 only
#
# A battery indicator blocklet script for i3blocks

import re
from datetime import time
from subprocess import check_output
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from i3_battery_block.font_awesome_glyphs import FA_NO_BATTERY
from i3_battery_block.html_formatter import STATUS_SPANS
from i3_battery_block.html_formatter import color
from i3_battery_block.html_formatter import discern_loading_state
from i3_battery_block.html_formatter import wrap_span
from i3_battery_block.html_formatter import wrap_span_battery_header


def get_power_status() -> str:
    return check_output(['acpi'], universal_newlines=True)


def refine_input(status_line: str) -> Dict[str, Any]:
    re_battery_line = re.compile(r'^Battery [0-9]+: (?P<state>[a-zA-Z]+), (?P<percentage>[0-9]{1,3})%'
                                 r'(, (?P<time>[0-9:]+)[a-zA-Z ]*$|'
                                 r', (?P<rate_info>rate information unavailable)$|'
                                 r', [a-zA-Z \-.]+$|'
                                 r'$)')
    group = re.match(re_battery_line, status_line).groupdict()

    return {'state': group['state'], 'percentage': int(group['percentage']),
            'time': None if not group['time'] else time.fromisoformat(group['time']),
            'unavailable': group['rate_info'] == "rate information unavailable"}


def prepare_output(batteries: List[Dict[str, Any]]) -> Tuple[str, int]:
    """
    Each Battery gets its own block, where the state (charging or discharging) and then
    the image of the battery percentage is shown. After all the percentage of the whole System and the charge_discharge_timer
    (to charge or discharge) is put.
    :param batteries:  a list of battery dictionaries (as refine_input returns)
    :return: the format string
    """
    charge_discharge_timer = None  # only one battery is showing these information
    avg_percentage = 0
    full_text = []
    nr = 0
    for battery in batteries:
        nr += 1
        avg_percentage += battery['percentage']
        # if charge_discharge_timer not already set, set it if its there
        if not charge_discharge_timer and battery['time']:
            charge_discharge_timer = battery['time']
        # set full_text
        full_text.append(wrap_span_battery_header(nr) +
                         STATUS_SPANS[battery['state']] +
                         discern_loading_state(battery['percentage'])
                         )
    avg_percentage = avg_percentage // len(batteries)
    full_text.append(wrap_span("%s%%" % avg_percentage, col=color(avg_percentage)))

    if charge_discharge_timer:
        full_text.append(wrap_span("(%s)" % charge_discharge_timer.strftime("%H:%M")))

    return "".join(full_text), avg_percentage


def distill_text(status: str) -> Tuple[str, int]:
    if status:
        batteries = []
        for battery in status.split("\n"):
            if battery != '':
                batteries.append(refine_input(battery))

        full_text, avg_percentage = prepare_output(batteries)

    else:
        # stands for no battery found
        full_text = wrap_span(FA_NO_BATTERY, "red")
        avg_percentage = 100
    return full_text, avg_percentage


def output(output_text: str):
    # from blocks documentation:
    # the 1st line updates the generate_full_text;
    # the 2nd line updates the short_text;
    # the 3rd line updates the color;
    # the 4th line updates the background.
    print(output_text)
    print(output_text)


def main(compact: bool = False):
    status = get_power_status()
    text, percent_left = distill_text(status)

    output(text)

    if percent_left < 10:
        exit(33)  # red background
