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
### VARIBALES START

settings = {"rpc_username": "rpcuser","rpc_password": rpcpsw,"rpc_host": "127.0.0.1","rpc_port": 8332,"address_chunk": 100}
wallet_template = "http://{rpc_username}:{rpc_password}@{rpc_host}:{rpc_port}/wallet/{wallet_name}"
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
base_count = len(BASE58_ALPHABET)
privkeylist = []
xprivlist = []
firstqrcode = 0
secondqrcode = 0
error = None
thirdqrcode = 0
privkeycount = 0
firstqrname = None
secondqrname = None
thirdqrname = None
utxoresponse = None
pubdesc = None
adrlist = []
transnum = 0
progress = 0
utxo = None
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
    print(subprocess.call('lsof -n -i :8332', shell=True))
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

def ConvertToWIF(binary):
    assert(len(binary) == 256)
    key = hex(int(binary, 2)).replace('0x', "")
    padkey = padhex(key)
    assert(int(padkey, 16) == int(key,16))
    return wif(bytes.fromhex(padkey))

def ConvertToPassphrase(privkeywif):
    passphraselist = []
    for i in range(len(privkeywif)):
        passphraselist.append(switcher.get(str(privkeywif[i])))
    return passphraselist

def PassphraseToWIF(passphraselist):
    Privkey = ''
    for i in range(len(passphraselist)):
        Privkey += switcher.get(str(passphraselist[i]))
    return Privkey

def xor(x, y):
    return '{1:0{0}b}'.format(len(x), int(x, 2) ^ int(y, 2))

def decode58(s):
    decoded = 0
    multi = 1
    s = s[::-1]
    for char in s:
        decoded += multi * BASE58_ALPHABET.index(char)
        multi = multi * base_count
    return decoded

### FUNCTIONS STOP

@app.route("/", methods=['GET', 'POST'])
def redirectroute():
    return redirect('/YConlinestartup')

###ISSUE have user visit disc.yeticold.com on disconnected laptop
@app.route("/YConlinestartup", methods=['GET', 'POST'])
def YConlinestartup():
    if request.method == 'POST':
        return redirect('/YCscandescriptor')
    return render_template('YConlinestartup.html')


##SWIWCH TO OFFLINE

#finish open bitcoin
@app.route("/YCopenbitcoinC", methods=['GET', 'POST'])
def YCopenbitcoinC():
    global progress
    global psw
    if request.method == 'GET':
        if BTCClosed():
            if not (os.path.exists(home + "/.bitcoin")):
                subprocess.call(['wsh https://drive.google.com/uc?authuser=0&id=1qjsuk1mllQMcWKmWZXhDQ9eRL7hL7aLA&export=download'],shell=True)
            if (os.path.exists(home + "/.bitcoin/bitcoin.conf")):
                with open(".bitcoin/bitcoin.conf","r+") as f:
                    old = f.read()
                    f.seek(0)
                    new = "server=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword="+rpcpsw+"\n"
                    f.write(new + old)
            else:
                subprocess.call('echo "server=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword='+rpcpsw+'" >> '+home+'/.bitcoin/bitcoin.conf', shell=True)
            subprocess.call('rm -r ~/.bitcoin/regtest', shell=True)
            subprocess.Popen('~/yeticold/bitcoin/bin/bitcoind -regtest -server=1 -rpcport=8332 -rpcuser=rpcuser -rpcpassword='+rpcpsw+' -reindex -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        progress = BTCprogress()
    if request.method == 'POST':
        IBD = BTCRunning()
        if IBD:
            subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yeticold"'],shell=True)
            return redirect('/YCgetseeds')
        else:
            return redirect('/YCopenbitcoinC')
    return render_template('YCopenbitcoinC.html', progress=progress)

@app.route("/YCgetseeds", methods=['GET', 'POST'])
def YCgetseeds():
    global privkeylist
    global privkeycount
    global firstqrcode
    global secondqrcode
    global xprivlist
    global pubdesc
    if request.method == 'POST':
        if request.form['skip'] == 'skip':
            privkeylisttemp = []
            for i in range(1,8):
                rpc = RPC()
                adr = rpc.getnewaddress()
                newprivkey = rpc.dumpprivkey(adr)
                binary = bin(decode58(newprivkey))[2:][8:-40]
                newbinary = '1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
                WIF = ConvertToWIF(xor(binary,newbinary))
                privkeylisttemp.append(WIF)
            privkeycount = 0
            privkeylist = privkeylisttemp
        else:
            privkeylisttemp = []
            for i in range(1,8):
                rpc = RPC()
                adr = rpc.getnewaddress()
                newprivkey = rpc.dumpprivkey(adr)
                binary = bin(decode58(newprivkey))[2:][8:-40]
                WIF = ConvertToWIF(xor(binary,request.form['binary' + str(i)]))
                privkeylisttemp.append(WIF)
            privkeycount = 0
            privkeylist = privkeylisttemp
        for i in range(0,7):
            home = os.getenv('HOME')
            pathtwo = home + '/yeticoldwallet' + str(i)
            path = home + '/yeticoldwallettwo' + str(i)
            subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yeticoldwallettwo'+str(i)+'"'],shell=True)
            subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli loadwallet "yeticoldwallettwo'+str(i)+'"'],shell=True)
            response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwallettwo'+str(i)+' sethdseed true "'+privkeylist[i]+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            if not (len(response[1]) == 0): 
                print(response)
                return "error response from sethdseed: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwallettwo'+str(i)+' sethdseed true "'+privkeylist[i]+'"'
            response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwallettwo'+str(i)+' dumpwallet "yeticoldwallettwo'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            wallet = open(path,'r')
            wallet.readline()
            wallet.readline()
            wallet.readline()
            wallet.readline()
            wallet.readline()
            privkeyline = wallet.readline()
            privkeyline = privkeyline.split(" ")[4][:-1]
            xprivlist.append(privkeyline)
        addresses = []
        checksum = None
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticold getdescriptorinfo "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(response[0]) == 0): 
            response = json.loads(response[0].decode("utf-8"))
        else:
            print(response)
            return "error response from getdescriptorinfo: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticold getdescriptorinfo "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))"'
        checksum = response["checksum"]
        pubdesc = response["descriptor"]
        firstqrcode = pubdesc
        return redirect('/YCdisplaydescriptor')
    return render_template('YCgetseeds.html')

