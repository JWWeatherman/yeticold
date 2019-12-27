from flask import Flask, render_template, redirect, url_for, request
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import hashlib
import os
import subprocess
import json
import cv2
from qrtools.qrtools import QR
from pyzbar.pyzbar import decode
from PIL import Image
import random
import qrcode
from datetime import datetime
import time
app = Flask(__name__)
home = os.getenv("HOME")
rpcpsw = str(random.randrange(0,1000000))
blockchain = False
if not (os.path.exists(home + "/.bitcoin")):
    blockchain = True
    subprocess.call(['mkdir ~/.bitcoin'],shell=True)
else:
    subprocess.call(['rm ~/.bitcoin/bitcoin.conf'],shell=True)
subprocess.call('echo "server=1\nrpcport=8332\nrpcuser=rpcuser\nprune=550\nrpcpassword='+rpcpsw+'" >> '+home+'/.bitcoin/bitcoin.conf', shell=True)

### VARIBALES START
settings = {"rpc_username": "rpcuser","rpc_password": rpcpsw,"rpc_host": "127.0.0.1","rpc_port": 8332,"address_chunk": 100}
wallet_template = "http://{rpc_username}:{rpc_password}@{rpc_host}:{rpc_port}/wallet/{wallet_name}"
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
base_count = len(BASE58_ALPHABET)
privkeylist = []
xprivlist = []
error = None
qrdata = None
privkeycount = 0
receipentaddress = None
qrcodescanning = None
pubdesc = None
progress = 0
switcher = {
    "1": "ONE",
    "2": "TWO",
    "3": "THREE",
    "4": "FOUR",
    "5": "FIVE",
    "6": "SIX",
    "7": "SEVEN",
    "8": "EIGHT",
    "9": "NINE",
    "A": "ALFA",
    "B": "BRAVO",
    "C": "CHARLIE",
    "D": "DELTA",
    "E": "ECHO",
    "F": "FOXTROT",
    "G": "GOLF",
    "H": "HOTEL",
    "I": "INDIA",
    "J": "JULIETT",
    "K": "KILO",
    "L": "LIMA",
    "M": "MIKE",
    "N": "NOVEMBER",
    "O": "OSCAR",
    "P": "PAPA",
    "Q": "QUEBEC",
    "R": "ROMEO",
    "S": "SIERRA",
    "T": "TANGO",
    "U": "UNIFORM",
    "V": "VICTOR",
    "W": "WHISKEY",
    "X": "X-RAY",
    "Y": "YANKEE",
    "Z": "ZULU",
    "a": "alfa",
    "b": "bravo",
    "c": "charlie",
    "d": "delta",
    "e": "echo",
    "f": "foxtrot",
    "g": "golf",
    "h": "hotel",
    "i": "india",
    "j": "juliett",
    "k": "kilo",
    "l": "lima",
    "m": "mike",
    "n": "november",
    "o": "oscar",
    "p": "papa",
    "q": "quebec",
    "r": "romeo",
    "s": "sierra",
    "t": "tango",
    "u": "uniform",
    "v": "victor",
    "w": "whiskey",
    "x": "x-ray",
    "y": "yankee",
    "z": "zulu",
    "ONE": "1",
    "TWO": "2",
    "THREE": "3",
    "FOUR": "4",
    "FIVE": "5",
    "SIX": "6",
    "SEVEN": "7",
    "EIGHT": "8",
    "NINE": "9",
    "ALFA": "A",
    "BRAVO": "B",
    "CHARLIE": "C",
    "DELTA": "D",
    "ECHO": "E",
    "FOXTROT": "F",
    "GOLF": "G",
    "HOTEL": "H",
    "INDIA": "I",
    "JULIETT": "J",
    "KILO": "K",
    "LIMA": "L",
    "MIKE": "M",
    "NOVEMBER": "N",
    "OSCAR": "O",
    "PAPA": "P",
    "QUEBEC": "Q",
    "ROMEO": "R",
    "SIERRA": "S",
    "TANGO": "T",
    "UNIFORM": "U",
    "VICTOR": "V",
    "WHISKEY": "W",
    "X-RAY": "X",
    "YANKEE": "Y",
    "ZULU": "Z",
    "alfa": "a",
    "bravo": "b",
    "charlie": "c",
    "delta": "d",
    "echo": "e",
    "foxtrot": "f",
    "golf": "g",
    "hotel": "h",
    "india": "i",
    "juliett": "j",
    "kilo": "k",
    "lima": "l",
    "mike": "m",
    "november": "n",
    "oscar": "o",
    "papa": "p",
    "quebec": "q",
    "romeo": "r",
    "sierra": "s",
    "tango": "t",
    "uniform": "u",
    "victor": "v",
    "whiskey": "w",
    "x-ray": "x",
    "yankee": "y",
    "zulu": "z"
}
### VARIBALES STOP

