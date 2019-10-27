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
import datetime
import ast
app = Flask(__name__)


### VARIBALES START

wallet_template = "http://{rpc_username}:{rpc_password}@{rpc_host}:{rpc_port}/wallet/{wallet_name}"
settings = {
    "rpc_username": "rpcuser",
    "rpc_password": "somesecretpassword",
    "rpc_host": "127.0.0.1",
    "rpc_port": 8332,
    "address_chunk": 100
}
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
base_count = len(BASE58_ALPHABET)
privkeylist = []
xprivlist = []
adrlist = []
firstqrcode = 0
secondqrcode = 0
error = None
thirdqrcode = 0
privkeycount = 0
firstqrname = None
secondqrname = None
thirdqrname = None
machine = 0
amount = 0
transnum = 0
utxo = None
currentsecondset = 0
bitcoindprogress = 0
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
    "J": "JULIET",
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
    "j": "juliet",
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
    "JULIET": "J",
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
    "juliet": "j",
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
def overview():
    if request.method == 'POST':
        return redirect('/options')
    return render_template('overview.html')

@app.route("/options", methods=['GET', 'POST'])
def options():
    global machine
    if request.method == 'POST':
        if request.form['option'] == 'start':
            return redirect('/items')
        elif request.form['option'] == 'mid':
            subprocess.call('gnome-terminal -- bash -c "~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-qt -proxy=127.0.0.1:9050; read line"', shell=True)
            machine = 1
            return redirect('/runbitcoind')
        elif request.form['option'] == 'end':
            subprocess.call('gnome-terminal -- bash -c "~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-qt -proxy=127.0.0.1:9050; read line"', shell=True)
            return redirect('/runbitcoind')
    return render_template('options.html')

### HOSTED WEBPAGE START

@app.route("/items", methods=['GET', 'POST'])
def items():
    if request.method == 'POST':
        return redirect('/label')
    return render_template('items.html')

@app.route("/label", methods=['GET', 'POST'])
def label():
    if request.method == 'POST':
        return redirect('/install')
    return render_template('label.html')

@app.route("/install", methods=['GET', 'POST'])
def install():
    if request.method == 'POST':
        return redirect('/download')
    return render_template('install.html')

