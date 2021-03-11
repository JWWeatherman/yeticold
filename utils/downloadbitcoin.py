import subprocess
import os
home = os.getenv("HOME")
if not os.path.exists(home + "/yeticold/bitcoin"):
	subprocess.call(['wget https://bitcoincore.org/bin/bitcoin-core-0.21.0/bitcoin-0.21.0-x86_64-linux-gnu.tar.gz -P ~/yeticold/'],shell=True)
	subprocess.call(['rm ~/yeticold/sigcorrect 2> /dev/null'],shell=True)
	if not (os.path.exists(home + "/yeticold/SHA256SUMS.asc")):
		subprocess.call(['sudo wget https://bitcoincore.org/bin/bitcoin-core-0.21.0/SHA256SUMS.asc -P ~/yeticold/'],shell=True)
	subprocess.call(['cd ~/yeticold; ./verifySig.sh 2> /dev/null; cd'],shell=True)
	if not (os.path.exists(home + "/yeticold/sigcorrect")):
		subprocess.call(['echo "We could not verify the bitcoin core code. This could be from not downloading the signatures or bitcoin core as well as faulty code. Please go to yeticold.slack.com and paste this message in the support section for help."'],shell=True)
		subprocess.call(['read line'],shell=True)
	else:
		subprocess.call(['echo "Successfully verified the bitcoin core code."'],shell=True)
	subprocess.call(['tar xvzf ~/yeticold/bitcoin-0.21.0-x86_64-linux-gnu.tar.gz -C ~/yeticold'],shell=True)
	subprocess.call(['mv ~/yeticold/bitcoin-0.21.0 ~/yeticold/bitcoin'],shell=True)
	subprocess.call(['chmod +x ~/yeticold/bitcoin/bin/bitcoin-qt'],shell=True)
	subprocess.call(['chmod +x ~/yeticold/bitcoin/bin/bitcoin-cli'],shell=True)
