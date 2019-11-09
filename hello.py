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
transnum = 0
utxo = None
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
    home = os.getenv('HOME')
    if request.method == 'POST':
        if request.form['option'] == 'start':
            return redirect('/step01')
        elif request.form['option'] == 'mid':
            return redirect('/step11')
        elif request.form['option'] == 'end':
            return redirect('/step07')
    return render_template('options.html')

### START HOSTED GETTING STARTED
@app.route("/step01", methods=['GET', 'POST'])
def step01():
    if request.method == 'POST':
        return redirect('/step02')
    return render_template('step01.html')

@app.route("/step02", methods=['GET', 'POST'])
def step02():
    if request.method == 'POST':
        return redirect('/step03')
    return render_template('step02.html')

@app.route("/step03", methods=['GET', 'POST'])
def step03():
    if request.method == 'POST':
        return redirect('/step04')
    return render_template('step03.html')

@app.route("/step04", methods=['GET', 'POST'])
def step04():
    return render_template('step04.html')
##STOP

###START HOSTED ONLINE
@app.route("/step05", methods=['GET', 'POST'])
def step05():
    if request.method == 'POST':
        return redirect('/step06')
    return render_template('step05.html')

@app.route("/step06", methods=['GET', 'POST'])
def step06():
    return render_template('step06.html')
##STOP

### START ONLINE
@app.route("/step07", methods=['GET', 'POST'])
def step07():
    if request.method == 'POST':
        subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-qt -proxy=127.0.0.1:9050'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return redirect('/step08')
    return render_template('step07.html')

@app.route("/step08", methods=['GET', 'POST'])
def step08():
    if request.method == 'GET':
        bitcoind = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getblockchaininfo'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(bitcoind[0]) == 0):
            bitcoindprogress = json.loads(bitcoind[0])['verificationprogress']
            bitcoindprogress = bitcoindprogress * 100
            bitcoindprogress = round(bitcoindprogress, 3)
        else:
            bitcoindprogress = 0
    if request.method == 'POST':
        if bitcoindprogress >= 100:
            return redirect('/step09')
    return render_template('step08.html')

@app.route("/step09", methods=['GET', 'POST'])
def step09():
    if request.method == 'GET':
        subprocess.call(['gnome-terminal -- bash -c "sudo chmod +x ~/yeticold/rpkg-script.sh; sudo ~/yeticold/rpkg-script.sh"'],shell=True)
    if request.method == 'POST':
        return redirect('/step10')
    return render_template('step09.html')

@app.route("/step10", methods=['GET', 'POST'])
def step10():
    if request.method == 'POST':
        return redirect('/step15')
    return render_template('step10.html')
##SWIWCH TO OFFLINE

###STARTE OFFLINE
@app.route("/step11", methods=['GET', 'POST'])
def step11():
    if request.method == 'POST':
        subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-qt -proxy=127.0.0.1:9050'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return redirect('/step12')
    return render_template('step11.html')

@app.route('/step12', methods=['GET', 'POST'])
def step12():
    if request.method == 'GET':
        bitcoind = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getblockchaininfo'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(bitcoind[0]) == 0):
            bitcoindprogress = json.loads(bitcoind[0])['verificationprogress']
            bitcoindprogress = bitcoindprogress * 100
            bitcoindprogress = round(bitcoindprogress, 3)
        else:
            bitcoindprogress = 0
    if request.method == 'POST':
        if bitcoindprogress >= 99:
            return redirect('/step13')
    return render_template('step12.html')

@app.route("/step13", methods=['GET', 'POST'])
def step13():
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
            pathtwo = home + '/blank' + str(i)
            path = home + '/full' + str(i)
            response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createwallet "full'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli loadwallet "full'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=full'+str(i)+' sethdseed false "'+privkeylist[i]+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
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
        response = response[0].decode("utf-8")
        response = json.loads(response)
        checksum = response["checksum"]
        desc = response["descriptor"]
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli deriveaddresses "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))#'+ checksum +'" "[0,999]"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        response = response[0].decode("utf-8")
        addresses = json.loads(response)
        firstqrcode = desc
        secondqrcode = '~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "'+desc+'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''
        return redirect('/step14')
    return render_template('step13.html')

@app.route("/step14", methods=['GET', 'POST'])
def step14():
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
        route = url_for('static', filename='firstqrcode' + firstqrname + '.png')
    if request.method == 'POST':
        return redirect('/step2127')
    return render_template('step14.html', qrdata=firstqrcode, route=route)
