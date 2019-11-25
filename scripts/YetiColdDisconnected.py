import subprocess
import os

if not (os.system("python3 -c 'import flask'") == 0):
	subprocess.call(['bash -c "sudo chmod +x ~/yeticold/scripts/dpkg-script.sh; sudo ~/yeticold/scripts/dpkg-script.sh"'],shell=True)
subprocess.call(['sudo chmod +x ~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli'],shell=True)
subprocess.call(['sudo chmod +x ~/yeticold/bitcoin-0.19.0rc1/bin/bitcoind'],shell=True)
subprocess.call(['sudo chmod +x ~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-qt'],shell=True)
subprocess.call(['sudo chmod +x ~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-wallet'],shell=True)
subprocess.call(['sudo chmod +x ~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-tx'],shell=True)
subprocess.call('sudo rm -r ~/.bitcoin/yeticold*', shell=True)
subprocess.call('sudo rm -r ~/yeticoldwallet*', shell=True)
subprocess.Popen('python3 ~/yeticold/appyeticold.py',shell=True,start_new_session=True)
subprocess.call(['xdg-open http://localhost:5000/step15'],shell=True)
