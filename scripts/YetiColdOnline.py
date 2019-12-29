import os
import subprocess
home = os.getenv("HOME")


subprocess.call(['cd ~/yeticold; git pull; cd'],shell=True)
subprocess.call('fuser -k 5000/tcp', shell=True)

	
if not (os.path.exists(home + "/yeticold/bitcoin")):
	subprocess.call(['sudo apt-get install python3-venv'],shell=True)
	subprocess.call(['sudo apt-get install python3-pip'],shell=True)
	subprocess.call(['sudo apt-get install libzbar0'],shell=True)
	subprocess.call(['sudo apt install tor'],shell=True)
	subprocess.call(['sudo pip3 install python-bitcoinrpc'],shell=True)
	subprocess.call(['pip3 install opencv-python'],shell=True)
	subprocess.call(['sudo apt-get update'],shell=True)
	subprocess.call(['echo "Installing updates. This could take an hour without feedback."'],shell=True)
	subprocess.call(['sudo unattended-upgrade'],shell=True)
	subprocess.call(['python3 ~/yeticold/utils/downloadbitcoin.py'],shell=True)
if not (os.path.exists(home + "/.bitcoin")):
	subprocess.call(['wsh https://drive.google.com/uc?authuser=0&id=1qjsuk1mllQMcWKmWZXhDQ9eRL7hL7aLA&export=download'],shell=True)
	subprocess.call(['tar -xzf .bitcoin.tar.gz'],shell=True)
if not (os.system("python3 -c 'import flask'") == 0):
	subprocess.call(['pip3 install flask'],shell=True)
if not (os.system("python3 -c 'import qrtools'") == 0):
	subprocess.call(['pip3 install qrtools'],shell=True)
if not (os.system("python3 -c 'import qrcode'") == 0):
	subprocess.call(['pip3 install qrcode'],shell=True)
if not (os.system("python3 -c 'import pyzbar'") == 0): 
	subprocess.call(['pip3 install pyzbar'],shell=True)
if not (os.system("python3 -c 'import PIL'") == 0):
	subprocess.call(['pip3 install pillow'],shell=True)
if not (os.system("python3 -c 'import zbar'") == 0):
	subprocess.call(['pip3 install zbar-py'],shell=True)
subprocess.call('python3 ~/yeticold/utils/stopbitcoin.py', shell=True)
subprocess.call('sudo rm -r ~/.bitcoin/yeticold*', shell=True)
subprocess.call('sudo rm -r ~/yetihotwallet*', shell=True)
subprocess.call('sudo rm -r ~/yetiwarmwallet*', shell=True)
subprocess.call('sudo rm -r ~/yeticoldwallet*', shell=True)
subprocess.Popen('python3 ~/yeticold/appyeticold.py',shell=True,start_new_session=True)
subprocess.call(['xdg-open http://localhost:5000/YConlinestartup'],shell=True)