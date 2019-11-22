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
subprocess.call(['sudo apt-get update'],shell=True)
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
    response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getblockchaininfo'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if not (len(response[0]) == 0):
        bitcoinprogress = json.loads(response[0])['verificationprogress']
        bitcoinprogress = bitcoinprogress * 100
        bitcoinprogress = round(bitcoinprogress, 3)
    else:
        print("error response: "+ str(response[1]))
        bitcoinprogress = 0
    return bitcoinprogress


def RPC():
    name = 'username'
    wallet_name = ''
    uri = wallet_template.format(**settings, wallet_name=wallet_name)
    rpc = AuthServiceProxy(uri, timeout=600)  # 1 minute timeout
    return rpc

def encode_base58(s):
    # determine how many 0 bytes (b'\x00') s starts with
    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break
    # convert to big endian integer
    num = int.from_bytes(s, 'big')
    prefix = '1' * count
    result = ''
    while num > 0:
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result
    return prefix + result


def hash256(s):
    """2 iterations of sha256"""
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()


def wif(pk):
    """Wallet import format for private key. Private key is a 32 bit bytes"""
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

# def ByteToHex( byteStr ):
#     return ''.join( [ "%02X " % ord( x ) for x in byteStr ] ).strip()

def decode58(s):
    """ Decodes the base58-encoded string s into an integer """
    decoded = 0
    multi = 1
    s = s[::-1]
    for char in s:
        decoded += multi * BASE58_ALPHABET.index(char)
        multi = multi * base_count
    return decoded

### FUNCTIONS STOP

@app.route("/", methods=['GET', 'POST'])
def step01():
    if request.method == 'GET':
        return redirect('/step07')
    return render_template('redirect.html')

