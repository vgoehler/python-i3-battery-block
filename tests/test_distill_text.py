from i3_battery_block_vgg.battery import distill_text
from i3_battery_block_vgg.font_awesome_glyphs import FA_NO_BATTERY
from i3_battery_block_vgg.html_formatter import wrap_span


def test_distill_text_empty():
    # this should output text for no battery found
    no_battery = wrap_span(FA_NO_BATTERY, "red")
    expected = (no_battery, no_battery, 100)
    assert distill_text('') == expected, "no battery output should be given"


def test_active_compact_mode():
    # this should output text for no battery found
    text = "Battery 0: Discharging, 77%, 01:40:21 remaining\n" \
           "Battery 0: design capacity 1898 mAh, last full capacity 1837 mAh = 96%\n" \
           "Battery 1: Unknown, 5%\n" \
           "Battery 1: design capacity 1898 mAh, last full capacity 1837 mAh = 96%"
    full, small, avg = distill_text(text, compact=True)
    assert full == small, "in compact mode the full output should be as big as the small output"
