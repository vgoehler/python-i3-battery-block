#!/usr/bin/env python3
#
#
# Copyright (C) 2016 James Murphy
# Licensed under the GPL version 2 only
#
# A battery indicator blocklet script for i3blocks

import re
from subprocess import check_output


def wrap_span(text: str, color: str = None) -> str:
    """
    :type text: string, the text that should be wraped in the span
    :type color: string, a html color string
    """
    color_text = "color='%s'" % color if color else ""
    return "<span font='FontAwesome' %s >%s</span>" % (color_text, text)


status = check_output(['acpi'], universal_newlines=True)

if not status:
    # stands for no battery found
    fulltext = wrap_span("\uf00d \uf240", "red")
    percentleft = 100
else:
    # if there is more than one battery in one laptop, the percentage left is 
    # available for each battery separately, although state and remaining 
    # time for overall block is shown in the status of the first battery 
    batteries = status.split("\n")
    state_batteries = []
    commasplitstatus_batteries = []
    percentleft_batteries = []
    time = ""
    for battery in batteries:
        if battery != '':
            state_batteries.append(battery.split(": ")[1].split(", ")[0])
            commasplitstatus = battery.split(", ")
            if not time:
                time = commasplitstatus[-1].strip()
                # check if it matches a time
                time = re.match(r"(\d+):(\d+)", time)
                if time:
                    time = ":".join(time.groups())
                    timeleft = " ({})".format(time)
                else:
                    timeleft = ""

            p = int(commasplitstatus[1].rstrip("%\n"))
            if p > 0:
                percentleft_batteries.append(p)
            commasplitstatus_batteries.append(commasplitstatus)
    commasplitstatus = commasplitstatus_batteries[0]
    if percentleft_batteries:
        percentleft = int(sum(percentleft_batteries) / len(percentleft_batteries))
    else:
        percentleft = 0

    # stands for charging
    FA_LIGHTNING = wrap_span("\uf0e7", "yellow")

    # stands for plugged in
    FA_PLUG = wrap_span('\uf1e6')

    # stands for using battery
    FA_BATTERY = wrap_span('\uf240')

    # stands for unknown status of battery
    FA_QUESTION = wrap_span('\uf128')

    FA_BATTERY_LIST = [
        "\uf244",  # empty
        "\uf243",  # 1 quarter
        "\uf242",  # half
        "\uf241",  # 3 quarters
        "\uf240",  # full
    ]

    # deceiver state of batteries, if one is unknown take the state of the other
    unknowntext = FA_QUESTION + " " + FA_BATTERY + " "
    fulltext = ''
    for state in state_batteries:
        if fulltext == unknowntext:
            # remove the entry if it is unknown and replace it with the actual one
            fulltext = ''
        if state == "Discharging":
            fulltext += FA_BATTERY + " "
        elif state == "Full":
            fulltext += FA_PLUG + " "
            timeleft = ""
        elif state == "Unknown" and fulltext == '':
            fulltext += unknowntext
            timeleft = ""
        else:
            fulltext += FA_LIGHTNING + " " + FA_PLUG + " "


    def color(percent):
        if percent < 10:
            # exit code 33 will turn background red
            return "#FFFFFF"
        if percent < 20:
            return "#FF3300"
        if percent < 30:
            return "#FF6600"
        if percent < 40:
            return "#FF9900"
        if percent < 50:
            return "#FFCC00"
        if percent < 60:
            return "#FFFF00"
        if percent < 70:
            return "#FFFF33"
        if percent < 80:
            return "#FFFF66"
        return "#FFFFFF"


    form = '<span color="{}">{}%</span>'
    fulltext += form.format(color(percentleft), percentleft)
    fulltext += timeleft

print(fulltext)
print(fulltext)
if percentleft < 10:
    exit(33)
