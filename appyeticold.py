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
app = Flask(__name__)
home = os.getenv("HOME")
rpcpsw = str(random.randrange(0,1000000))
if not (os.path.exists(home + "/.bitcoin")):
    subprocess.call(['mkdir ~/.bitcoin'],shell=True)
else:
    subprocess.call(['rm ~/.bitcoin/bitcoin.conf'],shell=True)
subprocess.call('echo "server=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword='+rpcpsw+'" >> '+home+'/.bitcoin/bitcoin.conf', shell=True)

### VARIBALES START
settings = {
    "rpc_username": "rpcuser",
    "rpc_password": rpcpsw,
    "rpc_host": "127.0.0.1",
    "rpc_port": 8332,
    "address_chunk": 100
}
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
    if request.method == 'GET':
        return redirect('/YCopenbitcoin')
    return render_template('redirect.html')

#finish open bitcoin
@app.route("/YCopenbitcoin", methods=['GET', 'POST'])
def YCopenbitcoin():
    global progress
    if request.method == 'GET':
        home = os.getenv("HOME")
        if BTCClosed():
            subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        progress = BTCprogress()
    if request.method == 'POST':
        if progress >= 99.9:
            subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yeticold"'],shell=True)
            return redirect('/YCpackage')
        else:
            return redirect('/YCopenbitcoin')
    return render_template('YCopenbitcoin.html', progress=progress)

@app.route("/YCpackage", methods=['GET', 'POST'])
def YCpackage():
    if request.method == 'GET':
        subprocess.call(['gnome-terminal -- bash -c "sudo chmod +x ~/yeticold/scripts/rpkg-script.sh; sudo ~/yeticold/scripts/rpkg-script.sh"'],shell=True)
    if request.method == 'POST':
        return redirect('/YCmovefiles')
    return render_template('YCpackage.html')

@app.route("/YCmovefiles", methods=['GET', 'POST'])
def YCmovefiles():
    if request.method == 'GET':
        subprocess.call('python3 ~/yeticold/utils/stopbitcoin.py', shell=True)
    if request.method == 'POST':
        return redirect('/YCopenbitcoinB')
    return render_template('YCmovefiles.html')
#finish open bitcoin
@app.route("/YCopenbitcoinB", methods=['GET', 'POST'])
def YCopenbitcoinB():
    global progress
    if request.method == 'GET':
        home = os.getenv("HOME")
        if BTCClosed():
            subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        progress = BTCprogress()
    if request.method == 'POST':
        IBD = BTCRunning()
        if IBD:
            subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli loadwallet "yeticold"'],shell=True)
            return redirect('/YConlinestartup')
        else:
            return redirect('/YCopenbitcoinB')
    return render_template('YCopenbitcoinB.html', progress=progress)

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
    if request.method == 'GET':
        if BTCClosed():
            subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
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
            response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwallettwo'+str(i)+' sethdseed false "'+privkeylist[i]+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            if not (len(response[1]) == 0): 
                print(response)
                return "error response from sethdseed: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwallettwo'+str(i)+' sethdseed false "'+privkeylist[i]+'"'
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
        desc = response["descriptor"]
        firstqrcode = desc
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

# @app.route("/YCsendtest", methods=['GET', 'POST'])
# def YCsendtest():
#     global firstqrcode
#     global firstqrname
#     global pubdesc
#     global adrlist
#     if request.method == 'GET':
#         pubdesc = firstqrcode[:-1]
#         response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticold importmulti \'[{ "desc": "'+pubdesc+'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#         if not (len(response[1]) == 0): 
#             print(response)
#             return "error response from importmulti: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticold importmulti \'[{ "desc": "'+pubdesc+'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''
#         response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticold deriveaddresses "'+pubdesc+'" "[0,999]"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#         if not (len(response[0]) == 0): 
#             response = json.loads(response[0].decode("utf-8"))
#         adrlist = response
#         randomnum = str(random.randrange(0,1000000))
#         firstqrname = randomnum
#         firstqrcode = adrlist[0]
#         path = url_for('static', filename='firstqrcode' + firstqrname + '.png')
#         qr = qrcode.QRCode(
#                version=1,
#                error_correction=qrcode.constants.ERROR_CORRECT_L,
#                box_size=10,
#                border=4,
#         )
#         qr.add_data(firstqrcode)
#         qr.make(fit=True)
#         img = qr.make_image(fill_color="black", back_color="white")
#         home = os.getenv("HOME")
#         img.save(home + '/yeticold/static/firstqrcode' + firstqrname + '.png')
#     if request.method == 'POST':
#         return redirect('/YCsendtestB')
#     return render_template('YCsendtest.html', path=path, qrdata=firstqrcode)

