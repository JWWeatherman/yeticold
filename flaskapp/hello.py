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

# def hashEveryFour(passphraselist):
#     passphrasehashlist = []
#     templist = []
#     for i in range(len(passphraselist)):
#         templist.append(str(passphraselist[i]))
#         if ((i + 1) % 4) == 0:
#             passphrasehashlist.append(hashFour(templist))
#             templist = []
#     return passphrasehashlist

# def hashFour(passphraselist):
#     templist = PassphraseToWIF(passphraselist)
#     templist = decode(templist)
#     key = hex(int(templist)).replace('0x', "")
#     padkey = padhex(key)
#     assert(int(padkey, 16) == int(key,16))
#     byteslist = bytes.fromhex(padkey)
#     hashedbyte = hashlib.sha256(byteslist).digest()
#     num, mod = divmod(int.from_bytes(hashedbyte, 'big'), 58)
#     checksum = ConvertToPassphrase(BASE58_ALPHABET[mod])[0]
#     return checksum

# def int_to_bytes(x: int) -> bytes:
#     return x.to_bytes((x.bit_length() + 7) // 8, 'big')

# def int_from_bytes(xbytes):
#     return int.from_bytes(xbytes, 'big')

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
            subprocess.call('gnome-terminal -- bash -c "sudo ~/flaskapp/bitcoin-0.18.1/bin/bitcoind -proxy=127.0.0.1:9050; read line"', shell=True)
            machine = 1
            return redirect('/runbitcoind')
        elif request.form['option'] == 'end':
            subprocess.call('gnome-terminal -- bash -c "sudo ~/flaskapp/bitcoin-0.18.1/bin/bitcoind -proxy=127.0.0.1:9050; read line"', shell=True)
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
        bitcoind = subprocess.Popen(['~/flaskapp/bitcoin-0.18.1/bin/bitcoin-cli getblockchaininfo'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
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
            adr = rpc.getnewaddress()
            newprivkey = rpc.dumpprivkey(adr)
            binary = bin(decode58(newprivkey))[2:][8:-40]
            WIF = ConvertToWIF(xor(binary,request.form['binary' + str(i)]))
            privkeylisttemp.append(WIF)
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
    global thirdqrcode
    if request.method == 'POST':
        for i in range(0,7):
            rpc = RPC()
            rpc.importprivkey(privkeylist[i],str(i) + 'cre', False)
            adr = rpc.getaddressesbylabel(str(i) + 'cre')
            adrlist.append(list(adr.keys())[0])
        rpc = RPC()
        newadr = rpc.addmultisigaddress(3, adrlist)
        firstqrcode = str(newadr['address'])
        secondqrcode = str(newadr['redeemScript'])
        thirdqrcode = 'addmultisigaddress(3, '+ str(adrlist) + ')'
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
        return redirect('/displaythirdqrcode')
    return render_template('displaysecondqrcode.html', qrdata=secondqrcode, route=route)

@app.route("/displaythirdqrcode", methods=['GET', 'POST'])
def displaythirdqrcode():
    global privkeylist
    global adrlist
    global thirdqrcode
    global thirdqrname
    if request.method == 'GET':
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
        img.save(home + '/flaskapp/static/thirdqrcode' + thirdqrname + '.png')
        route = url_for('static', filename='thirdqrcode' + thirdqrname + '.png')
    if request.method == 'POST':
        return redirect('/display')
    return render_template('displaythirdqrcode.html', qrdata=thirdqrcode, route=route)

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

@app.route("/testkeys", methods=['GET', 'POST'])
def testkeys():
    global privkeylist
    global privkeycount
    global adrlist
    if request.method == 'GET':
        privkeylisttemp = []
        for i in range(1,8):
            rpc = RPC()
            adr = rpc.getnewaddress()
            newprivkey = rpc.dumpprivkey(adr)
            binary = bin(decode58(newprivkey))[2:][8:-40]
            WIF = ConvertToWIF(xor(binary,'1010010111111000101010101101011000001001010101100101111001001111110001101111111010111011000011010100110000001011110010001101011000011111100101000000100011100101111101010110100110111000110111000010110111000000010100100110011010111111101000100100001011001100'))
            privkeylisttemp.append(WIF)
        privkeycount = 0
        privkeylist = privkeylisttemp
    if request.method == 'POST':
        print(privkeylist)
        print(privkeylist[0])
        print(PassphraseToWIF(privkeylist[0]))
        adrlist = []
        return redirect('/confirmkey')
    return render_template('testkeys.html')


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
        global secondqrcode
        global thirdqrcode
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("qrcodescaner")
        img_counter = 0
        qrcode_counter = 0
        pause = 0
        while True:
            if qrcode_counter == 3:
                break
            k = cv2.waitKey(1)
            if k == 13:
                pause = 0
            if not pause == 1 :
                ret, frame = cam.read()
                cv2.imshow("qrcodescaner", frame)
                if not ret:
                    break
                img_counter = img_counter + 1
                if img_counter >= 100:
                    img_counter = 0
                    img_name = "qrcodeimage.png"
                    cv2.imwrite(img_name, frame)
                    decodepng = decode(Image.open('qrcodeimage.png'))
                    if decodepng:
                        pause = 1
                        qrcode_counter = qrcode_counter + 1
                        if qrcode_counter == 1:
                            firstqrcode = decodepng[0].data
                        elif qrcode_counter == 2:
                            secondqrcode = decodepng[0].data
                        elif qrcode_counter == 3:
                            thirdqrcode = decodepng[0].data
        cam.release()
        cv2.destroyAllWindows()
        return redirect('/displayforprint')
    return render_template('scanfirstqrcode.html')

@app.route("/displayforprint", methods=['GET', 'POST'])
def displayforprint():
    global firstqrcode
    global secondqrcode
    global thirdqrcode
    global firstqrname
    global secondqrname
    global thirdqrname
    global currentsecondset
    randomnum = str(random.randrange(0,1000000))
    firstqrname = randomnum
    secondqrname = randomnum
    thirdqrname = randomnum
    routeone = url_for('static', filename='firstqrcode' + firstqrname + '.png')
    routetwo = url_for('static', filename='secondqrcode' + secondqrname + '.png')
    routethree = url_for('static', filename='thirdqrcode' + thirdqrname + '.png')
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
        img.save(home + '/flaskapp/static/thirdqrcode' + thirdqrname + '.png')
    if request.method == 'POST':
        return redirect('/watchonly')
    return render_template('displayforprint.html', first=firstqrcode, second=secondqrcode, third=thirdqrcode, routeone=routeone, routetwo=routetwo, routethree=routethree)

@app.route("/watchonly", methods=['GET', 'POST'])
def watchonly():
    global firstqrcode
    if request.method == 'GET':
        rpc = RPC()
        rpc.importaddress(firstqrcode.decode("utf-8"))
    if request.method == 'POST':
        return redirect('/bitcoinqt')
    return render_template('watchonly.html')

@app.route("/bitcoinqt", methods=['GET', 'POST'])
def bitcoinqt():
    if request.method == 'GET':
        subprocess.call('gnome-terminal -- bash -c "sudo ~/flaskapp/bitcoin-0.18.1/bin/bitcoin-qt; read line"', shell=True)
    if request.method == 'POST':
        return redirect('/displaynewaddress')
    return render_template('bitcoinqt.html')

@app.route("/displaynewaddress", methods=['GET', 'POST'])
def displaynewaddress():
    global firstqrcode
    global firstqrname
    if request.method == 'GET':
        rpc = RPC()
        firstqrcode = rpc.getnewaddress()
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
        img.save(home + '/flaskapp/static/adrqrcode'+firstqrname+'.png')
        route = url_for('static', filename='adrqrcode' + firstqrname + '.png')
    if request.method == 'POST':
        return redirect('/displayutxo')
    return render_template('displaynewaddress.html', qrdata=firstqrcode , route=route)

@app.route("/displayutxo", methods=['GET', 'POST'])
def displayutxo():
    global utxo
    global secondqrname
    if request.method == 'GET':
        utxo = subprocess.Popen(['~/flaskapp/bitcoin-0.18.1/bin/bitcoin-cli listunspent'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        utxo = json.loads(utxo[0])[0]
        newstr = utxo['txid'] + ','
        newstr = newstr + str(utxo['vout']) + ','
        newstr = newstr + utxo['address'] + ','
        newstr = newstr + utxo['scriptPubKey'] + ','
        newstr = newstr + str(utxo['amount'])
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
        return redirect('/scantransqrcode')
    return render_template('displayutxo.html', qrdata=newstr, route=route)

@app.route("/scantransqrcode", methods=['GET', 'POST'])
def scantransqrcode():
    if request.method == 'POST':
        global firstqrcode
        global secondqrcode
        global thirdqrcode
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("qrcodescaner")
        img_counter = 0
        qrcode_counter = 0
        pause = 0
        while True:
            if qrcode_counter == 3:
                break
            k = cv2.waitKey(1)
            if k == 13:
                pause = 0
            if not pause == 1 :
                ret, frame = cam.read()
                cv2.imshow("qrcodescaner", frame)
                if not ret:
                    break
                img_counter = img_counter + 1
                if img_counter >= 100:
                    img_counter = 0
                    img_name = "qrcodeimage.png"
                    cv2.imwrite(img_name, frame)
                    decodepng = decode(Image.open('qrcodeimage.png'))
                    if decodepng:
                        pause = 1
                        qrcode_counter = qrcode_counter + 1
                        if qrcode_counter == 1:
                            firstqrcode = decodepng[0].data
                        elif qrcode_counter == 2:
                            secondqrcode = decodepng[0].data
                        elif qrcode_counter == 3:
                            thirdqrcode = decodepng[0].data
        cam.release()
        cv2.destroyAllWindows()
        return redirect('/checktrans')
    return render_template('scantransqrcode.html')

@app.route("/checktrans", methods=['GET', 'POST'])
def checktrans():
    global firstqrcode
    global secondqrcode
    global thirdqrcode
    if request.method == 'GET':
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
        subprocess.call('gnome-terminal -- bash -c "rm ~/.bitcoin/wallet.dat; read line"', shell=True)
        subprocess.call('gnome-terminal -- bash -c "sudo ~/flaskapp/bitcoin-0.18.1/bin/bitcoind -proxy=127.0.0.1:9050; read line"', shell=True)
        machine = 2
        return redirect('/runbitcoind')
    return render_template('delwallet.html')

@app.route('/importprivkey', methods=['GET', 'POST'])
def importprivkey():
    global privkeylist
    global privkeycount
    global error
    ####ISSUE
    if request.method == 'GET':
        privkeylist = ['L1tze8ayXsYb8pggdAVHF469x1ZqjamExFWHRJuE1ri3nQbwtTeK','KydUgsQedGidufUAgcn2Aa2HMxXY3z6jVXtx6e8SrUVVrr3YhquK','Ky6FdrcTGs62tGG89AEi45Fn5sR5r7pBUacL2XYNX9NyQrHen2mo','KztQF5v7Ga4iazg3ASLDLNVNq1gevY15e9mDnGsM48K9jeDrYj7o','KxuEtno4VaZZSgmRb8PcDCyxA5NwbFSNeLRrJKPgDwnXXH1D2bxe','L2CJRsqAFt3HrTGV3U6vw4kecrCCNrrCURjygBuQUmrNk7h6Ezf5','L2obcyTfbw2Syztrp9kd3amHFEgaThrVG5rVnECJtWbewZttbvAu']
        return redirect('/scanutxo')
    if request.method == 'POSTE':
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
            for i in range(0,7):
                rpc = RPC()
                print(privkeylist[i])
                key = random.randrange(0, 10000000)
                rpc.importprivkey(privkeylist[i],str(i) + str(key), False)
                adr = rpc.getaddressesbylabel(str(i) + str(key))
                newprivkey = rpc.dumpprivkey(list(adr.keys())[0])
                if not newprivkey == privkeylist[i]:
                    privkeycount = 0
                    privkeylist = []
                    error = 'You have imported one of your keys incorrectly please try agian'
                    return redirect('/importprivkey')
            return redirect('/scanutxo')
        else:
            return redirect('/importprivkey')
    return render_template('importprivkey.html', x=privkeycount + 1, error=error)

@app.route("/scanutxo", methods=['GET', 'POST'])
def scanutxo():
    if request.method == 'POST':
        global firstqrcode
        global secondqrcode
        global thirdqrcode
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("qrcodescaner")
        img_counter = 0
        qrcode_counter = 0
        pause = 0
        while True:
            if qrcode_counter == 3:
                break
            k = cv2.waitKey(1)
            if k == 13:
                pause = 0
            if not pause == 1 :
                ret, frame = cam.read()
                if not ret:
                    break
                cv2.imshow("qrcodescaner", frame)
                img_counter = img_counter + 1
                if img_counter >= 100:
                    img_counter = 0
                    img_name = "qrcodeimage.png"
                    cv2.imwrite(img_name, frame)
                    decodepng = decode(Image.open('qrcodeimage.png'))
                    if decodepng:
                        pause = 1
                        qrcode_counter = qrcode_counter + 1
                        if qrcode_counter == 1:
                            firstqrcode = decodepng[0].data
                        elif qrcode_counter == 2:
                            secondqrcode = decodepng[0].data
                        elif qrcode_counter == 3:
                            thirdqrcode = decodepng[0].data
        cam.release()
        cv2.destroyAllWindows()
        return redirect('/displayfirsttransqrcode')
    return render_template('scanutxo.html')

@app.route("/displayfirsttransqrcode", methods=['GET', 'POST'])
def displayfirsttransqrcode():
    global firstqrcode
    global secondqrcode
    global thirdqrcode
    global firstqrname
    global secondqrname
    global thirdqrname
    global privkeylist
    if request.method == 'GET':
        rpc = RPC()
        trans = secondqrcode #### parse this
        trans = trans.decode("utf-8")
        trans = trans.split(",")
        trans[4] = float(trans[4])
        #trans[0] = txid
        #trans[1] = vout
        #trans[2] = address 
        #trans[3] = scrirptPubKey
        #trans[4] = amount
        print(trans)
        print(trans[4])
        amo = ((trans[4] / 3) - 0.00003)
        newamo = (trans[4] * (2 / 3))
        transonehex = rpc.createrawtransaction('''[ { "txid": "''' + trans[0] + '''", "vout": ''' + trans[1] + ''', "scriptPubKey": "''' + trans[3] + '''", "redeemScript": "''' + thirdqrcode + '''" } ]''', '''{ "''' + firstqrcode + '''": '''+ str(amo) +''', "'''+ trans[2] + '''": '''+ str(newamo) +'''}''')
        transone = rpc.signrawtransactionwithkey(transonehex, '['+ privkeylist[0] +','+ privkeylist[1] +','+ privkeylist[2] +']', secondqrcode)
        newamo = (trans[4] * (1 / 3))
        transtwohex = rpc.createrawtransaction('''[ { "txid": "''' + trans[0] + '''", "vout": ''' + trans[1] + ''', "scriptPubKey": "''' + trans[3] + '''", "redeemScript": "''' + thirdqrcode + '''" } ]''', '''{ "''' + firstqrcode + '''": '''+ str(amo) +''', "'''+ trans[2] + '''": '''+ str(newamo) +'''}''')
        transtwo = rpc.signrawtransactionwithkey(transtwohex, '['+ privkeylist[2] +','+ privkeylist[3] +','+ privkeylist[4] +']', secondqrcode)
        newamo = 0
        transthreehex = rpc.createrawtransaction('''[ { "txid": "''' + trans[0] + '''", "vout": ''' + trans[1] + ''', "scriptPubKey": "''' + trans[3] + '''", "redeemScript": "''' + thirdqrcode + '''" } ]''', '''{ "''' + firstqrcode + '''": '''+ str(amo) +''', "'''+ trans[2] + '''": '''+ str(newamo) +'''}''')
        transthree = rpc.signrawtransactionwithkey(transtwohex, '['+ privkeylist[4] +','+ privkeylist[5] +','+ privkeylist[6] +']', secondqrcode)
        firstqrcode = transone
        secondqrcode = transtwo
        thirdqrcode = transthree
        randomnum = str(random.randrange(0,1000000))
        firstqrname = randomnum
        secondqrname = randomnum
        thirdqrname = randomnum
        print(firstqrcode)
        print(secondqrcode)
        print(thirdqrcode)
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
        return redirect('/displaysecondtransqrcode')
    return render_template('displayfirsttransqrcode.html', qrdata=firstqrcode, route=route)

@app.route("/displaysecondtransqrcode", methods=['GET', 'POST'])
def displaysecondtransqrcode():
    global secondqrcode
    global secondqrname
    if request.method == 'GET':
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
        img.save(home + '/flaskapp/static/secondtransqrcode'+secondqrname+'.png')
        route = url_for('static', filename='secondtransqrcode' + secondqrname + '.png')
    if request.method == 'POST':
        return redirect('/displaythirdtransqrcode')
    return render_template('displaysecondtransqrcode.html', qrdata=secondqrcode, route=route)

@app.route("/displaythirdtransqrcode", methods=['GET', 'POST'])
def displaythirdtransqrcode():
    global thirdqrcode
    global thirdqrname
    if request.method == 'GET':
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