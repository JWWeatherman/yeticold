import subprocess
import os

BitcoinCoreURL = 'https://bitcoincore.org/bin/bitcoin-core-26.0/bitcoin-26.0-x86_64-linux-gnu.tar.gz'
BitcoinCorePath = os.path.dirname(BitcoinCoreURL)
BitcoinCoreFile = os.path.basename(BitcoinCoreURL)

home = os.getenv("HOME")
if not os.path.exists(home + "/yeticold/bitcoin"):
	subprocess.call(['wget ' + BitcoinCoreURL + ' -P ~/yeticold/'],shell=True)
	subprocess.call(['[ -f ~/yeticold/sigcorrect ] && rm ~/yeticold/sigcorrect 2> /dev/null'],shell=True)
	subprocess.call(['[ -f ~/yeticold/SHASUMS.asc ] && rm ~/yeticold/SHA256SUMS.asc 2> /dev/null'],shell=True)
	subprocess.call(['wget ' + BitcoinCorePath + '/SHA256SUMS -P ~/yeticold/'],shell=True)
	subprocess.call(['wget ' + BitcoinCorePath + '/SHA256SUMS.asc -P ~/yeticold/'],shell=True)
	subprocess.call(['cd ~/yeticold; ./verifySig.sh 2> /dev/null; cd'],shell=True)
	if not (os.path.exists(home + "/yeticold/sigcorrect")):
		subprocess.call(['echo "We could not verify the bitcoin core code. This could be from not downloading the signatures or bitcoin core as well as faulty code. Please go to yeticold.slack.com and paste this message in the support section for help."'],shell=True)
		subprocess.call(['read line'],shell=True)
	else:
		subprocess.call(['echo "Successfully verified the bitcoin core code."'],shell=True)
	subprocess.call(['mkdir ~/yeticold/bitcoin'],shell=True)
	subprocess.call(['tar -xvzf ~/yeticold/' + BitcoinCoreFile + ' -C ~/yeticold/bitcoin/ --strip-components=1'],shell=True)
	subprocess.call(['chmod u+x ~/yeticold/bitcoin/bin/bitcoin-qt'],shell=True)
	subprocess.call(['chmod u+x ~/yeticold/bitcoin/bin/bitcoin-cli'],shell=True)