# @app.route("/YCsendtestB", methods=['GET', 'POST'])
# def YCsendtestB():
#     global pubdesc
#     global adrlist
#     if request.method == 'GET':
#         randomnum = str(random.randrange(0,1000000))
#         firstqrname = randomnum
#         firstqrcode = adrlist[1]
#         path = url_for('static', filename='firstqrcode' + firstqrname + '.png')
#         qr = qrcode.QRCode(
#                version=1,
#                error_correction=qrcode.constants.ERROR_CORRECT_L,
#                box_size=10,
#                border=4,
#         )
#         qr.add_data(firstqrcode)
#         qr.make(fit=True)
#         img = qr.make_image(fill_color="black", back_color="white")
#         home = os.getenv("HOME")
#         img.save(home + '/yeticold/static/firstqrcode' + firstqrname + '.png')
#     if request.method == 'POST':
#         return redirect('/YCsendtestC')
#     return render_template('YCsendtestB.html', path=path, qrdata=firstqrcode)

# @app.route("/YCsendtestC", methods=['GET', 'POST'])
# def YCsendtestC():
#     global pubdesc
#     global adrlist
#     if request.method == 'GET':
#         randomnum = str(random.randrange(0,1000000))
#         firstqrname = randomnum
#         firstqrcode = adrlist[2]
#         path = url_for('static', filename='firstqrcode' + firstqrname + '.png')
#         qr = qrcode.QRCode(
#                version=1,
#                error_correction=qrcode.constants.ERROR_CORRECT_L,
#                box_size=10,
#                border=4,
#         )
#         qr.add_data(firstqrcode)
#         qr.make(fit=True)
#         img = qr.make_image(fill_color="black", back_color="white")
#         home = os.getenv("HOME")
#         img.save(home + '/yeticold/static/firstqrcode' + firstqrname + '.png')
#     if request.method == 'POST':
#         return redirect('/YCcheckfunds')
#     return render_template('YCsendtestC.html', path=path, qrdata=firstqrcode)

# @app.route("/YCcheckfunds", methods=['GET', 'POST'])
# def YCcheckfunds():
#     if request.method == 'POST':
#         return redirect('/YCdisplayutxo')
#     return render_template('YCcheckfunds.html')

##SWITCH TO OFFLINE

@app.route('/YCdisplayseeds', methods=['GET', 'POST'])
def YCdisplayseeds():
    global privkeylist
    global privkeycount
    if request.method == 'GET':
        privkey = privkeylist[privkeycount]
        passphraselist = ConvertToPassphrase(privkey)
    if request.method == 'POST':
        home = os.getenv('HOME')
        path = home + '/Documents'
        subprocess.call('rm '+path+'/ycseed'+str(privkeycount + 1)+'.txt', shell=True)
        subprocess.call('touch '+path+'/ycseed'+str(privkeycount + 1)+'.txt', shell=True)
        file = ''
        for i in range(0,13):
            file = file + request.form['displayrow' + str(i+1)] + '\n'
        subprocess.call('echo "'+file+'" >> '+path+'/ycseed'+str(privkeycount + 1)+'.txt', shell=True)
        privkeycount = privkeycount + 1
        if (privkeycount == 7):
            privkeycount = 0
            return redirect('/YCcheckseeds')
        else:
            return redirect('/YCdisplayseeds')
    return render_template('YCdisplayseeds.html', PPL=passphraselist, x=privkeycount + 1, i=privkeycount + 25)

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
                    response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwallet'+str(i)+' sethdseed false "'+privkeylist[i]+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                    if not (len(response[1]) == 0): 
                        print(response)
                        return "error response from sethdseed: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwallet'+str(i)+' sethdseed false "'+privkeylist[i]+'"'
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
    return render_template('YCcheckseeds.html', x=privkeycount + 1, error=error,i=privkeycount + 35 )

# @app.route("/YCscanutxo", methods=['GET', 'POST'])
# def YCscanutxo():
#     if request.method == 'POST':
#         global firstqrcode
#         global utxoresponse
#         firstqrcode = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
#         utxoresponse = firstqrcode
#         return redirect('/YCscandescriptorB')
#     return render_template('YCscanutxo.html')