#create a universal page for initial block download and automaticly move user on after its finished and display progress if not





### FUNCTIONS START

def BTCprogress():
    response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli getblockchaininfo'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if not (len(response[0]) == 0):
        bitcoinprogress = json.loads(response[0])['verificationprogress']
        bitcoinprogress = bitcoinprogress * 100
        bitcoinprogress = round(bitcoinprogress, 3)
    else:
        bitcoinprogress = 0
    return bitcoinprogress

def BTCFinished():
    response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli getblockchaininfo'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if not (len(response[0]) == 0):
        bitcoinprogress = json.loads(response[0])['initialblockdownload']
    else:
        bitcoinprogress = True
    return bitcoinprogress

def BTCClosed():
    home = os.getenv("HOME")
    if (subprocess.call('lsof -n -i :8332', shell=True) != 1):
        return False
    elif os.path.exists(home + "/.bitcoin/bitcoind.pid"):
        subprocess.call('rm -r ~/.bitcoin/bitcoind.pid', shell=True)
    return True

def BTCRunning():
    if not (BTCprogress() == 0):
        return True
    return False

def RPC():
    name = 'username'
    wallet_name = ''
    uri = wallet_template.format(**settings, wallet_name=wallet_name)
    rpc = AuthServiceProxy(uri, timeout=600)  # 1 minute timeout
    return rpc

def encode_base58(s):
    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break
    num = int.from_bytes(s, 'big')
    prefix = '1' * count
    result = ''
    while num > 0:
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result
    return prefix + result

def decode_base58(s):
    decoded = 0
    multi = 1
    s = s[::-1]
    for char in s:
        decoded += multi * BASE58_ALPHABET.index(char)
        multi = multi * base_count
    return decoded

def hash256(s):
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()

def wif(pk):
    prefix = b"\x80"
    suffix = b'\x01'
    extended_key = prefix + pk + suffix
    assert(len(extended_key) == 33 or len(extended_key) == 34)
    final_key = extended_key + hash256(extended_key)[:4]
    WIF = encode_base58(final_key)
    return WIF

def padhex(hex):
    if len(hex) == 64:
        return hex
    else:
        return padhex('0' + hex)

def BinaryToWIF(binary):
    assert(len(binary) == 256)
    key = hex(int(binary, 2)).replace('0x', "")
    padkey = padhex(key)
    assert(int(padkey, 16) == int(key,16))
    return wif(bytes.fromhex(padkey))

def PassphraseListToWIF(passphraselist):
    Privkey = ''
    for i in range(len(passphraselist)):
        Privkey += switcher.get(str(passphraselist[i]))
    return Privkey

def WIFToPassphraseList(privkeywif):
    passphraselist = []
    for i in range(len(privkeywif)):
        passphraselist.append(switcher.get(str(privkeywif[i])))
    return passphraselist

def xor(x, y):
    return '{1:0{0}b}'.format(len(x), int(x, 2) ^ int(y, 2))

### FUNCTIONS STOP

@app.route("/", methods=['GET', 'POST'])
def redirectroute():
    if request.method == 'GET':
        return redirect('/YHblockchain')
    return render_template('redirect.html')

@app.route("/YHblockchain", methods=['GET', 'POST'])
def YHblockchain():
    global blockchain
    if request.method == 'GET':
        home = os.getenv("HOME")
        if blockchain:
            return redirect('/YHopenbitcoin')
    if request.method == 'POST':
        if request.form['option'] == 'downloadblockchain':
            ###ISSUE function needed and a file hosted
            subprocess.call(['wsh a crap bitcoin file'],shell=True)
        else:
            ###ISSUE caculate blocks to prune with 10% buffer
            fmt = '%Y-%m-%d %H:%M:%S'
            d1 = datetime.strptime(request.form['date'] + '12:0:0', fmt)
            d2 = datetime.strptime(str(datetime.today()), fmt)
            d1_ts = time.mktime(d1.timetuple())
            d2_ts = time.mktime(d2.timetuple())
            diff = (int(d2_ts-d1_ts) / 60) / 10
            add = diff / 10
            blockheight = diff + add
            home = os.getenv("HOME")
            subprocess.call(['rm ~/.bitcoin/bitcoin.conf'],shell=True)
            subprocess.call('echo "server=1\nrpcport=8332\nrpcuser=rpcuser\nprune='+blockheight+'\nrpcpassword='+rpcpsw+'" >> '+home+'/.bitcoin/bitcoin.conf', shell=True)
        return redirect('/YHopenbitcoin')
    ###ISSUE template needed
    return render_template('YHblockchain.html')

