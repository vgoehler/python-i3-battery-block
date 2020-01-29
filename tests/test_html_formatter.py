import pytest

from i3_battery_block_vgg.font_awesome_glyphs import FA_BATTERY_LIST
from i3_battery_block_vgg.html_formatter import color
from i3_battery_block_vgg.html_formatter import discern_loading_state
from i3_battery_block_vgg.html_formatter import wrap_span
from i3_battery_block_vgg.html_formatter import wrap_span_fa


def test_wrap():
    assert wrap_span("a") == "<span>a</span>", "String should be wrapped into span element!"


def test_wrap_fa():
    assert wrap_span_fa("a") == "<span font='FontAwesome'>a</span>", "String should be wrapped into span element!"


def test_wrap_with_color():
    assert wrap_span("a", "b") == "<span color='b'>a</span>", "String should be wrapped into span element!"


def test_wrap_fa_with_color():
    assert wrap_span_fa("a",
                        "b") == "<span font='FontAwesome' color='b'>a</span>", "String should be wrapped into span " \
                                                                             "element! "


@pytest.mark.parametrize(
    "smaller_then, expected",
    [
        (10, "#FFFFFF"),
        (20, "#FF3300"),
        (30, "#FF6600"),
        (40, "#FF9900"),
        (50, "#FFCC00"),
        (60, "#FFFF00"),
        (70, "#FFFF33"),
        (80, "#FFFF66"),
        (100, "#FFFFFF")
    ]
)
def test_color(smaller_then: int, expected: str):
    assert color(smaller_then - 1) == expected, "below threshold %s color %s is expected" % (smaller_then, expected)


@pytest.mark.parametrize(
    "not_percentage",
    [
        -50, 150,
    ]
)
def test_color_percentage_over_stepped(not_percentage):
    with pytest.raises(AttributeError, match=r'Threshold.*'):
        color(not_percentage)


@pytest.mark.parametrize(
    "percentage, icon",
    [
        (0, FA_BATTERY_LIST[0]),
        (9, FA_BATTERY_LIST[0]),
        (25, FA_BATTERY_LIST[1]),
        (50, FA_BATTERY_LIST[2]),
        (75, FA_BATTERY_LIST[3]),
        (95, FA_BATTERY_LIST[4]),
        (100, FA_BATTERY_LIST[4])
    ]
)
def test_correct_icon(percentage, icon):
    assert discern_loading_state(percentage).find(icon) != -1, "glyph should be in string"
