import pytest

from i3_battery_block.html_formatter import color
from i3_battery_block.html_formatter import wrap_span


def test_wrap():
    assert wrap_span("a") == "<span font='FontAwesome'>a</span>", "String should be wrapped into span element!"


def test_wrap_with_color():
    assert wrap_span("a",
                     "b") == "<span font='FontAwesome' col='b'>a</span>", "String should be wrapped into span " \
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