### open bitcoin
@app.route("/step07", methods=['GET', 'POST'])
def step07():
    if request.method == 'POST':
        subprocess.Popen('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        return redirect('/step08')
    return render_template('YWstep07.html')
#finish open bitcoin
@app.route("/step08", methods=['GET', 'POST'])
def step08():
    global progress
    if request.method == 'GET':
        progress = BTCprogress()
    if request.method == 'POST':
        if progress >= 99.9:
            return redirect('/step09')
        else:
            return redirect('/step08')
    return render_template('YWstep08.html', progress=progress)

#randomise priv key and get xprivs
@app.route("/step09", methods=['GET', 'POST'])
def step09():
    global privkeylist
    global privkeycount
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
            pathtwo = home + '/blank' + str(i)
            path = home + '/full' + str(i)
            response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createwallet "full'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli loadwallet "full'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=full'+str(i)+' sethdseed false "'+privkeylist[i]+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            if not (len(response[1]) == 0): 
                print(response)
                return "error response from sethdseed: " + str(response[1]) + '\n' + '~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=full'+str(i)+' sethdseed false "'+privkeylist[i]+'"'
            response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=full'+str(i)+' dumpwallet "full'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
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
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getdescriptorinfo "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(response[0]) == 0): 
            response = json.loads(response[0].decode("utf-8"))
        else:
            print(response)
            return "error response from getdescriptorinfo: " + str(response[1]) + '\n' + '~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getdescriptorinfo "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))"'
        checksum = response["checksum"]
        pubdesc = response["descriptor"]
        return redirect('/step10')
    return render_template('YWstep09.html')

#display for print
@app.route("/step10", methods=['GET', 'POST'])
def step10():
    global firstqrcode
    global pubdesc
    if request.method == 'GET':
        randomnum = str(random.randrange(0,1000000))
        firstqrname = randomnum
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
        img.save(home + '/yeticold/static/firstqrcode' + firstqrname + '.png')
        route = url_for('static', filename='firstqrcode' + firstqrname + '.png')
    if request.method == 'POST':
        return redirect('/step11')
    return render_template('YWstep10.html', qrdata=pubdesc, route=route)

#get addresses and display one
@app.route("/step11", methods=['GET', 'POST'])
def step11():
    global pubdesc
    global adrlist
    if request.method == 'GET':
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "'+pubdesc+'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(response[1]) == 0): 
            print(response)
            return "error response from importmulti: " + str(response[1]) + '\n' + '~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "'+pubdesc+'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli deriveaddresses "'+pubdesc+'" "[0,999]"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(response[0]) == 0): 
            response = json.loads(response[0].decode("utf-8"))
        adrlist = response
        randomnum = str(random.randrange(0,1000000))
        firstqrname = randomnum
        firstqrcode = adrlist[0]
        routeone = url_for('static', filename='firstqrcode' + firstqrname + '.png')
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
        return redirect('/step12')
    return render_template('YWstep11.html', routeone=routeone, first=firstqrcode)

#display address for test amount
@app.route("/step12", methods=['GET', 'POST'])
def step12():
    global pubdesc
    global adrlist
    if request.method == 'GET':
        randomnum = str(random.randrange(0,1000000))
        firstqrname = randomnum
        firstqrcode = adrlist[1]
        routeone = url_for('static', filename='firstqrcode' + firstqrname + '.png')
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
        return redirect('/step13')
    return render_template('YWstep12.html', routeone=routeone, first=firstqrcode)

#display address for test amount
@app.route("/step13", methods=['GET', 'POST'])
def step13():
    global pubdesc
    global adrlist
    if request.method == 'GET':
        randomnum = str(random.randrange(0,1000000))
        firstqrname = randomnum
        firstqrcode = adrlist[2]
        routeone = url_for('static', filename='firstqrcode' + firstqrname + '.png')
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
        return redirect('/step14')
    return render_template('YWstep13.html', routeone=routeone, first=firstqrcode)

#confirm test funds
@app.route("/step14", methods=['GET', 'POST'])
def step14():
    if request.method == 'POST':
        return redirect('/step1521')
    return render_template('YWstep14.html')

#display seeds
@app.route('/step1521', methods=['GET', 'POST'])
def step1521():
    global privkeylist
    global privkeycount
    if request.method == 'GET':
        privkey = privkeylist[privkeycount]
        passphraselist = ConvertToPassphrase(privkey)
    if request.method == 'POST':
        home = os.getenv('HOME')
        path = home + '/Documents'
        subprocess.call('rm '+path+'/seed'+str(privkeycount + 1)+'.txt', shell=True)
        subprocess.call('touch '+path+'/seed'+str(privkeycount + 1)+'.txt', shell=True)
        file = ''
        for i in range(0,13):
            file = file + request.form['displayrow' + str(i+1)] + '\n'
        subprocess.call('echo "'+file+'" >> '+path+'/seed'+str(privkeycount + 1)+'.txt', shell=True)
        privkeycount = privkeycount + 1
        if (privkeycount == 7):
            privkeycount = 0
            return redirect('/step22')
        else:
            return redirect('/step1521')
    return render_template('YWstep1521.html', PPL=passphraselist, x=privkeycount + 1, i=privkeycount + 25)

#delete wallet
@app.route("/step22", methods=['GET', 'POST'])
def step22():
    if request.method == 'POST':
        subprocess.call('gnome-terminal -- bash -c "sudo python3 ~/yeticold/utils/deleteallwallets.py; echo "DONE, Close this window.""', shell=True)
        return redirect('/step23')
    return render_template('YWstep22.html')

#reopen bitcoin
@app.route("/step23", methods=['GET', 'POST'])
def step23():
    if request.method == 'POST':
        subprocess.Popen('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        return redirect('/step24')
    return render_template('YWstep23.html')

#finished reopen bitcoin
@app.route('/step24', methods=['GET', 'POST'])
def step24():
    global progress
    if request.method == 'GET':
        progress = BTCprogress()
    if request.method == 'POST':
        if progress >= 99:
            return redirect('/step2430')
        else:
            return redirect('/step24')
    return render_template('YWstep24.html', progress=progress)

#confirm privkey
@app.route('/step2430', methods=['GET', 'POST'])
def step2430():
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
                    rpc = RPC()
                    home = os.getenv('HOME')
                    path = home + '/blank' + str(i)
                    response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createwallet "blank'+str(i)+'" false true'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                    response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli loadwallet "blank'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                    response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=blank'+str(i)+' sethdseed false "'+privkeylist[i]+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                    if not (len(response[1]) == 0): 
                        print(response)
                        return "error response from sethdseed: " + str(response[1]) + '\n' + '~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=blank'+str(i)+' sethdseed false "'+privkeylist[i]+'"'
                    response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=blank'+str(i)+' dumpwallet "blank'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
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
                        return redirect('/step2430')
                return redirect('/step31')
            else:
                return redirect('/step2430')
        else:
            error = 'You enterd the private key incorrectly but the checksums are correct please try agian. This means you probably inputed a valid seed, but not your seed ' +str(privkeycount + 1)+' seed.'
    return render_template('YWstep2430.html', x=privkeycount + 1, error=error,i=privkeycount + 35 )

#delete wallet
@app.route("/step31", methods=['GET', 'POST'])
def step31():
    global transnum
    if request.method == 'POST':
        subprocess.call('gnome-terminal -- bash -c "sudo python3 ~/yeticold/utils/deleteallwallets.py; echo "DONE""', shell=True)
        return redirect('/step32')
    return render_template('YWstep31.html')
# open bitcoin
@app.route("/step32", methods=['GET', 'POST'])
def step32():
    if request.method == 'POST':
        subprocess.Popen('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        return redirect('/step33')
    return render_template('YWstep32.html')
#finish open bitcoin
@app.route('/step33', methods=['GET', 'POST'])
def step33():
    global progress
    if request.method == 'GET':
        progress = BTCprogress()
    if request.method == 'POST':
        if progress >= 99:
            return redirect('/step34')
        else:
            return redirect('/step33')
    return render_template('YWstep33.html', progress=progress)
#create first trans qr code
@app.route("/step34", methods=['GET', 'POST'])
def step34():
    global firstqrcode
    global secondqrcode
    global thirdqrcode
    global firstqrname
    global secondqrname
    global thirdqrname
    global privkeylist
    global xprivlist
    global transnum
    global utxoresponse
    global pubdesc
    if request.method == 'GET':
        #get utxos
        rpc = RPC()
        utxo = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli listunspent'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        utxos = json.loads(utxo[0])
        utxo = utxos[0]
        newstr = utxo['txid'] + ','
        newstr = newstr + str(utxo['vout']) + ','
        newstr = newstr + utxo['address'] + ','
        newstr = newstr + utxo['scriptPubKey'] + ','
        newstr = newstr + str(utxo['amount']) + ','
        newstr = newstr + rpc.getnewaddress() + ','
        newstr = newstr + utxo['witnessScript'] + '&'
        utxoone = utxos[1]
        newstr = newstr + utxoone['txid'] + ','
        newstr = newstr + str(utxoone['vout']) + ','
        newstr = newstr + utxoone['address'] + ','
        newstr = newstr + utxoone['scriptPubKey'] + ','
        newstr = newstr + str(utxoone['amount']) + ','
        newstr = newstr + rpc.getnewaddress() + ','
        newstr = newstr + utxoone['witnessScript'] + '&'
        utxotwo = utxos[2]
        newstr = newstr + utxotwo['txid'] + ','
        newstr = newstr + str(utxotwo['vout']) + ','
        newstr = newstr + utxotwo['address'] + ','
        newstr = newstr + utxotwo['scriptPubKey'] + ','
        newstr = newstr + str(utxotwo['amount']) + ','
        newstr = newstr + rpc.getnewaddress() + ','
        newstr = newstr + utxotwo['witnessScript']
        utxoresponse = newstr
        ###Conturinue with trans
        xpublist = pubdesc.split(',')[1:]
        xpublist[6] = xpublist[6].split('))')[0]
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getdescriptorinfo "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xpublist[3]+','+xpublist[4]+','+xpublist[5]+','+xpublist[6]+'))"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(response[0]) == 0): 
            response = json.loads(response[0].decode("utf-8"))
        else:
            print(response)
            return "error response from getdescriptorinfo: " + str(response[1]) + '\n' + '~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getdescriptorinfo "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xpublist[3]+','+xpublist[4]+','+xpublist[5]+','+xpublist[6]+'))"'
        checksum = response["checksum"]
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xpublist[3]+','+xpublist[4]+','+xpublist[5]+','+xpublist[6]+'))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(response[1]) == 0): 
            print(response)
            return "error response from importmulti: " + str(response[1]) + '\n' + '~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xpublist[3]+','+xpublist[4]+','+xpublist[5]+','+xpublist[6]+'))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''
        rpc = RPC()
        trans = utxoresponse
        trans = trans.decode("utf-8")
        trans = trans.split("&")[0].split(",")
        trans[1] = int(trans[1])
        trans[4] = float(trans[4])
        minerfee = float(rpc.estimatesmartfee(6)["feerate"])
        kilobytespertrans = 0.200
        amo = (trans[4] - (minerfee * kilobytespertrans))
        amo = "{:.8f}".format(float(amo))
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createrawtransaction \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\' \'[{"'+trans[5]+'" : '+str(amo)+'}]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(response[0]) == 0): 
            response = response[0].decode("utf-8")
        else:
            print(response)
            return "error response from createrawtransaction: " + str(response[1]) + '\n' + '~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createrawtransaction \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\' \'[{"'+trans[5]+'" : '+str(amo)+'}]\''
        transonehex = response[:-1]
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli signrawtransactionwithwallet '+transonehex+' \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(response[0]) == 0): 
            response = json.loads(response[0].decode("utf-8"))
        else:
            print(response)
            return "error response from signrawtransactionwithwallet: " + str(response[1]) + '\n' + '~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli signrawtransactionwithwallet '+transonehex+' \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\''
        transone = response
        firstqrcode = transone
        randomnum = str(random.randrange(0,1000000))
        firstqrname = randomnum
    if request.method == 'POST':
        return redirect('/step35')
    return render_template('YWstep34.html')