# ##SWITCH TO ONLINE

# @app.route("/YCdisplayutxo", methods=['GET', 'POST'])
# def YCdisplayutxo():
#     global utxo
#     global secondqrname
#     if request.method == 'GET':
#         rpc = RPC()
#         utxo = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticold listunspent'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#         utxos = json.loads(utxo[0])
#         utxo = utxos[0]
#         newstr = utxo['txid'] + ','
#         newstr = newstr + str(utxo['vout']) + ','
#         newstr = newstr + utxo['address'] + ','
#         newstr = newstr + utxo['scriptPubKey'] + ','
#         newstr = newstr + str(utxo['amount']) + ','
#         newstr = newstr + rpc.getnewaddress() + ','
#         newstr = newstr + utxo['witnessScript'] + '&'
#         utxoone = utxos[1]
#         newstr = newstr + utxoone['txid'] + ','
#         newstr = newstr + str(utxoone['vout']) + ','
#         newstr = newstr + utxoone['address'] + ','
#         newstr = newstr + utxoone['scriptPubKey'] + ','
#         newstr = newstr + str(utxoone['amount']) + ','
#         newstr = newstr + rpc.getnewaddress() + ','
#         newstr = newstr + utxoone['witnessScript'] + '&'
#         utxotwo = utxos[2]
#         newstr = newstr + utxotwo['txid'] + ','
#         newstr = newstr + str(utxotwo['vout']) + ','
#         newstr = newstr + utxotwo['address'] + ','
#         newstr = newstr + utxotwo['scriptPubKey'] + ','
#         newstr = newstr + str(utxotwo['amount']) + ','
#         newstr = newstr + rpc.getnewaddress() + ','
#         newstr = newstr + utxotwo['witnessScript']
#         randomnum = str(random.randrange(0,1000000))
#         secondqrname = randomnum
#         qr = qrcode.QRCode(
#                version=1,
#                error_correction=qrcode.constants.ERROR_CORRECT_L,
#                box_size=10,
#                border=4,
#         )
#         qr.add_data(newstr)
#         qr.make(fit=True)
#         img = qr.make_image(fill_color="black", back_color="white")
#         home = os.getenv("HOME")
#         img.save(home + '/yeticold/static/utxoqrcode'+secondqrname+'.png')
#         path = url_for('static', filename='utxoqrcode' + secondqrname + '.png')
#     if request.method == 'POST':
#         return redirect('/YCscantransaction')
#     return render_template('YCdisplayutxo.html', qrdata=newstr, path=path)

##SWITCH TO OFFLINE

# @app.route("/YCscandescriptorB", methods=['GET', 'POST'])
# def YCscandescriptorB():
#     if request.method == 'POST':
#         global secondqrcode
#         global pubdesc
#         global transnum
#         secondqrcode = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
#         pubdesc = secondqrcode
#         transnum = 1
#         return redirect('/YCdisplaytransaction')
#     return render_template('YCscandescriptorB.html')

