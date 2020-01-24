
from i3_battery_block.cli import main


def test_main():
    try:
        main([])
    except FileNotFoundError as e:
        # if no acpi is there (ci server) test for correct error message
        assert e.errno == 2 and e.strerror.find('acpi') != -1, "extraordinary failure"
