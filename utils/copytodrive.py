import subprocess
import os
home = os.getenv("HOME")

subprocess.run('sudo mount /dev/sdc1 ~/yeticold/usb_drive', shell=True, check=False)
subprocess.run('sudo rm -rf ~/yeticold/usb_drive/*', shell=True, check=False)
subprocess.run('sudo cp -r '+home+'/yeticold/pre_usb_drive/* '+home+'/yeticold/usb_drive/')
subprocess.run('sudo eject /dev/sdc1', shell=True, check=False)

