import subprocess
import os

# Change this variable when new versions of Bitcoin Core are released.
BITCOIN_VERSION = '27.0'

BITCOIN_SOURCE_URL = 'https://bitcoincore.org/bin/bitcoin-core-' + BITCOIN_VERSION + '/bitcoin-' + BITCOIN_VERSION + '-x86_64-linux-gnu.tar.gz'
BITCOIN_SOURCE_DIR = os.path.dirname(BITCOIN_SOURCE_URL)
BITCOIN_SOURCE_FILENAME = os.path.basename(BITCOIN_SOURCE_URL)

YETI_DIR = os.getenv('HOME') + '/yeticold'
BITCOIN_EXTRACT_DIR = YETI_DIR + '/bitcoin'

if not os.path.exists(BITCOIN_EXTRACT_DIR):
    subprocess.call(['wget ' + BITCOIN_SOURCE_URL + ' -P ' + YETI_DIR + '/'],shell=True)
    subprocess.call(['[ -f ' + YETI_DIR + '/sigcorrect ] && rm ' + YETI_DIR + '/sigcorrect 2> /dev/null'],shell=True)
    subprocess.call(['[ -f ' + YETI_DIR + '/SHA256SUMS ] && rm ' + YETI_DIR + '/SHA256SUMS 2> /dev/null'],shell=True)
    subprocess.call(['[ -f ' + YETI_DIR + '/SHA256SUMS.asc ] && rm ' + YETI_DIR + '/SHA256SUMS.asc 2> /dev/null'],shell=True)
    subprocess.call(['wget ' + BITCOIN_SOURCE_DIR + '/SHA256SUMS -P ' + YETI_DIR + '/'],shell=True)
    subprocess.call(['wget ' + BITCOIN_SOURCE_DIR + '/SHA256SUMS.asc -P ' + YETI_DIR + '/'],shell=True)
    subprocess.call(['cd ' + YETI_DIR + '; ./verifySig.sh 2> /dev/null; cd'],shell=True)
    if not os.path.exists(YETI_DIR + '/sigcorrect'):
        subprocess.call(['echo "We could not verify the bitcoin core code. This could be from not downloading the signatures or bitcoin core as well as faulty code. Please go to yeticold.slack.com and paste this message in the support section for help."'],shell=True)
        subprocess.call(['read line'],shell=True)
    else:
        subprocess.call(['echo "Successfully verified the bitcoin core code."'],shell=True)
    subprocess.call(['mkdir ' + BITCOIN_EXTRACT_DIR],shell=True)
    subprocess.call(['tar -xvzf ' + YETI_DIR + '/' + BITCOIN_SOURCE_FILENAME + ' -C ' + BITCOIN_EXTRACT_DIR + '/ --strip-components=1'],shell=True)
    subprocess.call(['chmod u+x ' + BITCOIN_EXTRACT_DIR + '/bin/bitcoin-qt'],shell=True)
    subprocess.call(['chmod u+x ' + BITCOIN_EXTRACT_DIR + '/bin/bitcoin-cli'],shell=True)
