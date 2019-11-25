import os
import subprocess

subprocess.call('sudo rm -r ~/.bitcoin/yeticold*', shell=True)
subprocess.call('sudo rm -r ~/.bitcoin/yetiwarm*', shell=True)
subprocess.call('sudo rm -r ~/yetiwarmwallet*', shell=True)

subprocess.call('sudo rm -r ~/yeticoldwallet*', shell=True)

subprocess.call('echo "DONE"', shell=True)
