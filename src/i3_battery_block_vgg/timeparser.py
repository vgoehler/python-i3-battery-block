import re
import sys
from datetime import time


def parse_time(time_input: str) -> time:
    """parses HH:MM and HH:MM:SS time stamps"""
    if sys.version_info < (3, 7):
        return __parse_time_manually(time_input)
    else:
        return time.fromisoformat(time_input)


def __parse_time_manually(time_input: str) -> time:
    search = re.compile("(?P<hour>[0-9]{1,2}):(?P<minute>[0-9]{1,2}):*(?P<second>[0-9]{0,2})")
    re_obj = re.match(search, time_input).groupdict()
    return time(hour=int(re_obj['hour']), minute=int(re_obj['minute']),
                second=int(re_obj['second']) if re_obj['second'] else 0)
