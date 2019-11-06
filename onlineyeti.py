import os
import subprocess
home = os.getenv("HOME")
subprocess.call(['sudo apt-get update'],shell=True)
if not (os.path.exists(home + "/yeticold")):
	subprocess.call(['sudo apt-get install git'],shell=True)
	subprocess.call(['git clone https://github.com/JWWeatherman/yeticold.git ~/yeticold'],shell=True)

subprocess.call(['sudo apt-get install python3-venv'],shell=True)
subprocess.call(['sudo apt-get install python3-pip'],shell=True)
subprocess.call(['sudo apt-get install libzbar0'],shell=True)
subprocess.call(['sudo apt install tor'],shell=True)
subprocess.call(['sudo pip3 install python-bitcoinrpc'],shell=True)
subprocess.call(['sudo pip3 install flask'],shell=True)

subprocess.call(['pip3 install opencv-python'],shell=True)
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
	

if not (os.path.exists(home + "/yeticold/bitcoin-0.19.0rc1/bin")):
	subprocess.call(['echo "unattended-upgrade"'],shell=True)
	subprocess.call(['sudo unattended-upgrade'],shell=True)
	subprocess.call(['wget https://bitcoincore.org/bin/bitcoin-core-0.19.0/test.rc1/bitcoin-0.19.0rc1-x86_64-linux-gnu.tar.gz -P ~/yeticold/'],shell=True)
	os.system('tar xvzf ~/yeticold/bitcoin-0.19.0rc1-x86_64-linux-gnu.tar.gz -C ~/yeticold')

subprocess.Popen('python3 ~/yeticold/hello.py',shell=True,start_new_session=True)
subprocess.call(['xdg-open http://localhost:5000'],shell=True)
