import datetime
from typing import Dict
from typing import List

from i3_battery_block_vgg.html_formatter import wrap_span


class battery_timer:
    capacities: List = []
    time: datetime = None

    def __init__(self):
        pass

    def set_timer(self, battery: Dict) -> None:
        if not self.time and battery['time']:
            self.time = battery['time']
        if battery['full_capacity']:
            self.capacities.append(battery['full_capacity'])

    def output_timer(self, full_text: List[str], small_text: [str]) -> None:
        if self.time:
            time_span = wrap_span("(%s)" % self.calculate_time())
            full_text.append(time_span)
            small_text.append(time_span)

    def calculate_time(self):
        calculate_time = self.time.strftime("%H:%M")
        return calculate_time
