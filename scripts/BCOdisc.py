import subprocess
import os
home = os.getenv("HOME")

if not (os.path.exists(home + "/yeticold")) or not (os.path.exists(home + "/.bitcoin")):
	subprocess.call(['cat ~ToDisconnected/ToDisconnected.tar.gz.part* >ToDisconnected.tar.gz'],shell=True)
	subprocess.call(['tar -xzf ToDisconnected.tar.gz'],shell=True)
if not (os.system("python3 -c 'import flask'") == 0):
	subprocess.call(['bash -c "sudo chmod +x ~/yeticold/scripts/dpkg-script.sh; sudo ~/yeticold/scripts/dpkg-script.sh"'],shell=True)
subprocess.call(['sudo chmod +x ~/yeticold/bitcoin/bin/bitcoin-cli'],shell=True)
subprocess.call(['sudo chmod +x ~/yeticold/bitcoin/bin/bitcoind'],shell=True)
subprocess.call(['sudo chmod +x ~/yeticold/bitcoin/bin/bitcoin-qt'],shell=True)
subprocess.call(['sudo chmod +x ~/yeticold/bitcoin/bin/bitcoin-wallet'],shell=True)
subprocess.call(['sudo chmod +x ~/yeticold/bitcoin/bin/bitcoin-tx'],shell=True)
subprocess.call('fuser -k 5000/tcp', shell=True)
subprocess.call('python3 ~/yeticold/utils/stopbitcoin.py', shell=True)
subprocess.Popen('python3 ~/yeticold/BCOffline.py',shell=True,start_new_session=True)
subprocess.call(['xdg-open http://localhost:5000/BCopenbitcoinC'],shell=True)