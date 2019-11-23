import os
import subprocess

subprocess.call('sudo rm -r ~/.bitcoin/yeticold*', shell=True)
subprocess.call('sudo rm -r ~/.bitcoin/yetiwarm*', shell=True)
subprocess.call('sudo rm -r ~/.bitcoin/yetihot*', shell=True)
subprocess.call('echo "DONE"', shell=True)
