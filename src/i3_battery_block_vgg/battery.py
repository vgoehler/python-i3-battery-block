import re
from subprocess import check_output
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from i3_battery_block_vgg.font_awesome_glyphs import FA_NO_BATTERY
from i3_battery_block_vgg.html_formatter import STATUS_SPANS
from i3_battery_block_vgg.html_formatter import color
from i3_battery_block_vgg.html_formatter import discern_loading_state
from i3_battery_block_vgg.html_formatter import wrap_span
from i3_battery_block_vgg.html_formatter import wrap_span_battery_header
from i3_battery_block_vgg.html_formatter import wrap_span_bug
from i3_battery_block_vgg.state import State
from i3_battery_block_vgg.timeparser import parse_time


def get_power_state() -> str:
    return check_output(['acpi'], universal_newlines=True)


def refine_input(status_line: str) -> Dict[str, Any]:
    re_battery_line = re.compile(r'^Battery (?P<id>[0-9]+): '
                                 r'((?P<state>[a-zA-Z]+), (?P<percentage>[0-9]{1,3})%'
                                 r'(, (?P<time>[0-9:]+)[a-zA-Z ]*$|'
                                 r', (?P<unavailable>rate information unavailable)$|'
                                 r', [a-zA-Z \-.]+$|'
                                 r'$)|'  # end of group state information line 1
                                 r'design capacity (?P<design_capacity>[0-9]+) mAh, '
                                 r'last full capacity (?P<full_capacity>[0-9]+) mAh = [0-9]{1,3}%$'
                                 ')')  # end of group capacity information line 2

    group = re.match(re_battery_line, status_line).groupdict()

    def none_or_convert_to_int(x):
        return None if not x else int(x)

    functions = {'id': int,
                 'state': lambda x: None if not x else State.get_state_according_to_value(x),
                 'percentage': none_or_convert_to_int,
                 'time': lambda x: None if not x else parse_time(x),
                 'unavailable': lambda x: x == "rate information unavailable",
                 'design_capacity': none_or_convert_to_int,
                 'full_capacity': none_or_convert_to_int}

    batteries = {}

    for key, value in group.items():
        batteries[key] = functions[key](value)

    return batteries


def distill_text(battery_text: str, compact: bool = False, show_bug: bool = False) -> Tuple[str, str, int]:
    if battery_text:
        batteries = consolidate_batteries(battery_text)

        full_text = []
        small_text = []
        avg_percentage = prepare_output(batteries, full_text, small_text, compact=compact, show_bug=show_bug)

        full_text = "".join(full_text)
        small_text = "".join(small_text)

    else:
        # stands for no battery found
        full_text = wrap_span(FA_NO_BATTERY, "red")
        small_text = full_text
        avg_percentage = 100

    if compact:
        return small_text, small_text, avg_percentage
    else:
        return full_text, small_text, avg_percentage


def consolidate_batteries(battery_text: str) -> List[Dict]:
    batteries = []
    for battery in battery_text.split("\n"):
        try:
            batteries.append(refine_input(battery))
        except AttributeError:
            # refine_input encountered an error, ignore this line
            continue
    return batteries


def output(full_text: str, small_text: str):
    # from blocks documentation:
    # the 1st line updates the generate_full_text;
    # the 2nd line updates the short_text;
    # the 3rd line updates the color;
    # the 4th line updates the background.
    print(full_text)
    print(small_text)


def main(compact: bool = False, show_bug: bool = False):
    state = get_power_state()
    full_text, small_text, percent_left = distill_text(state, compact=compact, show_bug=show_bug)

    output(full_text, small_text)

    if percent_left < 10:
        exit(33)  # red background


def prepare_output(batteries: List[Dict[str, Any]], full_text: List[str], small_text: List[str], compact: bool = False,
                   show_bug: bool = False) -> int:
    """
    Each Battery gets its own block, where the state (charging or discharging) and then the image of the battery
    percentage is shown. After all the percentage of the whole System and the charge_discharge_timer (to charge or
    discharge) is put. :param compact: :param show_bug: :param batteries:  a list of battery dictionaries (as
    refine_input returns) :return: the format string
    """
    charge_discharge_timer = None  # only one battery is showing these information
    avg_percentage = 0
    nr = 0
    bug_occurred = False
    for battery in batteries:
        # battery bug gate
        if battery['unavailable'] and battery['state'] == State.UNKNOWN:
            bug_occurred = True
            if show_bug:
                # bug icon in orange as first entry
                span_bug = wrap_span_bug()
                full_text.insert(0, span_bug)
                small_text.insert(0, span_bug)
            continue

        nr += 1
        avg_percentage += battery['percentage']
        # if charge_discharge_timer not already set, set it if its there
        if not charge_discharge_timer and battery['time']:
            charge_discharge_timer = battery['time']
        # set full_text
        full_text.append(wrap_span_battery_header(nr) +
                         STATUS_SPANS[battery['state']] + ' ' +
                         discern_loading_state(battery['percentage']) + ' '
                         )

    system_state = discern_system_states([b['state'] for b in batteries])
    small_text.append(STATUS_SPANS[system_state])

    avg_percentage = __calculate_avg_percentage(avg_percentage, len(batteries), bug_occurred)
    col = color(avg_percentage)
    full_text.append(wrap_span("%s%%" % avg_percentage, col=col))
    small_text.append(discern_loading_state(avg_percentage, color=col))

    if charge_discharge_timer:
        time_span = wrap_span("(%s)" % charge_discharge_timer.strftime("%H:%M"))
        full_text.append(time_span)
        small_text.append(time_span)

    return avg_percentage


def discern_system_states(states: List[State]) -> State:
    # in case only one entry, or only the same entries, reduce and return
    state_set = set(states)
    if len(state_set) == 1:
        return state_set.pop()
    # if charging or discharging is in list then return this
    for state in [State.CHARGING, State.DISCHARGING]:
        if state_set.issuperset([state]):
            return state
    if state_set.issuperset([State.FULL]):
        return State.FULL
    raise NotImplementedError("This should not happen. All States are set.")


def __calculate_avg_percentage(percentage_sum: int, battery_count: int, bug_occurred: bool) -> int:
    return percentage_sum // (battery_count - 1 if bug_occurred else battery_count)