@app.route("/download", methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        return redirect('/jone')
    return render_template('download.html')

@app.route("/jone", methods=['GET', 'POST'])
def jone():
    if request.method == 'POST':
        return redirect('/jtwo')
    return render_template('jone.html')

@app.route("/jtwo", methods=['GET', 'POST'])
def jtwo():
    if request.method == 'POST':
        return redirect('/jthree')
    return render_template('jtwo.html')

@app.route("/jthree", methods=['GET', 'POST'])
def jthree():
    if request.method == 'POST':
        return redirect('/jfour')
    return render_template('jthree.html')

@app.route("/jfour")
def jfour():
    return render_template('jfour.html')


### HOSTED WEBPAGE STOP

@app.route("/runbitcoind", methods=['GET', 'POST'])
def runbitcoind():
    global bitcoindprogress
    global machine
    global privkeycount
    if request.method == 'GET':
        bitcoind = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli getblockchaininfo'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(bitcoind[0]) == 0):
            bitcoindprogress = json.loads(bitcoind[0])['verificationprogress']
            bitcoindprogress = bitcoindprogress * 100
            bitcoindprogress = round(bitcoindprogress, 3)
        else:
            bitcoindprogress = 0
    if request.method == 'POST':
        if bitcoindprogress >= 99:
            if machine == 1:
                return redirect('/randomisePrivKey')
            elif machine == 2:
                privkeycount = 0
                privkeylist = []
                return redirect('/importprivkey')
            else:
                return redirect('/repack')
        else:
            return redirect('/runbitcoind')
    return render_template('runbitcoind.html', progress=bitcoindprogress)


### OFFLINE COMPUTER START

@app.route('/randomisePrivKey', methods=['GET', 'POST'])
def randomisePrivKey():
    global privkeylist
    global privkeycount
    global adrlist
    if request.method == 'POST':
        privkeylisttemp = []
        for i in range(1,8):
            rpc = RPC()
            print('1')
            adr = rpc.getnewaddress()
            print('2')
            newprivkey = rpc.dumpprivkey(adr)
            print('3')
            binary = bin(decode58(newprivkey))[2:][8:-40]
            print('4')
            WIF = ConvertToWIF(xor(binary,request.form['binary' + str(i)]))
            print('5')
            privkeylisttemp.append(WIF)
            print('6')
        privkeycount = 0
        privkeylist = privkeylisttemp
        adrlist = []
        return redirect('/generatemultisig')
    return render_template('randomisePrivKey.html')

@app.route("/generatemultisig", methods=['GET', 'POST'])
def generatemultisig():
    global privkeylist
    global adrlist
    global firstqrcode
    global secondqrcode
    global xprivlist
    ###### MULTI CREATE CODE
    if request.method == 'POST':
        for i in range(0,7):
            home = os.getenv('HOME')
            pathtwo = home + '/blank' + str(i)
            path = home + '/full' + str(i)
            response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli createwallet "full'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli loadwallet "full'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=full'+str(i)+' sethdseed false "'+privkeylist[i]+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=full'+str(i)+' dumpwallet "full'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            wallet = open(path,'r')
            wallet.readline()
            wallet.readline()
            wallet.readline()
            wallet.readline()
            wallet.readline()
            privkeyline = wallet.readline()
            privkeyline = privkeyline.split(" ")[4][:-1]
            xprivlist.append(privkeyline)
            response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli createwallet "blank'+str(i)+'" false true'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli loadwallet "blank'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=blank'+str(i)+' sethdseed false "'+privkeylist[i]+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=blank'+str(i)+' dumpwallet "blank'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            wallettwo = open(pathtwo,'r')
            wallettwo.readline()
            wallettwo.readline()
            wallettwo.readline()
            wallettwo.readline()
            wallettwo.readline()
            privkeytwoline = wallettwo.readline()
            privkeytwoline = privkeytwoline.split(" ")[4][:-1]
            if xprivlist[i] == privkeytwoline:
                print("OK")
        addresses = []
        checksum = None
        response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli getdescriptorinfo "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        response = response[0].decode("utf-8")
        response = json.loads(response)
        checksum = response["checksum"]
        desc = response["descriptor"]
        print("Descriptor public")
        print(desc)
        response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        for i in range(0,7):
            response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli getdescriptorinfo "pk('+xprivlist[i]+'/*)"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            response = response[0].decode("utf-8")
            privkeychecksum = json.loads(response)["checksum"]
            response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli deriveaddresses "pk('+xprivlist[i]+'/*)#'+privkeychecksum+'" "[0,999]"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            response = response[0].decode("utf-8")
            response = json.loads(response)
            addresses.append(response)
            for x in range(0,len(addresses[i])):
                response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli dumpprivkey "'+addresses[i][x]+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                response = response[0][:-1].decode("utf-8")
                noresponse = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli importprivkey "'+response+'" "" false'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        firstqrcode = desc
        secondqrcode = '~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "'+desc+'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''
        return redirect('/displayfirstqrcode')
    return render_template('generatemultisig.html')

@app.route("/displayfirstqrcode", methods=['GET', 'POST'])
def displayfirstqrcode():
    global privkeylist
    global adrlist
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
        img.save(home + '/flaskapp/static/firstqrcode' + firstqrname + '.png')
        route = url_for('static', filename='firstqrcode' + firstqrname + '.png')
    if request.method == 'POST':
        return redirect('/displaysecondqrcode')
    return render_template('displayfirstqrcode.html', qrdata=firstqrcode, route=route)

@app.route("/displaysecondqrcode", methods=['GET', 'POST'])
def displaysecondqrcode():
    global privkeylist
    global adrlist
    global secondqrcode
    global secondqrname
    if request.method == 'GET':
        randomnum = str(random.randrange(0,1000000))
        secondqrname = randomnum
        qr = qrcode.QRCode(
               version=1,
               error_correction=qrcode.constants.ERROR_CORRECT_L,
               box_size=10,
               border=4,
        )
        qr.add_data(secondqrcode)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        home = os.getenv("HOME")
        img.save(home + '/flaskapp/static/secondqrcode' + secondqrname + '.png')
        route = url_for('static', filename='secondqrcode' + secondqrname + '.png')
    if request.method == 'POST':
        return redirect('/display')
    return render_template('displaysecondqrcode.html', qrdata=secondqrcode, route=route)


## PAUSE OFFLINE COMPUTER AND CONTINUE ONLINE COMPUTER

@app.route('/display', methods=['GET', 'POST'])
def display():
    global privkeylist
    global privkeycount
    privkey = privkeylist[privkeycount]
    passphraselist = ConvertToPassphrase(privkey)
    if request.method == 'POST':
        privkeycount = privkeycount + 1
        if (privkeycount == 7):
            privkeycount = 0
            return redirect('/confirmkey')
        else:
            return redirect('/display')
        return redirect('/confirmkey')
    return render_template('display.html', PPL=passphraselist, x=privkeycount + 1)

@app.route('/confirmkey', methods=['GET', 'POST'])
def confirmkey():
    global privkeylist
    global privkeycount
    global error
    privkey = privkeylist[privkeycount]
    passphraselist = ConvertToPassphrase(privkey)
    if request.method == 'POST':
        privkeylisttoconfirm = ''
        for i in range(1,14):
            inputlist = request.form['row' + str(i)]
            inputlist = inputlist.split(' ')
            inputlist.pop()
            inputlist = " ".join(inputlist)
            privkeylisttoconfirm = privkeylisttoconfirm + ' ' + inputlist
        if PassphraseToWIF(privkeylisttoconfirm.split(' ')[1:]) == privkey:
            print(privkey)
            error = None
            privkeycount = privkeycount + 1
            if (privkeycount == 7):
                return redirect('/delwallet')
            else:
                return redirect('/confirmkey')
        else:
            error = 'You enterd the private key incorrectly but the checksums checked out please try agian'
    return render_template('confirmkey.html', x=privkeycount + 1, error=error)

### OFFLINE COMPUTER STOP

@app.route("/next")
def next():
    return "This page has not been added yet"

### ONLINE COMPUTER START

@app.route("/repack", methods=['GET', 'POST'])
def repack():
    if request.method == 'GET':
        subprocess.call(['gnome-terminal -- bash -c "sudo chmod +x ~/flaskapp/rpkg-script.sh; sudo ~/flaskapp/rpkg-script.sh; read line"'],shell=True)
    if request.method == 'POST':
        return redirect('/scanfirstqrcode')
    return render_template('repack.html')

## PAUSE ONLINE AND GO TO OFFLINE COMPUTER

@app.route("/scanfirstqrcode", methods=['GET', 'POST'])
def scanfirstqrcode():
    if request.method == 'POST':
        global firstqrcode
        firstqrcode = subprocess.Popen(['python3 ~/flaskapp/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        firstqrcode = firstqrcode.decode("utf-8")
        return redirect('/scansecondqrcode')
    return render_template('scanfirstqrcode.html')

@app.route("/scansecondqrcode", methods=['GET', 'POST'])
def scansecondqrcode():
    if request.method == 'POST':
        global secondqrcode
        secondqrcode = subprocess.Popen(['python3 ~/flaskapp/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        print(secondqrcode)
        secondqrcode = secondqrcode.decode("utf-8")
        print(secondqrcode)
        return redirect('/displayforprint')
    return render_template('scansecondqrcode.html')

@app.route("/displayforprint", methods=['GET', 'POST'])
def displayforprint():
    global firstqrcode
    global secondqrcode
    global firstqrname
    global secondqrname
    global currentsecondset
    randomnum = str(random.randrange(0,1000000))
    firstqrname = randomnum
    secondqrname = randomnum
    thirdqrname = randomnum
    routeone = url_for('static', filename='firstqrcode' + firstqrname + '.png')
    routetwo = url_for('static', filename='secondqrcode' + secondqrname + '.png')
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
        img.save(home + '/flaskapp/static/firstqrcode' + firstqrname + '.png')
        qr = qrcode.QRCode(
               version=1,
               error_correction=qrcode.constants.ERROR_CORRECT_L,
               box_size=10,
               border=4,
        )
        qr.add_data(secondqrcode)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        home = os.getenv("HOME")
        img.save(home + '/flaskapp/static/secondqrcode' + secondqrname +'.png')
    if request.method == 'POST':
        return redirect('/watchonly')
    return render_template('displayforprint.html', first=firstqrcode, second=secondqrcode, routeone=routeone, routetwo=routetwo)

@app.route("/watchonly", methods=['GET', 'POST'])
def watchonly():
    ##### watch only code
    global firstqrcode
    global firstqrname
    if request.method == 'GET':
        firstqrcode = firstqrcode[:-2]
        print(firstqrcode)
        response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "'+firstqrcode+'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli deriveaddresses "'+firstqrcode+'" "[0,999]"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        response = response[0].decode("utf-8")
        response = json.loads(response)
        randomnum = str(random.randrange(0,1000000))
        firstqrname = randomnum
        firstqrcode = response[0]
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
        img.save(home + '/flaskapp/static/firstqrcode' + firstqrname + '.png')
        rpc = RPC()
        for i in range(0,999):
            subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli importaddress "'+response[i]+'" "" false'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if request.method == 'POST':
        return redirect('/bitcoinqt')
    return render_template('watchonly.html', routeone=routeone, first=firstqrcode)

@app.route("/bitcoinqt", methods=['GET', 'POST'])
def bitcoinqt():
    if request.method == 'POST':
        return redirect('/displayutxo')
    return render_template('bitcoinqt.html')

@app.route("/displayutxo", methods=['GET', 'POST'])
def displayutxo():
    global utxo
    global secondqrname
    if request.method == 'GET':
        ##### get utxo code
        rpc = RPC()
        utxo = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli listunspent'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        utxo = json.loads(utxo[0])[0]
        print(utxo)
        newstr = utxo['txid'] + ','
        newstr = newstr + str(utxo['vout']) + ','
        newstr = newstr + utxo['address'] + ','
        newstr = newstr + utxo['scriptPubKey'] + ','
        newstr = newstr + str(utxo['amount']) + ','
        newstr = newstr + rpc.getnewaddress() + ','
        newstr = newstr + utxo['witnessScript']
        randomnum = str(random.randrange(0,1000000))
        secondqrname = randomnum
        qr = qrcode.QRCode(
               version=1,
               error_correction=qrcode.constants.ERROR_CORRECT_L,
               box_size=10,
               border=4,
        )
        qr.add_data(newstr)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        home = os.getenv("HOME")
        img.save(home + '/flaskapp/static/utxoqrcode'+secondqrname+'.png')
        route = url_for('static', filename='utxoqrcode' + secondqrname + '.png')
    if request.method == 'POST':
        return redirect('/scanfirsttransqrcode')
    return render_template('displayutxo.html', qrdata=newstr, route=route)

@app.route("/scanfirsttransqrcode", methods=['GET', 'POST'])
def scanfirsttransqrcode():
    if request.method == 'POST':
        global firstqrcode
        firstqrcode = subprocess.Popen(['python3 ~/flaskapp/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        return redirect('/scansecondtransqrcode')
    return render_template('scanfirsttransqrcode.html')

@app.route("/scansecondtransqrcode", methods=['GET', 'POST'])
def scansecondtransqrcode():
    if request.method == 'POST':
        global secondqrcode
        secondqrcode = subprocess.Popen(['python3 ~/flaskapp/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        return redirect('/scanthirdtransqrcode')
    return render_template('scansecondtransqrcode.html')

@app.route("/scanthirdtransqrcode", methods=['GET', 'POST'])
def scanthirdtransqrcode():
    if request.method == 'POST':
        global thirdqrcode
        thirdqrcode = subprocess.Popen(['python3 ~/flaskapp/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        return redirect('/checktrans')
    return render_template('scanthirdtransqrcode.html')

@app.route("/checktrans", methods=['GET', 'POST'])
def checktrans():
    global firstqrcode
    global secondqrcode
    global thirdqrcode
    if request.method == 'GET':
        firstqrcode = firstqrcode.decode("utf-8")
        secondqrcode = secondqrcode.decode("utf-8")
        thirdqrcode = thirdqrcode.decode("utf-8")
        rpc = RPC()
        rpc.sendrawtransaction(firstqrcode)
        rpc.sendrawtransaction(secondqrcode)
        rpc.sendrawtransaction(thirdqrcode)
    if request.method == 'POST':
        return redirect('/next')
    return render_template('checktrans.html')

@app.route("/delwallet", methods=['GET', 'POST'])
def delwallet():
    global machine
    if request.method == 'POST':
        subprocess.call('gnome-terminal -- bash -c "sudo python3 ~/flaskapp/deleteallwallets.py; echo "DONE"; read line"', shell=True)
        return redirect('/openbitcoinqt')
    return render_template('delwallet.html')

@app.route("/openbitcoinqt", methods=['GET', 'POST'])
def openbitcoinqt():
    global machine
    if request.method == 'POST':
        subprocess.call('gnome-terminal -- bash -c "~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-qt -proxy=127.0.0.1:9050; read line"', shell=True)
        machine = 2
        return redirect('/runbitcoind')
    return render_template('openbitcoinqt.html')

@app.route('/importprivkey', methods=['GET', 'POST'])
def importprivkey():
    global privkeylist
    global xprivlist
    global privkeycount
    global error 
    #####ISSUE
    if request.method == 'GET':
        newxprivlist = []
        privkeylist = []
        xprivlist = []
        for i in range(0,7):
            rpc = RPC()
            home = os.getenv('HOME')
            path = home + '/blank' + str(i)
            response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli createwallet "blank'+str(i)+'" false true'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli loadwallet "blank'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=blank'+str(i)+' sethdseed false "'+privkeylist[i]+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=blank'+str(i)+' dumpwallet "blank'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            wallet = open(path,'r')
            wallet.readline()
            wallet.readline()
            wallet.readline()
            wallet.readline()
            wallet.readline()
            privkeyline = wallet.readline()
            privkeyline = privkeyline.split(" ")[4][:-1]
            newxprivlist.append(privkeyline)
            print(i)
            print(newxprivlist)
            print(xprivlist)
            if not xprivlist[i] == newxprivlist[i]:
                privkeycount = 0
                privkeylist = []
                print('You have imported one of your keys incorrectly please try agian. key: ' + str(i))
        return redirect('/scanfirstutxoqrcode')
    if request.method == 'POST':
        privkeyphraselist = []
        for i in range(1,14):
            inputlist = request.form['row' + str(i)]
            inputlist = inputlist.split(' ')
            inputlist.pop()
            privkeyphraselist.append(inputlist[0])
            privkeyphraselist.append(inputlist[1])
            privkeyphraselist.append(inputlist[2])
            privkeyphraselist.append(inputlist[3])
        privkeylist.append(str(PassphraseToWIF(privkeyphraselist)))
        privkeycount = privkeycount + 1
        if (privkeycount == 7):
            newxprivlist = []
            for i in range(0,7):
                rpc = RPC()
                home = os.getenv('HOME')
                path = home + '/blank' + str(i)
                response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli createwallet "blank'+str(i)+'" false true'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli loadwallet "blank'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=blank'+str(i)+' sethdseed false "'+privkeylist[i]+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=blank'+str(i)+' dumpwallet "blank'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                wallet = open(path,'r')
                wallet.readline()
                wallet.readline()
                wallet.readline()
                wallet.readline()
                wallet.readline()
                privkeyline = wallet.readline()
                privkeyline = privkeyline.split(" ")[4][:-1]
                newxprivlist.append(privkeyline)
                print(i)
                print(newxprivlist)
                print(xprivlist)
                if not xprivlist[i] == newxprivlist[i]:
                    privkeycount = 0
                    privkeylist = []
                    error = 'You have imported one of your keys incorrectly please try agian'
                    return redirect('/importprivkey')
            return redirect('/scanfirstutxoqrcode')
        else:
            return redirect('/importprivkey')
    return render_template('importprivkey.html', x=privkeycount + 1, error=error)

@app.route("/scanfirstutxoqrcode", methods=['GET', 'POST'])
def scanfirstutxoqrcode():
    if request.method == 'POST':
        global firstqrcode
        firstqrcode = subprocess.Popen(['python3 ~/flaskapp/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        return redirect('/scansecondutxoqrcode')
    return render_template('scanfirstutxoqrcode.html')

@app.route("/scansecondutxoqrcode", methods=['GET', 'POST'])
def scansecondutxoqrcode():
    if request.method == 'POST':
        global secondqrcode
        secondqrcode = subprocess.Popen(['python3 ~/flaskapp/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        return redirect('/displayfirsttransqrcode')
    return render_template('scansecondutxoqrcode.html')

@app.route("/restartwallet", methods=['GET', 'POST'])
def restartwallet():
    global machine
    global transnum
    if request.method == 'POST':
        subprocess.call('gnome-terminal -- bash -c "sudo python3 ~/flaskapp/deleteallwallets.py; echo "DONE"; read line"', shell=True)
        response = subprocess.Popen(['sudo python3 ~/flaskapp/deleteallwallets.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if transnum == 0:
            return redirect('/displayfirsttransqrcode')
        elif transnum == 1:
            return redirect('/displaysecondtransqrcode')
        else:
            return redirect('/displaythirdtransqrcode')
    return render_template('restartwallet.html')

@app.route("/displayfirsttransqrcode", methods=['GET', 'POST'])
def displayfirsttransqrcode():
    global firstqrcode
    global secondqrcode
    global thirdqrcode
    global firstqrname
    global secondqrname
    global thirdqrname
    global privkeylist
    global xprivlist
    global transnum
    global amount
    ##### GEN TRANS CODE
    #############SPLIT THE TRANS QRCODES INTO THREE DIFFRENT SECTIONS AND DELET CURRENT WALLET.DAT .WALLETLOCK AND ALL OTHER WALLET FOLDERS
    if request.method == 'GET':
        response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli getdescriptorinfo "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*))"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        response = response[0].decode("utf-8")
        response = json.loads(response)
        checksum = response["checksum"]
        response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        rpc = RPC()
        trans = firstqrcode #### parse this
        trans = trans.decode("utf-8")
        trans = trans.split(",")
        trans[1] = int(trans[1])
        trans[4] = float(trans[4])
        print(secondqrcode)
        #trans[0] = txid
        #trans[1] = vout
        #trans[2] = changeaddress
        #trans[3] = scrirptPubKey
        #trans[4] = amount
        #trans[5] = recpipentaddress
        #trans[6] = witnessScript
        minerfee = float(rpc.estimatesmartfee(6)["feerate"])
        kilobytespertrans = 0.01
        amo = ((trans[4] / 3) - (minerfee * kilobytespertrans))
        amount = (trans[4] * (2 / 3))
        amo = "{:.8f}".format(float(amo))
        newamo = "{:.8f}".format(float(amount))
        transonehex = rpc.createrawtransaction([{ "txid": trans[0], "vout": trans[1], "scriptPubKey": trans[3]}], [{trans[5] : amo}, {trans[2] : newamo }])
        print(transonehex)
        transone = rpc.signrawtransactionwithwallet(transonehex, [{ "txid": trans[0], "vout": trans[1], "scriptPubKey": trans[3], "witnessScript": trans[6], "amount": trans[4]}])
        print(transone)
        firstqrcode = transone
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
        img.save(home + '/flaskapp/static/firsttransqrcode'+firstqrname+'.png')
        route = url_for('static', filename='firsttransqrcode' + firstqrname + '.png')
    if request.method == 'POST':
        transnum = 1
        return redirect('/restartwallet')
    return render_template('displayfirsttransqrcode.html', qrdata=firstqrcode, route=route)

@app.route("/displaysecondtransqrcode", methods=['GET', 'POST'])
def displaysecondtransqrcode():
    global firstqrcode
    global secondqrcode
    global thirdqrcode
    global firstqrname
    global secondqrname
    global thirdqrname
    global privkeylist
    global xprivlist
    global transnum
    global amount
    ##### GEN TRANS CODE
    if request.method == 'GET':
        response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli getdescriptorinfo "wsh(multi(3,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xprivlist[5]+'/*))"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        response = response[0].decode("utf-8")
        response = json.loads(response)
        checksum = response["checksum"]
        response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "wsh(multi(3,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xprivlist[5]+'/*))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        rpc = RPC()
        trans = firstqrcode #### parse this
        trans = trans.decode("utf-8")
        trans = trans.split(",")
        trans[1] = int(trans[1])
        trans[4] = float(trans[4])
        #trans[0] = txid
        #trans[1] = vout
        #trans[2] = changeaddress
        #trans[3] = scrirptPubKey
        #trans[4] = amount
        #trans[5] = recpipentaddress
        #trans[6] = witnessScript
        minerfee = float(rpc.estimatesmartfee(6)["feerate"])
        kilobytespertrans = 0.01
        amo = ((trans[4] / 3) - (minerfee * kilobytespertrans))
        amo = "{:.8f}".format(float(amo))
        newamo = (trans[4] * (1 / 3))
        newamo = "{:.8f}".format(float(newamo))
        transtwohex = rpc.createrawtransaction([{ "txid": trans[0], "vout": trans[1], "scriptPubKey": trans[3]}], [{trans[5] : amo}, {trans[2] : newamo }])
        print(transtwohex)
        transtwo = rpc.signrawtransactionwithwallet(transtwohex, [{ "txid": trans[0], "vout": trans[1], "scriptPubKey": trans[3], "witnessScript": trans[6], "amount": trans[4]}])
        print(transtwo)
        secondqrcode = transtwo
        randomnum = str(random.randrange(0,1000000))
        secondqrname = randomnum
        qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        )
        qr.add_data(secondqrcode)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        home = os.getenv("HOME")
        img.save(home + '/flaskapp/static/secondtransqrcode'+secondqrcode+'.png')
        route = url_for('static', filename='secondtransqrcode' + secondqrname + '.png')
    if request.method == 'POST':
        transnum = 2
        return redirect('/restartwallet')
    return render_template('displaysecondtransqrcode.html', qrdata=secondqrcode, route=route)

@app.route("/displaythirdtransqrcode", methods=['GET', 'POST'])
def displaythirdtransqrcode():
    global firstqrcode
    global secondqrcode
    global thirdqrcode
    global firstqrname
    global secondqrname
    global thirdqrname
    global privkeylist
    global xprivlist
    global transnum
    global amount
    if request.method == 'GET':
        response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli getdescriptorinfo "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[3]+'/*,'+xprivlist[6]+'/*))"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        response = response[0].decode("utf-8")
        response = json.loads(response)
        checksum = response["checksum"]
        response = subprocess.Popen(['~/flaskapp/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[3]+'/*,'+xprivlist[6]+'/*))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        rpc = RPC()
        trans = firstqrcode #### parse this
        trans = trans.decode("utf-8")
        trans = trans.split(",")
        trans[1] = int(trans[1])
        trans[4] = float(trans[4])
        #trans[0] = txid
        #trans[1] = vout
        #trans[2] = changeaddress
        #trans[3] = scrirptPubKey
        #trans[4] = amount
        #trans[5] = recpipentaddress
        #trans[6] = witnessScript
        minerfee = float(rpc.estimatesmartfee(6)["feerate"])
        kilobytespertrans = 0.01
        amo = ((trans[4] / 3) - (minerfee * kilobytespertrans))
        amo = "{:.8f}".format(float(amo))
        newamo = 0
        transthreehex = rpc.createrawtransaction([{ "txid": trans[0], "vout": trans[1], "scriptPubKey": trans[3]}], [{trans[5] : amo}, {trans[2] : newamo }])
        print(transthreehex)
        transthree = rpc.signrawtransactionwithwallet(transtwohex, [{ "txid": trans[0], "vout": trans[1], "scriptPubKey": trans[3], "witnessScript": trans[6], "amount": trans[4]}])
        print(transthree)
        thirdqrcode = transthree
        randomnum = str(random.randrange(0,1000000))
        thirdqrname = randomnum
        qr = qrcode.QRCode(
               version=1,
               error_correction=qrcode.constants.ERROR_CORRECT_L,
               box_size=10,
               border=4,
        )
        qr.add_data(thirdqrcode)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        home = os.getenv("HOME")
        img.save(home + '/flaskapp/static/thirdtransqrcode'+thirdqrname+'.png')
        route = url_for('static', filename='thirdtransqrcode' + thirdqrname + '.png')
    if request.method == 'POST':
        return redirect('/next')
    return render_template('displaythirdtransqrcode.html', qrdata=thirdqrcode, route=route)

### ONLINE COMPUTER START

if __name__ == "__main__":
    app.run()