######USE DIFFRENT WALLET NAMES
# @app.route("/YCdisplaytransaction", methods=['GET', 'POST'])
# def YCdisplaytransaction():
#     global firstqrcode
#     global secondqrcode
#     global thirdqrcode
#     global firstqrname
#     global secondqrname
#     global thirdqrname
#     global privkeylist
#     global xprivlist
#     global transnum
#     global utxoresponse
#     global pubdesc
#     if request.method == 'GET':
#         subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yeticoldwalletthree"'],shell=True)
#         subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli loadwallet "yeticoldwalletthree"'],shell=True)
#         xpublist = pubdesc.decode("utf-8").split(',')[1:]
#         xpublist[6] = xpublist[6].split('))')[0]
#         response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletthree getdescriptorinfo "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xpublist[3]+','+xpublist[4]+','+xpublist[5]+','+xpublist[6]+'))"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#         if not (len(response[0]) == 0): 
#             response = json.loads(response[0].decode("utf-8"))
#         else:
#             print(response)
#             return "error response from getdescriptorinfo: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletthree getdescriptorinfo "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xpublist[3]+','+xpublist[4]+','+xpublist[5]+','+xpublist[6]+'))"'
#         checksum = response["checksum"]
#         response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletthree importmulti \'[{ "desc": "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xpublist[3]+','+xpublist[4]+','+xpublist[5]+','+xpublist[6]+'))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#         if not (len(response[1]) == 0): 
#             print(response)
#             return "error response from importmulti: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletthree importmulti \'[{ "desc": "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xpublist[3]+','+xpublist[4]+','+xpublist[5]+','+xpublist[6]+'))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''
#         rpc = RPC()
#         trans = utxoresponse
#         trans = trans.decode("utf-8")
#         trans = trans.split("&")[0].split(",")
#         trans[1] = int(trans[1])
#         trans[4] = float(trans[4])
#         minerfee = float(rpc.estimatesmartfee(1)["feerate"])
#         kilobytespertrans = 0.200
#         amo = (trans[4] - (minerfee * kilobytespertrans))
#         amo = "{:.8f}".format(float(amo))
#         response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletthree createrawtransaction \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\' \'[{"'+trans[5]+'" : '+str(amo)+'}]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#         if not (len(response[0]) == 0): 
#             response = response[0].decode("utf-8")
#         else:
#             print(response)
#             return "error response from createrawtransaction: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletthree createrawtransaction \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\' \'[{"'+trans[5]+'" : '+str(amo)+'}]\''
#         transonehex = response[:-1]
#         response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletthree signrawtransactionwithwallet '+transonehex+' \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+', "scriptPubKey": "'+trans[3]+'", "witnessScript": "'+trans[6][:-1]+'", "amount": "'+str(trans[4])+'" }]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#         if not (len(response[0]) == 0): 
#             response = json.loads(response[0].decode("utf-8"))
#         else:
#             print(response)
#             return "error response from signrawtransactionwithwallet: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletthree signrawtransactionwithwallet '+transonehex+' \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+', "scriptPubKey": "'+trans[3]+'", "witnessScript": "'+trans[6][:-1]+'", "amount": "'+str(trans[4])+'" }]\''
#         transone = response
#         firstqrcode = transone
#         randomnum = str(random.randrange(0,1000000))
#         firstqrname = randomnum
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#             )
#         qr.add_data(firstqrcode)
#         qr.make(fit=True)
#         img = qr.make_image(fill_color="black", back_color="white")
#         home = os.getenv("HOME")
#         img.save(home + '/yeticold/static/firsttransqrcode'+firstqrname+'.png')
#         path = url_for('static', filename='firsttransqrcode' + firstqrname + '.png')
#     if request.method == 'POST':
#         transnum = 2
#         return redirect('/YCdisplaytransactionB')
#     return render_template('YCdisplaytransaction.html', qrdata=firstqrcode, path=path)

# ##SWITCH TO ONLINE

# @app.route("/YCscantransaction", methods=['GET', 'POST'])
# def YCscantransaction():
#     if request.method == 'POST':
#         global firstqrcode
#         firstqrcode = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
#         return redirect('/YCswitchlaptop')
#     return render_template('YCscantransaction.html')

# @app.route("/YCswitchlaptop", methods=['GET', 'POST'])
# def YCswitchlaptop():
#     if request.method == 'POST':
#         return redirect('/YCscantransactionB')
#     return render_template('YCswitchlaptop.html')

# ##SWITCH TO OFFLINE

