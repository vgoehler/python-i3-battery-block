from functools import partial

from i3_battery_block_vgg.font_awesome_glyphs import FA_BATTERY_LIST
from i3_battery_block_vgg.font_awesome_glyphs import FA_BUG
from i3_battery_block_vgg.font_awesome_glyphs import FA_LAPTOP
from i3_battery_block_vgg.font_awesome_glyphs import FA_PLUG
from i3_battery_block_vgg.font_awesome_glyphs import FA_QUESTION
from i3_battery_block_vgg.state import State


def wrap_span(text: str, col: str = None, font: str = None, weight: str = None) -> str:
    """
    This wraps a span element around an input text.

    :param weight: string, the weight of the element, numerical or  'ultralight', 'light', 'normal', 'bold',
        'ultrabold', 'heavy'
    :param font: string, the font to use for the span element
    :type text: string, the text that should be wrapped in the span
    :type col: string, a html color string
    """
    color_text = " color='%s'" % col if col else ""
    font_text = " font='%s'" % font if font else ""
    weight_text = " weight='%s'" % weight if weight else ""
    return "<span%s%s%s>%s</span>" % (font_text, color_text, weight_text, text)


wrap_span_fa = partial(wrap_span, font='FontAwesome')
wrap_span_fa.__doc__ = """This behaves like wrap_span but has the font locked to FontAwesome"""


def wrap_span_battery_header(id_nr: int) -> str:
    return wrap_span(str(id_nr), col="#BFBFBF", weight='bold')


def wrap_span_bug():
    return wrap_span_fa(FA_BUG, "orange")


def color(percent: int):
    """
    This returns the appropriate color for a percentage.
    :param percent: An integer value percent representation
    :return: the color according to the __COLOR_MAP constant map
    """
    if percent < 0 or percent > 100:
        raise AttributeError("Threshold %i is out of percent range." % percent)

    # we only need the first number
    deca = percent // 10
    return __COLOR_MAP[deca]


"""
    This Mapping contains the text color for each percent decade.
    as exit code 33 will turn background red 0-9 percent font is white.
"""
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
STATUS_SPANS = {
    State.CHARGING: wrap_span_fa(FA_PLUG, "yellow"),
    State.DISCHARGING: wrap_span_fa(FA_LAPTOP),
    State.UNKNOWN: wrap_span_fa(FA_QUESTION),
    State.FULL: wrap_span_fa(FA_PLUG)
}


def discern_loading_state(percentage: int, color: str = None) -> str:
    """
    returns the appropriate icon for the load
    :param color: an optional color for the span element
    :param percentage: for the load state of the battery
    :return: a span element
    """
    assert percentage in range(0, 101)
    idx = len(FA_BATTERY_LIST) * percentage // 100
    # 100 % produces one not valid entry
    idx = len(FA_BATTERY_LIST) - 1 if idx == len(FA_BATTERY_LIST) else idx
    return wrap_span_fa(FA_BATTERY_LIST[idx], col=color)
