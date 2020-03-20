import datetime
from typing import Dict
from typing import List

from i3_battery_block_vgg.html_formatter import wrap_span

FORMAT = "%H:%M"
INVALID = 1000000


class battery_timer:

    def __init__(self):
        self.capacities: List[int] = []
        self.time: datetime.time = datetime.time()
        self.battery_nr_for_time: int = INVALID  # give it a value that will raise a key error
        self.battery_counter: int = -1  # as we increment first in the method we want a 0
        self.percentages: List[float] = []

    @property
    def time_is_set(self) -> bool:
        return self.time != datetime.time()

    def set_timer(self, battery: Dict) -> None:
        self.battery_counter += 1

        # if we get a battery time set it, acpi output only specifies one "time"
        if not self.time_is_set and battery['time']:
            self.time = battery['time']
            self.battery_nr_for_time = self.battery_counter

        if battery['full_capacity']:
            self.capacities.append(battery['full_capacity'])

        self.percentages.append(battery['percentage'] / 100)

    def output_timer(self, full_text: List[str], small_text: [str]) -> None:
        if self.time_is_set:
            time_span = wrap_span("(%s)" % self.calculate_time())
            full_text.append(time_span)
            small_text.append(time_span)

    def calculate_time(self):
        # if only one battery is there we don't need to calculate all the stuff
        if len(self.capacities) == 1:
            return self.time.strftime(FORMAT)

        # time [in minutes] to capacity of this nr as x to whole capacity
        # capacity means the capacity left in the battery (percentage * last_known_percentage)
        sum_capacity = sum([cap * perc for cap, perc in zip(self.capacities, self.percentages)])
        time_in_minutes = self.time.hour * 60 + self.time.minute
        modified_capacity_for_time_nr = \
            self.capacities[self.battery_nr_for_time] * self.percentages[self.battery_nr_for_time]
        calculated_minutes = int(time_in_minutes * sum_capacity / modified_capacity_for_time_nr)

        # now we need to calculate hours and minutes in the result above
        calc_hour = calculated_minutes // 60
        calc_rest_mins = calculated_minutes % 60
        try:
            return datetime.time(hour=calc_hour, minute=calc_rest_mins).strftime(FORMAT)
        except ValueError:  # gets raised in case hours is out of 0..23
            return "> 1 day"

    def calculate_avg_percentage(self) -> int:
        if len(self.percentages) == 0:
            # in case we got no percentages return zero
            return 0
        percentage_sum: int = sum([perc * 100 for perc in self.percentages])
        relevant_battery_count: int = len(self.percentages)
        return int(percentage_sum // relevant_battery_count)