#delete wallet
@app.route("/step35", methods=['GET', 'POST'])
def step35():
    if request.method == 'POST':
        subprocess.call('gnome-terminal -- bash -c "sudo python3 ~/yeticold/utils/deleteallwallets.py; echo "DONE""', shell=True)
        return redirect('/step36')
    return render_template('YWstep35.html')
#open bitcoin
@app.route("/step36", methods=['GET', 'POST'])
def step36():
    if request.method == 'POST':
        subprocess.Popen('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        return redirect('/step37')
    return render_template('YWstep36.html')
#finish open bitcoin
@app.route('/step37', methods=['GET', 'POST'])
def step37():
    global progress
    if request.method == 'GET':
        progress = BTCprogress()
    if request.method == 'POST':
        if progress >= 99:
            return redirect('/step38')
        else:
            return redirect('/step37')
    return render_template('YWstep37.html', progress=progress)
#create second transaction
@app.route("/step38", methods=['GET', 'POST'])
def step38():
    global firstqrcode
    global secondqrcode
    global thirdqrcode
    global firstqrname
    global secondqrname
    global thirdqrname
    global privkeylist
    global xprivlist
    global transnum
    global utxoresponse
    global pubdesc
    if request.method == 'GET':
        xpublist = pubdesc.decode("utf-8").split(',')[1:]
        xpublist[6] = xpublist[6].split('))')[0]
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getdescriptorinfo "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xpublist[5]+','+xpublist[6]+'))"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(response[0]) == 0): 
            response = json.loads(response[0].decode("utf-8"))
        else:
            print(response)
            return "error response from getdescriptorinfo: " + str(response[1]) + '\n' + '~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getdescriptorinfo "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xpublist[5]+','+xpublist[6]+'))"'
        checksum = response["checksum"]
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xpublist[5]+','+xpublist[6]+'))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(response[1]) == 0): 
            print(response)
            return "error response from importmulti: " + str(response[1]) + '\n' + '~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xpublist[5]+','+xpublist[6]+'))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''
        rpc = RPC()
        trans = utxoresponse #### parse this
        trans = trans.decode("utf-8")
        trans = trans.split("&")[1].split(",")
        trans[1] = int(trans[1])
        trans[4] = float(trans[4])
        minerfee = float(rpc.estimatesmartfee(6)["feerate"])
        kilobytespertrans = 0.200
        amo = (trans[4] - (minerfee * kilobytespertrans))
        amo = "{:.8f}".format(float(amo))
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createrawtransaction \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\' \'[{"'+trans[5]+'" : '+str(amo)+'}]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(response[0]) == 0): 
            response = response[0].decode("utf-8")
        else:
            print(response)
            return "error response from createrawtransaction: " + str(response[1]) + '\n' + '~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createrawtransaction \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\' \'[{"'+trans[5]+'" : '+str(amo)+'}]\''
        transtwohex = response[:-1]
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli signrawtransactionwithwallet '+transtwohex+' \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(response[0]) == 0): 
            response = json.loads(response[0].decode("utf-8"))
        else:
            print(response)
            return "error response from signrawtransactionwithwallet: " + str(response[1]) + '\n' + '~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli signrawtransactionwithwallet '+transtwohex+' \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\''
        transtwo = response
        secondqrcode = transtwo
    if request.method == 'POST':
        return redirect('/step39')
    return render_template('YWstep38.html')