##SWITCH TO ONLINE


@app.route("/step15", methods=['GET', 'POST'])
def step15():
    global firstqrcode
    if request.method == 'POST':
        firstqrcode = subprocess.Popen(['python3 ~/yeticold/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        firstqrcode = firstqrcode.decode("utf-8")
        return redirect('/step16')
    return render_template('step15.html')

@app.route("/step16", methods=['GET', 'POST'])
def step16():
    global firstqrcode
    global secondqrcode
    global firstqrname
    global secondqrname
    randomnum = str(random.randrange(0,1000000))
    firstqrname = randomnum
    secondqrname = randomnum
    thirdqrname = randomnum
    routeone = url_for('static', filename='firstqrcode' + firstqrname + '.png')
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
        return redirect('/step17')
    return render_template('step16.html', first=firstqrcode, routeone=routeone)

@app.route("/step17", methods=['GET', 'POST'])
def step17():
    global firstqrcode
    global firstqrname
    global pubdesc
    if request.method == 'GET':
        pubdesc = firstqrcode[:-1]
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "'+pubdesc+'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli deriveaddresses "'+pubdesc+'" "[0,999]"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
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
        img.save(home + '/yeticold/static/firstqrcode' + firstqrname + '.png')
    if request.method == 'POST':
        return redirect('/step18')
    return render_template('step17.html', routeone=routeone, first=firstqrcode)

@app.route("/step18", methods=['GET', 'POST'])
def step18():
    global pubdesc
    if request.method == 'GET':
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "'+pubdesc+'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli deriveaddresses "'+pubdesc+'" "[0,999]"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
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
        img.save(home + '/yeticold/static/firstqrcode' + firstqrname + '.png')
    if request.method == 'POST':
        return redirect('/step19')
    return render_template('step18.html', routeone=routeone, first=firstqrcode)

@app.route("/step19", methods=['GET', 'POST'])
def step19():
    global pubdesc
    if request.method == 'GET':
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "'+pubdesc+'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli deriveaddresses "'+pubdesc+'" "[0,999]"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
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
        img.save(home + '/yeticold/static/firstqrcode' + firstqrname + '.png')
    if request.method == 'POST':
        return redirect('/step20')
    return render_template('step19.html', routeone=routeone, first=firstqrcode)

@app.route("/step20", methods=['GET', 'POST'])
def step20():
    if request.method == 'POST':
        return redirect('/step39')
    return render_template('step20.html')
##SWITCH TO OFFLINE


@app.route('/step2127', methods=['GET', 'POST'])
def step2127():
    global privkeylist
    global privkeycount
    privkey = privkeylist[privkeycount]
    passphraselist = ConvertToPassphrase(privkey)
    if request.method == 'POST':
        privkeycount = privkeycount + 1
        if (privkeycount == 7):
            privkeycount = 0
            return redirect('/step28')
        else:
            return redirect('/step2127')
    return render_template('step21-27.html', PPL=passphraselist, x=privkeycount + 1, i=privkeycount + 21)

@app.route("/step28", methods=['GET', 'POST'])
def step28():
    if request.method == 'POST':
        subprocess.call('gnome-terminal -- bash -c "sudo python3 ~/yeticold/deleteallwallets.py; echo "DONE, Close this window.""', shell=True)
        return redirect('/step29')
    return render_template('step28.html')

@app.route("/step29", methods=['GET', 'POST'])
def step29():
    if request.method == 'POST':
        subprocess.call('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-qt -proxy=127.0.0.1:9050', shell=True)
        return redirect('/step30')
    return render_template('step29.html')

@app.route('/step30', methods=['GET', 'POST'])
def step30():
    if request.method == 'GET':
        bitcoind = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getblockchaininfo'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(bitcoind[0]) == 0):
            bitcoindprogress = json.loads(bitcoind[0])['verificationprogress']
            bitcoindprogress = bitcoindprogress * 100
            bitcoindprogress = round(bitcoindprogress, 3)
        else:
            bitcoindprogress = 0
    if request.method == 'POST':
        if bitcoindprogress >= 99:
            return redirect('/step3137')
    return render_template('step30.html')

@app.route('/step3137', methods=['GET', 'POST'])
def step3137():
    global privkeylist
    global xprivlist
    global privkeycount
    global error 
    if request.method == 'POST':
        privkey = privkeylist[privkeycount]
        passphraselist = ConvertToPassphrase(privkey)
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
                newxprivlist = []
                for i in range(0,7):
                    rpc = RPC()
                    home = os.getenv('HOME')
                    path = home + '/blank' + str(i)
                    response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createwallet "blank'+str(i)+'" false true'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                    response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli loadwallet "blank'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                    response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=blank'+str(i)+' sethdseed false "'+privkeylist[i]+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
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
                    print(i)
                    print(newxprivlist)
                    print(xprivlist)
                    if not xprivlist[i] == newxprivlist[i]:
                        privkeycount = 0
                        privkeylist = []
                        error = 'You have imported your seeds correctly but your xprivs do not match'
                        return redirect('/step3137')
                return redirect('/step38')
            else:
                return redirect('/step3137')
        else:
            error = 'You enterd the private key incorrectly but the checksums checked out please try agian'
    return render_template('step31-37.html', x=privkeycount + 1, error=error,i=privkeycount + 31 )

@app.route("/step38", methods=['GET', 'POST'])
def step38():
    if request.method == 'POST':
        global firstqrcode
        global utxoresponse
        firstqrcode = subprocess.Popen(['python3 ~/yeticold/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        utxoresponse = firstqrcode
        return redirect('/step40')
    return render_template('step38.html')
##SWITCH TO ONLINE


@app.route("/step39", methods=['GET', 'POST'])
def step39():
    global utxo
    global secondqrname
    if request.method == 'GET':
        rpc = RPC()
        utxo = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli listunspent'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        utxos = json.loads(utxo[0])
        utxo = utxos[0]
        print(utxo)
        newstr = utxo['txid'] + ','
        newstr = newstr + str(utxo['vout']) + ','
        newstr = newstr + utxo['address'] + ','
        newstr = newstr + utxo['scriptPubKey'] + ','
        newstr = newstr + str(utxo['amount']) + ','
        newstr = newstr + rpc.getnewaddress() + ','
        newstr = newstr + utxo['witnessScript'] + '&'
        utxoone = utxos[1]
        print(utxoone)
        newstr = newstr + utxoone['txid'] + ','
        newstr = newstr + str(utxoone['vout']) + ','
        newstr = newstr + utxoone['address'] + ','
        newstr = newstr + utxoone['scriptPubKey'] + ','
        newstr = newstr + str(utxoone['amount']) + ','
        newstr = newstr + rpc.getnewaddress() + ','
        newstr = newstr + utxoone['witnessScript'] + '&'
        utxotwo = utxos[2]
        print(utxotwo)
        newstr = newstr + utxotwo['txid'] + ','
        newstr = newstr + str(utxotwo['vout']) + ','
        newstr = newstr + utxotwo['address'] + ','
        newstr = newstr + utxotwo['scriptPubKey'] + ','
        newstr = newstr + str(utxotwo['amount']) + ','
        newstr = newstr + rpc.getnewaddress() + ','
        newstr = newstr + utxotwo['witnessScript']
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
        img.save(home + '/yeticold/static/utxoqrcode'+secondqrname+'.png')
        route = url_for('static', filename='utxoqrcode' + secondqrname + '.png')
    if request.method == 'POST':
        return redirect('/step45')
    return render_template('step39.html', qrdata=newstr, route=route)
##SWITCH TO OFFLINE


@app.route("/step40", methods=['GET', 'POST'])
def step40():
    if request.method == 'POST':
        global secondqrcode
        global pubdesc
        global transnum
        secondqrcode = subprocess.Popen(['python3 ~/yeticold/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        pubdesc = secondqrcode
        transnum = 1
        return redirect('/step41')
    return render_template('step40.html')

@app.route("/step41", methods=['GET', 'POST'])
def step41():
    global transnum
    if request.method == 'POST':
        subprocess.call('gnome-terminal -- bash -c "sudo python3 ~/yeticold/deleteallwallets.py; echo "DONE"; read line"', shell=True)
        return redirect('/step42')
    return render_template('step41.html')

@app.route("/step42", methods=['GET', 'POST'])
def step42():
    if request.method == 'POST':
        subprocess.call('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-qt -proxy=127.0.0.1:9050', shell=True)
        return redirect('/step43')
    return render_template('step42.html')

@app.route('/step43', methods=['GET', 'POST'])
def step43():
    if request.method == 'GET':
        bitcoind = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getblockchaininfo'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(bitcoind[0]) == 0):
            bitcoindprogress = json.loads(bitcoind[0])['verificationprogress']
            bitcoindprogress = bitcoindprogress * 100
            bitcoindprogress = round(bitcoindprogress, 3)
        else:
            bitcoindprogress = 0
    if request.method == 'POST':
        if bitcoindprogress >= 99:
            return redirect('/step44')
    return render_template('step43.html')

@app.route("/step44", methods=['GET', 'POST'])
def step44():
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
    ##### GEN TRANS CODE
    if request.method == 'GET':
        xpublist = pubdesc.decode("utf-8").split(',')[1:]
        print(xpublist)
        xpublist[6] = xpublist[6].split('))')[0]
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getdescriptorinfo "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xpublist[3]+','+xpublist[4]+','+xpublist[5]+','+xpublist[6]+'))"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getdescriptorinfo "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xpublist[3]+','+xpublist[4]+','+xpublist[5]+','+xpublist[6]+'))"')
        print("getdescriptorinfo")
        print(response)
        response = response[0].decode("utf-8")
        response = json.loads(response)
        checksum = response["checksum"]
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xpublist[3]+','+xpublist[4]+','+xpublist[5]+','+xpublist[6]+'))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xpublist[3]+','+xpublist[4]+','+xpublist[5]+','+xpublist[6]+'))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\'')
        print("importmulti")
        print(response)
        rpc = RPC()
        trans = utxoresponse
        print("trans start")
        print(trans)
        trans = trans.decode("utf-8")
        print("trans mid")
        print(trans)
        trans = trans.split("&")[0].split(",")
        print("trans end")
        print(trans)
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
        kilobytespertrans = 0.545
        amo = ((trans[4] / 3) - (minerfee * kilobytespertrans))
        amo = "{:.8f}".format(float(amo))
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createrawtransaction \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\' \'[{"'+trans[5]+'" : '+str(amo)+'}]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print()
        print('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createrawtransaction \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\' \'[{"'+trans[5]+'" : '+str(amo)+'}]\'')
        print(response)
        print("create raw transaction")
        transonehex = response[0].decode("utf-8")[:-1]
        print(transonehex)
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli signrawtransactionwithwallet '+transonehex+' \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+', "scriptPubKey": "'+trans[3]+'", "witnessScript": "'+trans[6][:-1]+'", "amount": "'+str(trans[4])+'" }]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli signrawtransactionwithwallet '+transonehex+' \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+', "scriptPubKey": "'+trans[3]+'", "witnessScript": "'+trans[6][:-1]+'", "amount": "'+str(trans[4])+'" }]\'')
        print("signrawtrans")
        print(response)
        print("result")
        transone = json.loads(response[0].decode("utf-8"))
        print(transone)
        firstqrcode = transone
        randomnum = str(random.randrange(0,1000000))
        firstqrname = randomnum
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
            )####DISPLAYING THE ADDRESS IS NOT COMPLEATED ON THE HTML SIDE
        qr.add_data(firstqrcode)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        home = os.getenv("HOME")
        img.save(home + '/yeticold/static/firsttransqrcode'+firstqrname+'.png')
        route = url_for('static', filename='firsttransqrcode' + firstqrname + '.png')
    if request.method == 'POST':
        transnum = 2
        return redirect('/step47')
    return render_template('step44.html', qrdata=firstqrcode, route=route)
