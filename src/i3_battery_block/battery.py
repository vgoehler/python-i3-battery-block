#!/usr/bin/env python3
#
#
# Copyright (C) 2016 James Murphy
# Licensed under the GPL version 2 only
#
# A battery indicator blocklet script for i3blocks

import re
from subprocess import check_output


def wrap_span(text: str, col: str = None) -> str:
    """
    :type text: string, the text that should be wraped in the span
    :type col: string, a html color string
    """
    color_text = " col='%s'" % col if col else ""
    return "<span font='FontAwesome'%s>%s</span>" % (color_text, text)


def color(percent):
    if percent < 0 or percent > 100:
        raise AttributeError("Threshold %i is out of percent range." % percent)

    # we only need the first number
    deca = percent // 10
    return __COLOR_MAP[deca]


# as exit code 33 will turn background red 0-9 percent font is white
__COLOR_MAP = {
    0: "#FFFFFF",
    1: "#FF3300",
    2: "#FF6600",
    3: "#FF9900",
    4: "#FFCC00",
    5: "#FFFF00",
    6: "#FFFF33",
    7: "#FFFF66",
    8: "#FFFFFF",
    9: "#FFFFFF",
    10: "#FFFFFF",
}

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
    timeleft = None
    for battery in batteries:
        if battery != '':
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
        percentleft = int(sum(percentleft_batteries) / len(percentleft_batteries))
    else:
        percentleft = 0

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

    form = '<span col="{}">{}%</span>'
    fulltext += form.format(color(percentleft), percentleft)
    fulltext += timeleft

print(fulltext)
print(fulltext)
if percentleft < 10:
    exit(33)