##SWITCH TO ONLINE
#delete wallet
@app.route("/step39", methods=['GET', 'POST'])
def step39():
    if request.method == 'POST':
        subprocess.call('gnome-terminal -- bash -c "sudo python3 ~/yeticold/utils/deleteallwallets.py; echo "DONE""', shell=True)
        return redirect('/step40')
    return render_template('YWstep39.html')
#open bitcoin
@app.route("/step40", methods=['GET', 'POST'])
def step40():
    if request.method == 'POST':
        subprocess.Popen('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        return redirect('/step41')
    return render_template('YWstep40.html')
#finish open bitcoin
@app.route('/step41', methods=['GET', 'POST'])
def step41():
    global progress
    if request.method == 'GET':
        progress = BTCprogress()
    if request.method == 'POST':
        if progress >= 99:
            return redirect('/step42')
        else:
            return redirect('/step41')
    return render_template('YWstep41.html', progress=progress)
#create third trans
@app.route("/step42", methods=['GET', 'POST'])
def step42():
    global firstqrcode
    global secondqrcode
    global thirdqrcode
    global firstqrname
    global secondqrname
    global thirdqrname
    global privkeylist
    global xprivlist
    global transnum
    global utxoresponse
    global pubdesc
    if request.method == 'GET':
        xpublist = pubdesc.decode("utf-8").split(',')[1:]
        xpublist[6] = xpublist[6].split('))')[0]
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getdescriptorinfo "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xpublist[2]+','+xpublist[3]+','+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(response[0]) == 0): 
            response = json.loads(response[0].decode("utf-8"))
        else:
            print(response)
            return "error response from getdescriptorinfo: " + str(response[1]) + '\n' + '~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getdescriptorinfo "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xpublist[2]+','+xpublist[3]+','+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))"'
        checksum = response["checksum"]
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xpublist[2]+','+xpublist[3]+','+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(response[1]) == 0): 
            print(response)
            return "error response from importmulti: " + str(response[1]) + '\n' + '~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xpublist[2]+','+xpublist[3]+','+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''
        rpc = RPC()
        trans = utxoresponse #### parse this
        trans = trans.decode("utf-8")
        trans = trans.split("&")[2].split(",")
        trans[1] = int(trans[1])
        trans[4] = float(trans[4])
        minerfee = float(rpc.estimatesmartfee(6)["feerate"])
        kilobytespertrans = 0.200
        amo = (trans[4] - (minerfee * kilobytespertrans))
        amo = "{:.8f}".format(float(amo))
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createrawtransaction \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\' \'[{"'+trans[5]+'" : '+str(amo)+'}]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(response[0]) == 0): 
            response = response[0].decode("utf-8")
        else:
            print(response)
            return "error response from createrawtransaction: " + str(response[1]) + '\n' + '~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createrawtransaction \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\' \'[{"'+trans[5]+'" : '+str(amo)+'}]\''
        transthreehex = response[:-1]
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli signrawtransactionwithwallet '+transthreehex+' \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(response[0]) == 0): 
            response = json.loads(response[0].decode("utf-8"))
        else:
            print(response)
            return "error response from signrawtransactionwithwallet: " + str(response[1]) + '\n' + '~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli signrawtransactionwithwallet '+transthreehex+' \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\''
        transthree = response
        thirdqrcode = transthree
    if request.method == 'POST':
        return redirect('/step43')
    return render_template('YWstep42.html')