##SWITCH TO ONLINE


@app.route("/step45", methods=['GET', 'POST'])
def step45():
    if request.method == 'POST':
        global firstqrcode
        firstqrcode = subprocess.Popen(['python3 ~/yeticold/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        return redirect('/step46')
    return render_template('step45.html')

@app.route("/step46", methods=['GET', 'POST'])
def step46():
    if request.method == 'POST':
        return redirect('/step51')
    return render_template('step46.html')
##SWITCH TO OFFLINE


@app.route("/step47", methods=['GET', 'POST'])
def step47():
    global transnum
    if request.method == 'POST':
        subprocess.call('gnome-terminal -- bash -c "sudo python3 ~/yeticold/deleteallwallets.py; echo "DONE"; read line"', shell=True)
        return redirect('/step48')
    return render_template('step47.html')

@app.route("/step48", methods=['GET', 'POST'])
def step48():
    if request.method == 'POST':
        subprocess.call('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-qt -proxy=127.0.0.1:9050', shell=True)
        return redirect('/step49')
    return render_template('step48.html')

@app.route('/step49', methods=['GET', 'POST'])
def step49():
    if request.method == 'GET':
        bitcoind = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getblockchaininfo'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(bitcoind[0]) == 0):
            bitcoindprogress = json.loads(bitcoind[0])['verificationprogress']
            bitcoindprogress = bitcoindprogress * 100
            bitcoindprogress = round(bitcoindprogress, 3)
        else:
            bitcoindprogress = 0
    if request.method == 'POST':
        if bitcoindprogress >= 99:
            return redirect('/step50')
    return render_template('step49.html')

@app.route("/step50", methods=['GET', 'POST'])
def step50():
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
    ##### GEN TRANS CODE
    if request.method == 'GET':
        xpublist = pubdesc.decode("utf-8").split(',')[1:]
        print(xpublist)
        xpublist[6] = xpublist[6].split('))')[0]
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getdescriptorinfo "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xpublist[5]+','+xpublist[6]+'))"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getdescriptorinfo "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xpublist[5]+','+xpublist[6]+'))"')
        print("getdescriptorinfo")
        print(response)
        response = response[0].decode("utf-8")
        response = json.loads(response)
        checksum = response["checksum"]
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xpublist[5]+','+xpublist[6]+'))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xpublist[5]+','+xpublist[6]+'))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\'')
        print("importmulti")
        print(response)
        rpc = RPC()
        trans = utxoresponse #### parse this
        print("trans start")
        print(trans)
        trans = trans.decode("utf-8")
        print("trans mid")
        print(trans)
        trans = trans.split("&")[1].split(",")
        print("trans end")
        print(trans)
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
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createrawtransaction \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\' \'[{"'+trans[5]+'" : '+str(amo)+'}]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print()
        print('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createrawtransaction \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\' \'[{"'+trans[5]+'" : '+str(amo)+'}]\'')
        print(response)
        print("create raw transaction")
        transtwohex = response[0].decode("utf-8")[:-1]
        print(transtwohex)
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli signrawtransactionwithwallet '+transtwohex+' \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+', "scriptPubKey": "'+trans[3]+'", "witnessScript": "'+trans[6][:-1]+'", "amount": "'+str(trans[4])+'" }]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli signrawtransactionwithwallet '+transtwohex+' \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+', "scriptPubKey": "'+trans[3]+'", "witnessScript": "'+trans[6][:-1]+'", "amount": "'+str(trans[4])+'" }]\'')
        print("signrawtrans")
        print(response)
        print("result")
        transtwo = json.loads(response[0].decode("utf-8"))
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
        img.save(home + '/yeticold/static/secondtransqrcode'+secondqrname+'.png')
        route = url_for('static', filename='secondtransqrcode' + secondqrname + '.png')
    if request.method == 'POST':
        transnum = 3
        return redirect('/step53')
    return render_template('step50.html', qrdata=firstqrcode, route=route)