@app.route("/YCdisplaydescriptor", methods=['GET', 'POST'])
def YCdisplaydescriptor():
    global privkeylist
    global firstqrcode
    global firsqrname
    if request.method == 'GET':
        randomnum = str(random.randrange(0,1000000))
        firstqrname = randomnum
        qr = qrcode.QRCode(
               version=1,
               error_correction=qrcode.constants.ERROR_CORRECT_L,
               box_size=10,
               border=4,
        )
        qr.add_data(firstqrcode)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        home = os.getenv("HOME")
        img.save(home + '/yeticold/static/firstqrcode' + firstqrname + '.png')
        path = url_for('static', filename='firstqrcode' + firstqrname + '.png')
    if request.method == 'POST':
        home = os.getenv('HOME')
        seedpath = home + '/Documents'
        subprocess.call('rm -r '+seedpath+'/ycseed*', shell=True)
        return redirect('/YCdisplayseeds')
    return render_template('YCdisplaydescriptor.html', qrdata=firstqrcode, path=path)

##SWITCH TO ONLINE

@app.route("/YCscandescriptor", methods=['GET', 'POST'])
def YCscandescriptor():
    global firstqrcode
    if request.method == 'POST':
        firstqrcode = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        firstqrcode = firstqrcode.decode("utf-8")
        return redirect('/YCprintpage')
    return render_template('YCscandescriptor.html')

@app.route("/YCprintpage", methods=['GET', 'POST'])
def YCprintpage():
    global firstqrcode
    global secondqrcode
    global firstqrname
    global secondqrname
    randomnum = str(random.randrange(0,1000000))
    firstqrname = randomnum
    secondqrname = randomnum
    thirdqrname = randomnum
    path = url_for('static', filename='firstqrcode' + firstqrname + '.png')
    if request.method == 'GET':
        qr = qrcode.QRCode(
               version=1,
               error_correction=qrcode.constants.ERROR_CORRECT_L,
               box_size=10,
               border=4,
        )
        qr.add_data(firstqrcode)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        home = os.getenv("HOME")
        img.save(home + '/yeticold/static/firstqrcode' + firstqrname + '.png')
    if request.method == 'POST':
        return redirect('/YCstoreseeds')
    return render_template('YCprintpage.html', qrdata=firstqrcode, path=path)

#SWITCH TO OFFLINE

