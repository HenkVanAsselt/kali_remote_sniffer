# file: channel_hop.py

# Global imports
import os
import time

# Local variables
channel_list = [1,6,11]
wait = 5

# -----------------------------------------------------------------------------
def main() -> None:

    # Loop forever
    while True:

        # Hop over all channels in the given list with at the 'wait' interval
        for channel in channel_list:
           cmd = 'sudo iw dev wlan0mon set channel %d' % channel
           print(cmd)
           os.system(cmd)
           time.sleep(wait)

# =============================================================================
if __name__ == "__main__":
    main()