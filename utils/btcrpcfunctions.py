from imports import *
import variables as v
from formating import *
home = os.getenv("HOME")


def BTCprogress():
    if not (os.path.exists(home + "/.bitcoin")):
        return 0
    response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli getblockchaininfo'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if not (len(response[0]) == 0):
        bitcoinprogress = json.loads(response[0].decode("utf-8"))['verificationprogress']
        bitcoinprogress = bitcoinprogress * 100
        bitcoinprogress = round(bitcoinprogress, 3)
    else:
        bitcoinprogress = 0
    return bitcoinprogress

def BTCFinished():
    if not (os.path.exists(home + "/.bitcoin")):
        return False
    response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli getblockchaininfo'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if not (len(response[0]) == 0):
        bitcoinprogress = json.loads(response[0].decode("utf-8"))['initialblockdownload']
    else:
        bitcoinprogress = True
    return not bitcoinprogress

def BTCClosed():
    if (subprocess.call('lsof -n -i :8332', shell=True) != 1):
        return False
    return True

def BTCRunning():
    if not (BTCprogress() == 0):
        return True
    return False

def blockheight():
    response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli getblockchaininfo'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    Blockinfo = json.loads(response[0].decode("utf-8"))
    blockheight = 0
    if Blockinfo['pruned']:
        blockheight = Blockinfo['pruneheight']
    return str(blockheight)