@app.route("/step43", methods=['GET', 'POST'])
def step43():
    global firstqrcode
    global secondqrcode
    global thirdqrcode
    if request.method == 'GET':
        parsedfirstqrcode = firstqrcode.decode("utf-8").split('\'')[3]
        parsedsecondqrcode = secondqrcode.decode("utf-8").split('\'')[3]
        parsedthirdqrcode = thirdqrcode.decode("utf-8").split('\'')[3]
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli sendrawtransaction '+parsedfirstqrcode+''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(response[1]) == 0): 
            print(response)
            return "error response from sendrawtransaction: " + str(response[1]) + '\n' + '~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli sendrawtransaction '+parsedfirstqrcode+''
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli sendrawtransaction '+parsedsecondqrcode+''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(response[1]) == 0): 
            print(response)
            return "error response from sendrawtransaction: " + str(response[1]) + '\n' + '~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli sendrawtransaction '+parsedsecondqrcode+''
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli sendrawtransaction '+parsedthirdqrcode+''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(response[1]) == 0): 
            print(response)
            return "error response from sendrawtransaction: " + str(response[1]) + '\n' + '~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli sendrawtransaction '+parsedthirdqrcode+''
    if request.method == 'POST':
        return redirect('/step44')
    return render_template('YWstep43.html')

