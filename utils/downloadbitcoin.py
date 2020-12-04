import subprocess
import os
home = os.getenv("HOME")
if not os.path.exists(home + "/yeticold/bitcoin"):
	subprocess.call(['wget https://bitcoincore.org/bin/bitcoin-core-0.21.0/test.rc2/bitcoin-0.21.0rc2-x86_64-linux-gnu.tar.gz -P ~/yeticold/'],shell=True)
subprocess.call(['chmod +x ~/yeticold/verifySig.sh'],shell=True)
if (os.path.exists(home + "/yeticold/sigcorrect")):
	subprocess.call(['rm ~/yeticold/sigcorrect'],shell=True)
if not (os.path.exists(home + "/yeticold/SHA256SUMS.asc")):
	subprocess.call(['sudo wget https://bitcoincore.org/bin/bitcoin-core-0.21.0/test.rc2/SHA256SUMS.asc -P ~/yeticold/'],shell=True)
subprocess.call(['cd ~/yeticold; ./verifySig.sh 2> /dev/null; cd'],shell=True)
if not (os.path.exists(home + "/yeticold/sigcorrect")):
	subprocess.call(['echo "We could not verify the bitcoin core code. This could be from not downloading the signatures or bitcoin core as well as faulty code. Hit [Enter] to ignore and continue"'],shell=True)
	subprocess.call(['read line'],shell=True)
else
	subprocess.call(['echo "Successfully verify the bitcoin core code."'],shell=True)
if not os.path.exists(home + "/yeticold/bitcoin"):
	subprocess.call(['tar xvzf ~/yeticold/bitcoin-0.21.0rc2-x86_64-linux-gnu.tar.gz -C ~/yeticold'],shell=True)
	subprocess.call(['mv ~/yeticold/bitcoin-0.21.0rc2 ~/yeticold/bitcoin'],shell=True)
	subprocess.call(['chmod +x ~/yeticold/bitcoin/bin/bitcoin-qt'],shell=True)
	subprocess.call(['chmod +x ~/yeticold/bitcoin/bin/bitcoin-cli'],shell=True)