##SWITCH TO ONLINE


@app.route("/step51", methods=['GET', 'POST'])
def step51():
    if request.method == 'POST':
        global secondqrcode
        secondqrcode = subprocess.Popen(['python3 ~/yeticold/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        return redirect('/step52')
    return render_template('step51.html')

@app.route("/step52", methods=['GET', 'POST'])
def step52():
    if request.method == 'POST':
        return redirect('/step57')
    return render_template('step52.html')
##SWITCH TO OFFLINE


@app.route("/step53", methods=['GET', 'POST'])
def step53():
    global transnum
    if request.method == 'POST':
        subprocess.call('gnome-terminal -- bash -c "sudo python3 ~/yeticold/deleteallwallets.py; echo "DONE"; read line"', shell=True)
        return redirect('/step54')
    return render_template('step53.html')

@app.route("/step54", methods=['GET', 'POST'])
def step54():
    if request.method == 'POST':
        subprocess.call('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-qt -proxy=127.0.0.1:9050', shell=True)
        return redirect('/step55')
    return render_template('step54.html')

@app.route('/step55', methods=['GET', 'POST'])
def step55():
    if request.method == 'GET':
        bitcoind = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getblockchaininfo'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if not (len(bitcoind[0]) == 0):
            bitcoindprogress = json.loads(bitcoind[0])['verificationprogress']
            bitcoindprogress = bitcoindprogress * 100
            bitcoindprogress = round(bitcoindprogress, 3)
        else:
            bitcoindprogress = 0
    if request.method == 'POST':
        if bitcoindprogress >= 99:
            return redirect('/step56')
    return render_template('step55.html')

@app.route("/step56", methods=['GET', 'POST'])
def step56():
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
    ##### GEN TRANS CODE
    if request.method == 'GET':
        xpublist = pubdesc.decode("utf-8").split(',')[1:]
        print(xpublist)
        xpublist[6] = xpublist[6].split('))')[0]
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getdescriptorinfo "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xpublist[2]+','+xpublist[3]+','+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getdescriptorinfo "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xpublist[2]+','+xpublist[3]+','+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))"')
        print("getdescriptorinfo")
        print(response)
        response = response[0].decode("utf-8")
        response = json.loads(response)
        checksum = response["checksum"]
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xpublist[2]+','+xpublist[3]+','+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "wsh(multi(3,'+xpublist[0]+','+xpublist[1]+','+xpublist[2]+','+xpublist[3]+','+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\'')
        print("importmulti")
        print(response)
        rpc = RPC()
        trans = utxoresponse #### parse this
        print("trans start")
        print(trans)
        trans = trans.decode("utf-8")
        print("trans mid")
        print(trans)
        trans = trans.split("&")[2].split(",")
        print("trans end")
        print(trans)
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
        amo = (trans[4] - (minerfee * kilobytespertrans))
        amo = "{:.8f}".format(float(amo))
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createrawtransaction \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\' \'[{"'+trans[5]+'" : '+str(amo)+'}]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print()
        print('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createrawtransaction \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\' \'[{"'+trans[5]+'" : '+str(amo)+'}]\'')
        print(response)
        print("create raw transaction")
        transthreehex = response[0].decode("utf-8")[:-1]
        print(transthreehex)
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli signrawtransactionwithwallet '+transthreehex+' \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+', "scriptPubKey": "'+trans[3]+'", "witnessScript": "'+trans[6][:-1]+'", "amount": "'+str(trans[4])+'" }]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli signrawtransactionwithwallet '+transthreehex+' \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+', "scriptPubKey": "'+trans[3]+'", "witnessScript": "'+trans[6][:-1]+'", "amount": "'+str(trans[4])+'" }]\'')
        print("signrawtrans")
        print(response)
        print("result")
        transthree = json.loads(response[0].decode("utf-8"))
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
        img.save(home + '/yeticold/static/thirdtransqrcode'+thirdqrname+'.png')
        route = url_for('static', filename='thirdtransqrcode' + thirdqrname + '.png')
    if request.method == 'POST':
        return redirect('/step')
    return render_template('step56.html', qrdata=firstqrcode, route=route)
