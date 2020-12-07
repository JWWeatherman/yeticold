subprocess.run('sudo mount /dev/sdb1 ~/yeticold/usb_drive', shell=True, check=False)
subprocess.run('sudo rm -rf ~/yeticold/usb_drive/*', shell=True, check=False)
subprocess.run('sudo cp -r ~/yeticold/pre_usb_drive ~/yeticold/usb_drive/yeticold')