# ######USE DIFFRENT WALLET NAMES
# @app.route("/YCdisplaytransactionB", methods=['GET', 'POST'])
# def YCdisplaytransactionB():
#     global firstqrcode
#     global secondqrcode
#     global thirdqrcode
#     global firstqrname
#     global secondqrname
#     global thirdqrname
#     global privkeylist
#     global xprivlist
#     global transnum
#     global utxoresponse
#     global pubdesc
#     if request.method == 'GET':
#         subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yeticoldwalletfour"'],shell=True)
#         subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli loadwallet "yeticoldwalletfour"'],shell=True)
#         xpublist = pubdesc.decode("utf-8").split(',')[1:]
#         xpublist[6] = xpublist[6].split('))')[0]
#         response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletfour getdescriptorinfo "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xpublist[5]+','+xpublist[6]+'))"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#         if not (len(response[0]) == 0): 
#             response = json.loads(response[0].decode("utf-8"))
#         else:
#             print(response)
#             return "error response from getdescriptorinfo: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletfour getdescriptorinfo "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xpublist[5]+','+xpublist[6]+'))"'
#         checksum = response["checksum"]
#         response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletfour importmulti \'[{ "desc": "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xpublist[5]+','+xpublist[6]+'))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#         if not (len(response[1]) == 0): 
#             print(response)
#             return "error response from importmulti: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletfour importmulti \'[{ "desc": "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xpublist[5]+','+xpublist[6]+'))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''
#         rpc = RPC()
#         trans = utxoresponse #### parse this
#         trans = trans.decode("utf-8")
#         trans = trans.split("&")[1].split(",")
#         trans[1] = int(trans[1])
#         trans[4] = float(trans[4])
#         minerfee = float(rpc.estimatesmartfee(1)["feerate"])
#         kilobytespertrans = 0.200
#         amo = (trans[4] - (minerfee * kilobytespertrans))
#         amo = "{:.8f}".format(float(amo))
#         response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletfour createrawtransaction \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\' \'[{"'+trans[5]+'" : '+str(amo)+'}]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#         if not (len(response[0]) == 0): 
#             response = response[0].decode("utf-8")
#         else:
#             print(response)
#             return "error response from createrawtransaction: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletfour createrawtransaction \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\' \'[{"'+trans[5]+'" : '+str(amo)+'}]\''
#         transtwohex = response[:-1]
#         response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletfour signrawtransactionwithwallet '+transtwohex+' \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+', "scriptPubKey": "'+trans[3]+'", "witnessScript": "'+trans[6][:-1]+'", "amount": "'+str(trans[4])+'" }]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#         if not (len(response[0]) == 0): 
#             response = json.loads(response[0].decode("utf-8"))
#         else:
#             print(response)
#             return "error response from signrawtransactionwithwallet: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletfour signrawtransactionwithwallet '+transtwohex+' \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+', "scriptPubKey": "'+trans[3]+'", "witnessScript": "'+trans[6][:-1]+'", "amount": "'+str(trans[4])+'" }]\''
#         transtwo = response
#         secondqrcode = transtwo
#         randomnum = str(random.randrange(0,1000000))
#         secondqrname = randomnum
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#             )
#         qr.add_data(secondqrcode)
#         qr.make(fit=True)
#         img = qr.make_image(fill_color="black", back_color="white")
#         home = os.getenv("HOME")
#         img.save(home + '/yeticold/static/secondtransqrcode'+secondqrname+'.png')
#         path = url_for('static', filename='secondtransqrcode' + secondqrname + '.png')
#     if request.method == 'POST':
#         transnum = 3
#         return redirect('/YCdisplaytransactionC')
#     return render_template('YCdisplaytransactionB.html', qrdata=firstqrcode, path=path)

# ##SWITCH TO ONLINE

# @app.route("/YCscantransactionB", methods=['GET', 'POST'])
# def YCscantransactionB():
#     if request.method == 'POST':
#         global secondqrcode
#         secondqrcode = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
#         return redirect('/YCswitchlaptopB')
#     return render_template('YCscantransactionB.html')

# @app.route("/YCswitchlaptopB", methods=['GET', 'POST'])
# def YCswitchlaptopB():
#     if request.method == 'POST':
#         return redirect('/YCscantransactionC')
#     return render_template('YCswitchlaptopB.html')
# ##SWITCH TO OFFLINE