##SWITCH TO ONLINE
### END OF OFFLINE


@app.route("/step57", methods=['GET', 'POST'])
def step57():
    if request.method == 'POST':
        global thirdqrcode
        global secondqrcode
        global thirdqrcode
        thirdqrcode = subprocess.Popen(['python3 ~/yeticold/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        print(firstqrcode)
        print(secondqrcode)
        print(thirdqrcode)
        return redirect('/step58')
    return render_template('step57.html')

@app.route("/step58", methods=['GET', 'POST'])
def step58():
    global firstqrcode
    global secondqrcode
    global thirdqrcode
    if request.method == 'GET':
        firstqrcode = firstqrcode.decode("utf-8")
        secondqrcode = secondqrcode.decode("utf-8")
        thirdqrcode = thirdqrcode.decode("utf-8")
        firstqrcode = firstqrcode.split('\'')[3]
        secondqrcode = secondqrcode.split('\'')[3]
        thirdqrcode = thirdqrcode.split('\'')[3]
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli sendrawtransaction '+firstqrcode+''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli sendrawtransaction '+secondqrcode+''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli sendrawtransaction '+thirdqrcode+''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
    if request.method == 'POST':
        return redirect('/step59')
    return render_template('step58.html')

@app.route("/step59", methods=['GET', 'POST'])
def step59():
    if request.method == 'POST':
        return redirect('/step60')
    return render_template('step59.html')

@app.route("/step60", methods=['GET', 'POST'])
def step60():
    if request.method == 'POST':
        return redirect('/step61')
    return render_template('step60.html')

@app.route("/step61", methods=['GET', 'POST'])
def step61():
    if request.method == 'POST':
        return redirect('/step')
    return render_template('step61.html')
### END OF ONLINE













@app.route("/step")
def step():
    return "This page has not been added yet"

###LEAVE CODE BELLOW UNTILL NEW FLOW IS CONFIRMED

# @app.route("/displayfirsttransqrcode", methods=['GET', 'POST'])
# def displayfirsttransqrcode():
#     global firstqrcode
#     global secondqrcode
#     global thirdqrcode
#     global firstqrname
#     global secondqrname
#     global thirdqrname
#     global privkeylist
#     global xprivlist
#     global transnum
#     global amount
#     global utxoresponse
#     global pubdesc
#     ##### GEN TRANS CODE
#     if request.method == 'GET':
#         xpublist = pubdesc.decode("utf-8").split(',')[1:]
#         print(xpublist)
#         xpublist[6] = xpublist[6].split('))')[0]
#         response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getdescriptorinfo "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xpublist[3]+','+xpublist[4]+','+xpublist[5]+','+xpublist[6]+'))"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#         print('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getdescriptorinfo "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xpublist[3]+','+xpublist[4]+','+xpublist[5]+','+xpublist[6]+'))"')
#         print("getdescriptorinfo")
#         print(response)
#         response = response[0].decode("utf-8")
#         response = json.loads(response)
#         checksum = response["checksum"]
#         response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xpublist[3]+','+xpublist[4]+','+xpublist[5]+','+xpublist[6]+'))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#         print('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xpublist[3]+','+xpublist[4]+','+xpublist[5]+','+xpublist[6]+'))#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\'')
#         print("importmulti")
#         print(response)
#         rpc = RPC()
#         trans = utxoresponse
#         print("trans start")
#         print(trans)
#         trans = trans.decode("utf-8")
#         print("trans mid")
#         print(trans)
#         trans = trans.split("&")[0].split(",")
#         print("trans end")
#         print(trans)
#         trans[1] = int(trans[1])
#         trans[4] = float(trans[4])
#         #trans[0] = txid
#         #trans[1] = vout
#         #trans[2] = changeaddress
#         #trans[3] = scrirptPubKey
#         #trans[4] = amount
#         #trans[5] = recpipentaddress
#         #trans[6] = witnessScript
#         minerfee = float(rpc.estimatesmartfee(6)["feerate"])
#         kilobytespertrans = 0.545
#         amo = ((trans[4] / 3) - (minerfee * kilobytespertrans))
#         amo = "{:.8f}".format(float(amo))
#         response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createrawtransaction \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\' \'[{"'+trans[5]+'" : '+str(amo)+'}]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#         print()
#         print('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createrawtransaction \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+'}]\' \'[{"'+trans[5]+'" : '+str(amo)+'}]\'')
#         print(response)
#         print("create raw transaction")
#         transonehex = response[0].decode("utf-8")[:-1]
#         print(transonehex)
#         response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli signrawtransactionwithwallet '+transonehex+' \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+', "scriptPubKey": "'+trans[3]+'", "witnessScript": "'+trans[6][:-1]+'", "amount": "'+str(trans[4])+'" }]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
#         print('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli signrawtransactionwithwallet '+transonehex+' \'[{ "txid": "'+trans[0]+'", "vout": '+str(trans[1])+', "scriptPubKey": "'+trans[3]+'", "witnessScript": "'+trans[6][:-1]+'", "amount": "'+str(trans[4])+'" }]\'')
#         print("signrawtrans")
#         print(response)
#         print("result")
#         transone = json.loads(response[0].decode("utf-8"))
#         print(transone)
#         firstqrcode = transone
#         randomnum = str(random.randrange(0,1000000))
#         firstqrname = randomnum
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#             )####DISPLAYING THE ADDRESS IS NOT COMPLEATED ON THE HTML SIDE
#         qr.add_data(firstqrcode)
#         qr.make(fit=True)
#         img = qr.make_image(fill_color="black", back_color="white")
#         home = os.getenv("HOME")
#         img.save(home + '/yeticold/static/firsttransqrcode'+firstqrname+'.png')
#         route = url_for('static', filename='firsttransqrcode' + firstqrname + '.png')
#     if request.method == 'POST':
#         transnum = 2
#         return redirect('/restartwallet')
#     return render_template('displayfirsttransqrcode.html', qrdata=firstqrcode, route=route)
if __name__ == "__main__":
    app.run()
