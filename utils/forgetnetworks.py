import subprocess
import os

res = subprocess.Popen("nmcli -t -f TYPE,UUID con",shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode("utf-8")
lines = res.split('\n')

for line in lines:
    parts = line.split(":")
    if (parts[0] == "802-11-wireless"):
        os.system("nmcli connection delete uuid "+ parts[1])

