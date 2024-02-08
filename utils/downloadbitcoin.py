import subprocess
import os

BitcoinCoreURL = 'https://bitcoincore.org/bin/bitcoin-core-26.0/bitcoin-26.0-x86_64-linux-gnu.tar.gz'
BitcoinCorePath = os.path.dirname(BitcoinCoreURL)
BitcoinCoreFile = os.path.basename(BitcoinCoreURL)

YetiDir = os.getenv("HOME") + '/yeticold'
BitcoinExtractDir = YetiDir + '/bitcoin'

if not os.path.exists(BitcoinExtractDir):
	subprocess.call(['wget ' + BitcoinCoreURL + ' -P ' + YetiDir + '/'],shell=True)
	subprocess.call(['[ -f ' + YetiDir + '/sigcorrect ] && rm ' + YetiDir + '/sigcorrect 2> /dev/null'],shell=True)
	subprocess.call(['[ -f ' + YetiDir + '/SHASUMS.asc ] && rm ' + YetiDir + '/SHA256SUMS.asc 2> /dev/null'],shell=True)
	subprocess.call(['wget ' + BitcoinCorePath + '/SHA256SUMS -P ' + YetiDir + '/'],shell=True)
	subprocess.call(['wget ' + BitcoinCorePath + '/SHA256SUMS.asc -P ' + YetiDir + '/'],shell=True)
	subprocess.call(['cd ' + YetiDir + '; ./verifySig.sh 2> /dev/null; cd'],shell=True)
	if not (os.path.exists(YetiDir + '/sigcorrect')):
		subprocess.call(['echo "We could not verify the bitcoin core code. This could be from not downloading the signatures or bitcoin core as well as faulty code. Please go to yeticold.slack.com and paste this message in the support section for help."'],shell=True)
		subprocess.call(['read line'],shell=True)
	else:
		subprocess.call(['echo "Successfully verified the bitcoin core code."'],shell=True)
	subprocess.call(['mkdir ' + BitcoinExtractDir],shell=True)
	subprocess.call(['tar -xvzf ' + YetiDir + '/' + BitcoinCoreFile + ' -C ' + BitcoinExtractDir + '/ --strip-components=1'],shell=True)
	subprocess.call(['chmod u+x ' + BitcoinExtractDir + '/bin/bitcoin-qt'],shell=True)
	subprocess.call(['chmod u+x ' + BitcoinExtractDir + '/bin/bitcoin-cli'],shell=True)
