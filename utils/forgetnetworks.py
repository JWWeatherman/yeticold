"""
This script automates the action of disconnecting the computer from any wireless or cabled networks.
The purpose of this is to disable internet connectivity before generating private keys.
The disabled network (at least the cabled kind) can be restored using `nmcli n on` and rebooting.
Though that is only advised during testing. It is not advised for normal usage.
"""

import subprocess
import os

def forget_networks():
    # Get list of wireless access points
    res = subprocess.Popen("nmcli -t -f TYPE,UUID con", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode("utf-8")
    # Split the lines by newline character
    lines = res.split('\n')

    # Loop through each line, splitting it by a colon, until a wireless access point is found, then delete it
    for line in lines:
        parts = line.split(":")
        if parts[0] == "802-11-wireless":
            os.system("nmcli connection delete uuid " + parts[1])

    # Disable all networking system wide
    subprocess.call(['nmcli n off'], shell=True)

# If script is run as standalone (not imported) then it will execute the following commands
if __name__ == "__main__":
    forget_networks()
    