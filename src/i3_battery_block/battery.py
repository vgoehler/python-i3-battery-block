# Copyright (C) 2016 James Murphy
# Licensed under the GPL version 2 only
#
# A battery indicator blocklet script for i3blocks

import re
from datetime import time
from subprocess import check_output
from typing import Tuple, Dict, Any

from i3_battery_block.font_awesome_glyphs import FA_BATTERY, FA_NO_BATTERY
from i3_battery_block.font_awesome_glyphs import FA_LIGHTNING
from i3_battery_block.font_awesome_glyphs import FA_PLUG
from i3_battery_block.font_awesome_glyphs import FA_QUESTION
from i3_battery_block.html_formatter import color
from i3_battery_block.html_formatter import wrap_span

# stands for charging
FA_LIGHTNING_SPAN = wrap_span(FA_LIGHTNING, "yellow")

# stands for plugged in
FA_PLUG_SPAN = wrap_span(FA_PLUG)

# stands for using battery
FA_BATTERY_SPAN = wrap_span(FA_BATTERY)

# stands for unknown status of battery
FA_QUESTION_SPAN = wrap_span(FA_QUESTION)


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


def distill_text(status: str) -> Tuple[str, int]:
    if status:
        state_batteries = []
        commasplitstatus_batteries = []
        percentleft_batteries = []
        time = ""
        timeleft = None
        batteries = []
        for battery in status.split("\n"):
            if battery != '':
                batteries.append(refine_input(battery))

                state_batteries.append(battery.split(": ")[1].split(", ")[0])
                commasplitstatus = battery.split(", ")
                if not time:
                    timeleft = ""
                    time = commasplitstatus[-1].strip()
                    # check if it matches a time
                    time = re.match(r"(\d+):(\d+)", time)
                    if time:
                        time = ":".join(time.groups())
                        timeleft = " ({})".format(time)

                p = int(commasplitstatus[1].rstrip("%\n"))
                if p > 0:
                    percentleft_batteries.append(p)
                commasplitstatus_batteries.append(commasplitstatus)
        commasplitstatus = commasplitstatus_batteries[0]
        if percentleft_batteries:
            percent_left = int(sum(percentleft_batteries) / len(percentleft_batteries))
        else:
            percent_left = 0

        # deceiver state of batteries, if one is unknown take the state of the other
        unknowntext = FA_QUESTION_SPAN + " " + FA_BATTERY_SPAN + " "
        fulltext = ''
        for state in state_batteries:
            if fulltext == unknowntext:
                # remove the entry if it is unknown and replace it with the actual one
                fulltext = ''
            if state == "Discharging":
                fulltext += FA_BATTERY_SPAN + " "
            elif state == "Full":
                fulltext += FA_PLUG_SPAN + " "
                timeleft = ""
            elif state == "Unknown" and fulltext == '':
                fulltext += unknowntext
                timeleft = ""
            else:
                fulltext += FA_LIGHTNING_SPAN + " " + FA_PLUG_SPAN + " "

        form = '<span col="{}">{}%</span>'
        fulltext += form.format(color(percent_left), percent_left)
        fulltext += timeleft
    else:
        # stands for no battery found
        fulltext = wrap_span(FA_NO_BATTERY, "red")
        percent_left = 100
    return fulltext, percent_left


def output(output_text: str):
    # from blocks documentation:
    # the 1st line updates the full_text;
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