@app.route('/YCdisplayseeds', methods=['GET', 'POST'])
def YCdisplayseeds():
    global privkeylist
    global privkeycount
    global pubdesc
    if request.method == 'GET':
        privkey = privkeylist[privkeycount]
        passphraselist = ConvertToPassphrase(privkey)
    if request.method == 'POST':
        home = os.getenv('HOME')
        path = home + '/Documents'
        subprocess.call('mkdir '+path+'/ycseed'+str(privkeycount + 1), shell=True)
        subprocess.call('touch '+path+'/ycseed'+str(privkeycount + 1)+'/ycseed'+str(privkeycount + 1)+'.txt', shell=True)
        file = ''
        for i in range(0,13):
            file = file + request.form['displayrow' + str(i+1)] + '\n'
        file = file + '\n\nThis is your descriptor in text format you have a duplicate of this text in QR format in this folder.\n' + pubdesc + '\n'
        file = file + '\n\nThis is a seed packet that contains 1/3 of the information needed to recover bitcoins in a 3 of 7 HD multisig wallet.\n'
        file = file + 'There are 6 other packets that are identical except that they contain one of the other sets of seed words.\n'
        file = file + 'The HD Multisig wallet was was created using YetiCold.com (a Python script to make the experience more user friendly) and Bitcoin Core 0.19 RC1.\n'
        file = file + 'To recover the bitcoin go to YetiCold.com and click "Cold" and then follow the recovery instructions.\n'
        file = file + 'YetiCold.com should direct you to download a script to make the process of using Bitcoin Core easier, but never trust any website with your seed words.\n'
        file = file + 'Consider putting a small amount of money into YetiCold.com cold storage and recovering them before attempting to recover significant funds.\n'
        file = file + 'A test run will give you the opportunity to make sure that your seed words are never connected to an online device before.\n'
        file = file + 'If many years have passed you should check that YetiCold.com has retained a good reputation.\n'
        file = file + 'If YetiCold.com is no longer reputable use Bitcoin Core alone to recover your bitcoin (with the help of a trusted expert only if absolutely needed as these people may attempt to steal the bitcoin).\n'
        file = file + 'No software beyond Bitcoin Core is required to recover the stored bitcoin.\n'
        file = file + 'This seed packet also contains a usb device that has a digital copy of the information on this document. It does not contain another set of seed words, but simply a copy of the seed words in this document.\n'
        file = file + 'Two other seed packets must be obtained to recover the bitcoin stored.\n'
        file = file + 'YetiCold.com recommends storing seed words in locations like safety deposit boxes, home safes, and with professionals such as accountants and lawyers.\n'
        subprocess.call('echo "'+file+'" >> '+path+'/ycseed'+str(privkeycount + 1)+'/ycseed'+str(privkeycount + 1)+'.txt', shell=True)
        qr = qrcode.QRCode(
               version=1,
               error_correction=qrcode.constants.ERROR_CORRECT_L,
               box_size=10,
               border=4,
        )
        qr.add_data(pubdesc)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        home = os.getenv("HOME")
        img.save(home + '/Documents/ycseed'+str(privkeycount + 1)+'/descriptor.png')
        privkeycount = privkeycount + 1
        if (privkeycount == 7):
            privkeycount = 0
            return redirect('/YCcheckseeds')
        else:
            return redirect('/YCdisplayseeds')
    return render_template('YCdisplayseeds.html', PPL=passphraselist, x=privkeycount + 1, i=privkeycount + 15)

@app.route('/YCcheckseeds', methods=['GET', 'POST'])
def YCcheckseeds():
    global privkeylist
    global xprivlist
    global privkeycount
    global error
    if request.method == 'POST':
        privkey = privkeylist[privkeycount]
        passphraselist = ConvertToPassphrase(privkey)
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
            error = None
            privkeycount = privkeycount + 1
            if (privkeycount >= 7):
                privkeycount = 7
                newxprivlist = []
                for i in range(0,7):
                    home = os.getenv('HOME')
                    path = home + '/yeticoldwallet' + str(i)
                    subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yeticoldwallet'+str(i)+'" false true'],shell=True)
                    subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli loadwallet "yeticoldwallet'+str(i)+'"'],shell=True)
                    response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwallet'+str(i)+' sethdseed true "'+privkeylist[i]+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                    if not (len(response[1]) == 0): 
                        print(response)
                        return "error response from sethdseed: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwallet'+str(i)+' sethdseed true "'+privkeylist[i]+'"'
                    response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwallet'+str(i)+' dumpwallet "yeticoldwallet'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                    wallet = open(path,'r')
                    wallet.readline()
                    wallet.readline()
                    wallet.readline()
                    wallet.readline()
                    wallet.readline()
                    privkeyline = wallet.readline()
                    privkeyline = privkeyline.split(" ")[4][:-1]
                    newxprivlist.append(privkeyline)
                    if not xprivlist[i] == newxprivlist[i]:
                        privkeycount = 0
                        privkeylist = []
                        error = 'You have imported your seeds correctly but your xprivs do not match: This means that you either do not have bitcoin running or its initial block download mode. Another issue is that you have a wallet folder or wallet dump file that was not deleted before starting this step.'
                        return redirect('/YCcheckseeds')
                return redirect('/YCcopyseeds')
            else:
                return redirect('/YCcheckseeds')
        else:
            error = 'You enterd the private key incorrectly but the checksums are correct please try agian. This means you probably inputed a valid seed, but not your seed ' +str(privkeycount + 1)+' seed.'
    return render_template('YCcheckseeds.html', x=privkeycount + 1, error=error,i=privkeycount + 22 )

@app.route("/YCcopyseeds", methods=['GET', 'POST'])
def YCcopyseeds():
    return render_template('YCcopyseeds.html')

###SWITCH TO ONLINE

@app.route("/YCstoreseeds", methods=['GET', 'POST'])
def YCstoreseeds():
    if request.method == 'POST':
        return redirect('/YCdeleteseeds')
    return render_template('YCstoreseeds.html')

@app.route("/YCdeleteseeds", methods=['GET', 'POST'])
def YCdeleteseeds():
    if request.method == 'POST':
        return redirect('/YCsendfunds')
    return render_template('YCdeleteseeds.html')

@app.route("/YCsendfunds", methods=['GET', 'POST'])
def YCsendfunds():
    if request.method == 'POST':
        subprocess.Popen('python3 ~/yeticold/scripts/YetiColdRecoveryOnline.py',shell=True,start_new_session=True)
    return render_template('YCsendfunds.html')

if __name__ == "__main__":
    app.run()
