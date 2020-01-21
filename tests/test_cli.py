from i3_battery_block import cli

def smoke_test_compact():
    cli.main(['-c'])

def smoke_test_loglevel():
    cli.main(['-l warning'])
