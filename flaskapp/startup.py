import os
import subprocess
home = os.getenv("HOME")
if not (os.path.exists(home + "/flaskapp")):
	subprocess.call(['wget https://github.com/JWWeatherman/yeti/files/3698150/flaskapp.zip -P ~/'],shell=True)
	subprocess.call(['unzip ~/flaskapp.zip -d ~/'],shell=True)

subprocess.call(['sudo apt-get update'],shell=True)
subprocess.call(['sudo apt-get install python3-venv'],shell=True)
subprocess.call(['sudo apt-get install python3-pip'],shell=True)
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

if not (os.path.exists(home + "/flaskapp/bitcoin-0.18.1/bin")):
	subprocess.call(['sudo unattended-upgrade'],shell=True)
	subprocess.call(['wget https://bitcoin.org/bin/bitcoin-core-0.18.1/bitcoin-0.18.1-x86_64-linux-gnu.tar.gz -P ~/flaskapp/'],shell=True)
	subprocess.call(['tar xvzf ~/flaskapp/bitcoin-0.18.1-x86_64-linux-gnu.tar.gz -C ~/flaskapp'],shell=True)
	subprocess.call(['sudo apt install apt-transport-https curl'],shell=True)
	subprocess.call(['sudo -i echo "deb https://deb.torproject.org/torproject.org/ $(lsb_release -cs) main" > /etc/apt/sources.list.d/tor.list'],shell=True)
	subprocess.call(['sudo -i curl https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc | gpg --import'],shell=True)
	subprocess.call(['sudo -i gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | apt-key add -'],shell=True)
	subprocess.call(['sudo apt update'],shell=True)
	subprocess.call(['sudo apt install tor tor-geoipdb torsocks deb.torproject.org-keyring'],shell=True)




subprocess.Popen('python3 ~/flaskapp/hello.py',shell=True,start_new_session=True)
subprocess.call(['xdg-open http://localhost:5000'],shell=True)