## extra pages
@app.route("/step44", methods=['GET', 'POST'])
def step44():
    if request.method == 'POST':
        return redirect('/step45')
    return render_template('YWstep44.html')

#dispaly qr codes
@app.route("/step45", methods=['GET', 'POST'])
def step45():
    global adrlist
    global color
    addresses = []
    if request.method == 'GET':
        for i in range(0, len(adrlist)):
            randomnum = str(random.randrange(0,1000000))
            route = url_for('static', filename='address'+randomnum+'.png')
            rpc = RPC()
            testlist = []
            testlist.append(adrlist[i])
            response = rpc.listunspent(0, 9999999, testlist)
            if response == []:
                bal = "0.0000000"
            else:
                bal = str(response[0]['amount'])
            utxocount = len(response)
            bal = "{:.8f}".format(float(bal))
            address['address'] = adrlist[i]
            address['balance'] = bal
            address['numbal'] = float(bal)
            address['route'] = route
            addresses.append(address)
        addresses.sort(key=lambda x: x['balance'], reverse=True)
        for i in range(0, len(addresses)):
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(addresses[i]['address'])
            qr.make(fit=True)
            color = '#b8daff'
            if (i % 2) == 0:
                color = 'white'
            img = qr.make_image(fill_color="black", back_color=color)
            home = os.getenv("HOME")
            img.save(home + '/yeticold/'+addresses[i]['route'])
    if request.method == 'POST':
        return redirect('/step')
    return render_template('YWstep45.html', addresses=addresses, len=len(addresses))
### END OF ONLINE

@app.route("/step")
def step():
    return "This page has not been added yet"

if __name__ == "__main__":
    app.run()
