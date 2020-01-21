from i3_battery_block import wrap_span

def test_wrap():
    assert wrap_span("a") == "<span font='FontAwesome'>a</span>", "String should be wraped into span element!"

def test_wrap_with_color():
    assert wrap_span("a", "b") == "<span font='FontAwesome' color='b'>a</span>", "String should be wraped into span element!"
