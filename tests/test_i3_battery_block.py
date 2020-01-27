
from i3_battery_block_vgg.cli import main


def test_main():
    try:
        main([])
    except FileNotFoundError as e:
        # if no acpi is there (ci server) test for correct error message
        assert e.errno == 2, "extraordinary failure"