#finish open bitcoin
@app.route("/YHopenbitcoin", methods=['GET', 'POST'])
def YHopenbitcoin():
    global progress
    if request.method == 'GET':
        home = os.getenv("HOME")
        if BTCClosed():
            subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        progress = BTCprogress()
    if request.method == 'POST':
        if progress >= 99.9:
            return redirect('/YHmenu')
        else:
            return redirect('/YHopenbitcoin')
    return render_template('YHopenbitcoin.html', progress=progress)

@app.route("/YHmenu", methods=['GET', 'POST'])
def YHmenu():
    if request.method == 'POST':
        subprocess.call('python3 ~/yeticold/utils/stopbitcoin.py', shell=True)
        if request.form['option'] == 'recovery':
            return redirect('/YHRrestartbitcoin')
        else:
            return redirect('/YHrestartbitcoin')
    return render_template('YHmenu.html')

#finish open bitcoin
@app.route("/YHrestartbitcoin", methods=['GET', 'POST'])
def YHrestartbitcoin():
    global progress
    if request.method == 'GET':
        home = os.getenv("HOME")
        if BTCClosed():
            subprocess.call('rm -r ~/.bitcoin/yetihot*', shell=True)
            subprocess.call('rm -r ~/yetihotwallet*', shell=True)
            subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        progress = BTCprogress()
    if request.method == 'POST':
        IBD = BTCRunning()
        if IBD:
            response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetiwarmpriv"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            return redirect('/YHgetseed')
        else:
            return redirect('/YHrestartbitcoin')
    return render_template('YHrestartbitcoin.html')

#randomise priv key and get xprivs
@app.route("/YHgetseed", methods=['GET', 'POST'])
def YHgetseed():
    global privkey
    global xpriv
    global pubdesc
    if request.method == 'POST':
        if request.form['skip'] == 'skip':
            newbinary = '1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
        else:
            newbinary = request.form['binary']
        rpc = RPC()
        adr = rpc.getnewaddress()
        newprivkey = rpc.dumpprivkey(adr)
        binary = bin(decode_base58(newprivkey))[2:][8:-40]
        privkey = BinaryToWIF(xor(binary,newbinary))
        home = os.getenv('HOME')
        path = home + '/yetihotwallet'
        subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetihot"','~/yeticold/bitcoin/bin/bitcoin-cli loadwallet "yetihot"'],shell=True)
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetihot sethdseed true "'+privkey+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return redirect('/YHdisplayseed')
    return render_template('YHgetseed.html')
#display seeds
@app.route('/YHdisplayseed', methods=['GET', 'POST'])
def YHdisplayseed():
    global privkey
    global privkeycount
    if request.method == 'GET':
        passphraselist = WIFToPassphraseList(privkey)
    if request.method == 'POST':
        home = os.getenv('HOME')
        path = home + '/Documents'
        subprocess.call('rm '+path+'/yhseed.txt', shell=True)
        subprocess.call('touch '+path+'/yhseed.txt', shell=True)
        file = ''
        for i in range(0,13):
            file = file + request.form['displayrow' + str(i+1)] + '\n'
        subprocess.call('echo "'+file+'" >> '+path+'/yhseed.txt', shell=True)
        return redirect('/YHcheckseed')
    return render_template('YHdisplayseed.html', PPL=passphraselist)
#confirm privkey
@app.route('/YHcheckseed', methods=['GET', 'POST'])
def YHcheckseed():
    global privkey
    global xpriv
    global error
    if request.method == 'POST':
        passphraselist = WIFToPassphraseList(privkey)
        privkeylisttoconfirm = []
        for i in range(1,14):
            inputlist = request.form['row' + str(i)]
            inputlist = inputlist.split(' ')
            inputlist = inputlist[0:4]
            privkeylisttoconfirm.append(inputlist[0])
            privkeylisttoconfirm.append(inputlist[1])
            privkeylisttoconfirm.append(inputlist[2])
            privkeylisttoconfirm.append(inputlist[3])
        if privkeylisttoconfirm == passphraselist:
            return redirect('/YHcopyseed')
        else:
            error = 'You enterd the private key incorrectly but the checksums are correct please try agian. This means you probably inputed a valid seed, but not your seed.'
    return render_template('YHcheckseed.html', x=privkeycount + 1, error=error,i=privkeycount + 35 )
