import subprocess
import os
home = os.getenv("HOME")
subprocess.call(['wget https://bitcoincore.org/bin/bitcoin-core-0.19.0.1/bitcoin-0.19.0.1-x86_64-linux-gnu.tar.gz -P ~/yeticold/'],shell=True)
subprocess.call(['tar xvzf ~/yeticold/bitcoin-0.19.0.1-x86_64-linux-gnu.tar.gz -C ~/yeticold'],shell=True)
subprocess.call(['chmod +x ~/yeticold/utils/verifySig.sh'],shell=True)
subprocess.call(['~/yeticold/utils/verifySig.sh'],shell=True)
if not (os.path.exists(home + "/yeticold/sigcorrect")):
	subprocess.call(['echo "We could not verify the bitcoin core code. This could be from not downloading the signatures or bitcoin core as well as faulty code. Hit [Enter] to ignore and continue'],shell=True)
	subprocess.call(['read line'],shell=True)
subprocess.call(['mv ~/yeticold/bitcoin-0.19.0.1 ~/yeticold/bitcoin'],shell=True)