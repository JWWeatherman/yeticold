"""
This script automates the action of disconnecting the computer from any wireless or cabled networks.
The purpose of this is to disable internet connectivity before generating private keys.
The disabled network (at least the cabled kind) can be restored using `nmcli n on` and rebooting.
Though that is only advised during testing. It is not advised for normal usage.
"""
import subprocess
import os


def forget_networks():
    res = subprocess.Popen("nmcli -t -f TYPE,UUID con", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode("utf-8")
    lines = res.split('\n')
    for line in lines:
        parts = line.split(":")
        if parts[0] == "802-11-wireless":
            os.system("nmcli connection delete uuid " + parts[1])
    subprocess.run('nmcli n off', shell=True, check=False)
    subprocess.run('touch ~/yeticold/connectionOff', shell=True, check=False)

if __name__ == "__main__":
    forget_networks()