# ######USE DIFFRENT WALLET NAMES
# @app.route("/YCdisplaytransactionC", methods=['GET', 'POST'])
# def YCdisplaytransactionC():
#     global firstqrcode
#     global secondqrcode
#     global thirdqrcode
#     global firstqrname
#     global secondqrname
#     global thirdqrname
#     global privkeylist
#     global xprivlist
#     global transnum
#     global utxoresponse
#     global pubdesc
#     if request.method == 'GET':
#         subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yeticoldwalletfive"'],shell=True)
#         subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli loadwallet "yeticoldwalletfive"'],shell=True)
#         xpublist = pubdesc.decode("utf-8").split(',')[1:]
#         xpublist[6] = xpublist[6].split('))')[0]
#         response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletfive getdescriptorinfo "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xpublist[2]+','+xpublist[3]+','+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#         if not (len(response[0]) == 0): 
#             response = json.loads(response[0].decode("utf-8"))
#         else:
#             print(response)
#             return "error response from getdescriptorinfo: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletfive getdescriptorinfo "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xpublist[2]+','+xpublist[3]+','+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))"'
#         checksum = response["checksum"]
#         response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletfive importmulti \'[{ "desc": "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xpublist[2]+','+xpublist[3]+','+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#         if not (len(response[1]) == 0): 
#             print(response)
#             return "error response from importmulti: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletfive importmulti \'[{ "desc": "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xpublist[2]+','+xpublist[3]+','+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''
#         rpc = RPC()
#         trans = utxoresponse #### parse this
#         trans = trans.decode("utf-8")
#         trans = trans.split("&")[2].split(",")
#         trans[1] = int(trans[1])
#         trans[4] = float(trans[4])
#         minerfee = float(rpc.estimatesmartfee(1)["feerate"])
#         kilobytespertrans = 0.200
#         amo = (trans[4] - (minerfee * kilobytespertrans))
#         amo = "{:.8f}".format(float(amo))
#         response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletfive createrawtransaction \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\' \'[{"'+trans[5]+'" : '+str(amo)+'}]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#         if not (len(response[0]) == 0): 
#             response = response[0].decode("utf-8")
#         else:
#             print(response)
#             return "error response from createrawtransaction: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletfive createrawtransaction \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\' \'[{"'+trans[5]+'" : '+str(amo)+'}]\''
#         transthreehex = response[:-1]
#         response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletfive signrawtransactionwithwallet '+transthreehex+' \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+', "scriptPubKey": "'+trans[3]+'", "witnessScript": "'+trans[6][:-1]+'", "amount": "'+str(trans[4])+'" }]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#         if not (len(response[0]) == 0): 
#             response = json.loads(response[0].decode("utf-8"))
#         else:
#             print(response)
#             return "error response from signrawtransactionwithwallet: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwalletfive signrawtransactionwithwallet '+transthreehex+' \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+', "scriptPubKey": "'+trans[3]+'", "witnessScript": "'+trans[6][:-1]+'", "amount": "'+str(trans[4])+'" }]\''
#         transthree = response
#         thirdqrcode = transthree
#         randomnum = str(random.randrange(0,1000000))
#         thirdqrname = randomnum
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#             )
#         qr.add_data(thirdqrcode)
#         qr.make(fit=True)
#         img = qr.make_image(fill_color="black", back_color="white")
#         home = os.getenv("HOME")
#         img.save(home + '/yeticold/static/thirdtransqrcode'+thirdqrname+'.png')
#         path = url_for('static', filename='thirdtransqrcode' + thirdqrname + '.png')
#     if request.method == 'POST':
#         return redirect('/YCcopyseeds')
#     return render_template('YCdisplaytransactionC.html', qrdata=firstqrcode, path=path)

# ##SWITCH TO ONLINE

# @app.route("/YCscantransactionC", methods=['GET', 'POST'])
# def YCscantransactionC():
#     if request.method == 'POST':
#         global thirdqrcode
#         global secondqrcode
#         global thirdqrcode
#         thirdqrcode = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
#         return redirect('/YCsendtransactions')
#     return render_template('YCscantransactionC.html')

# @app.route("/YCsendtransactions", methods=['GET', 'POST'])
# def YCsendtransactions():
#     global firstqrcode
#     global secondqrcode
#     global thirdqrcode
#     if request.method == 'GET':
#         parsedfirstqrcode = firstqrcode.decode("utf-8").split('\'')[3]
#         parsedsecondqrcode = secondqrcode.decode("utf-8").split('\'')[3]
#         parsedthirdqrcode = thirdqrcode.decode("utf-8").split('\'')[3]
#         response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticold sendrawtransaction '+parsedfirstqrcode+''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#         if not (len(response[1]) == 0): 
#             print(response)
#             return "error response from sendrawtransaction: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticold sendrawtransaction '+parsedfirstqrcode+''
#         response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticold sendrawtransaction '+parsedsecondqrcode+''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#         if not (len(response[1]) == 0): 
#             print(response)
#             return "error response from sendrawtransaction: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticold sendrawtransaction '+parsedsecondqrcode+''
#         response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticold sendrawtransaction '+parsedthirdqrcode+''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#         if not (len(response[1]) == 0): 
#             print(response)
#             return "error response from sendrawtransaction: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticold sendrawtransaction '+parsedthirdqrcode+''
#     if request.method == 'POST':
#         return redirect('/YCstoreseeds')
#     return render_template('YCsendtransactions.html')
#
# ####SWITCH TO OFFLINE

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
