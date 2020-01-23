# Copyright (C) 2016 James Murphy
# Licensed under the GPL version 2 only
#
# A battery indicator blocklet script for i3blocks

import re
from subprocess import check_output

from i3_battery_block.font_awesome_glyphs import FA_BATTERY
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
    fulltext += form.format(color(percentleft), percentleft)
    fulltext += timeleft

print(fulltext)
print(fulltext)
if percentleft < 10:
    exit(33)