#store USB drives
@app.route("/YHcopyseed", methods=['GET', 'POST'])
def YHcopyseed():
    if request.method == 'POST':
        return redirect('/YHwalletinstructions')
    return render_template('YHcopyseed.html')

@app.route('/YHwalletinstructions', methods=['GET', 'POST'])
def YHwalletinstructions():
    global qrdata
    global error
    if request.method == 'POST':
        error = None
        qrdata = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        qrdata = qrdata.decode("utf-8").replace('\n', '')
        if (qrdata.split(':')[0] == 'bitcoin'):
            qrdata = qrdata.split(':')[1].split('?')[0]
        if (qrdata[:3] == 'bc1') or (qrdata[:1] == '3') or (qrdata[:1] == '1'):
            if not (len(qrdata) >= 26) and (len(qrdata) <= 35):
                error = qrdata + ' is not a valid bitcoin address, address should have a length from 26 to 35 instead of ' + str(len(qrdata)) + '.'
        else: 
            error = qrdata + ' is not a valid bitcoin address, address should have started with bc1, 3 or 1 instead of ' + qrdata[:1] + ', or ' + qrdata[:3] + '.'
        if error:
            qrdata = None
        return redirect('/YHwalletinstructions')
    return render_template('YHwalletinstructions.html', error=error, qrdata=qrdata)
#STOP SET UP-----------------------------------------------------------------------------------------------------------------------------------------------------

#finish open bitcoin
@app.route("/YHRrestartbitcoin", methods=['GET', 'POST'])
def YHRrestartbitcoin():
    global progress
    if request.method == 'GET':
        home = os.getenv("HOME")
        if BTCClosed():
            subprocess.call('rm -r ~/.bitcoin/yetihot*', shell=True)
            subprocess.call('rm -r ~/yetihotwallet*', shell=True)
            subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        progress = BTCprogress()
    if request.method == 'POST':
        IBD = BTCRunning()
        if IBD:
            response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetiwarmpriv"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            return redirect('/YHRinputseed')
        else:
            return redirect('/YHRrestartbitcoin')
    return render_template('YHRrestartbitcoin.html')
    
@app.route('/YHRinputseed', methods=['GET', 'POST'])
def YHRinputseed():
    global error 
    if request.method == 'POST':
        privkey = []
        for i in range(1,14):
            inputlist = request.form['row' + str(i)]
            inputlist = inputlist.split(' ')
            inputlist = inputlist[0:4]
            privkey.append(inputlist[0])
            privkey.append(inputlist[1])
            privkey.append(inputlist[2])
            privkey.append(inputlist[3])
        privkey = PassphraseListToWIF(privkey)
        error = None
        rpc = RPC()
        subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetihot" false true'],shell=True)
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetihot sethdseed true "'+privkey+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return redirect('/YHRwalletinstructions')
    return render_template('YHRinputseed.html', error=error)

@app.route('/YHRwalletinstructions', methods=['GET', 'POST'])
def YHRwalletinstructions():
    global qrdata
    global error
    global qrcodescanning
    if request.method == 'GET':
        if not qrcodescanning:
            qrcodescanning = False
            subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetihot rescanblockchain 600000',shell=True,start_new_session=True)
    if request.method == 'POST':
        error = None
        qrdata = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        qrdata = qrdata.decode("utf-8").replace('\n', '')
        if (qrdata.split(':')[0] == 'bitcoin'):
            qrdata = qrdata.split(':')[1].split('?')[0]
        if (qrdata[:3] == 'bc1') or (qrdata[:1] == '3') or (qrdata[:1] == '1'):
            if not (len(qrdata) >= 26) and (len(qrdata) <= 35):
                error = qrdata + ' is not a valid bitcoin address, address should have a length from 26 to 35 instead of ' + str(len(qrdata)) + '.'
        else: 
            error = qrdata + ' is not a valid bitcoin address, address should have started with bc1, 3 or 1 instead of ' + qrdata[:1] + ', or ' + qrdata[:3] + '.'
        if error:
            qrdata = None
        qrcodescanning = True
        return redirect('/YHRwalletinstructions')
    return render_template('YHRwalletinstructions.html', error=error, qrdata=qrdata)

if __name__ == "__main__":
    app.run()
