from enum import Enum


class State(Enum):
    UNKNOWN = 'Unknown'
    CHARGING = "Charging"
    DISCHARGING = "Discharging"
    FULL = "Full"

    @staticmethod
    def get_state_according_to_value(value: str) -> Enum:
        """returns a state enum obj according to the given value"""
        return State.__members__.get(value.upper())
