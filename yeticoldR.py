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
sourceaddress = None
receipentaddress = None
adrlist = []
transnum = 0
progress = 0
balance = 0
txid = None
vout = 0
utxo = None
amount = 0
minerfee = 0
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

@app.route("/step07", methods=['GET', 'POST'])
def step07():
    if request.method == 'POST':
        subprocess.Popen('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        return redirect('/step08')
    return render_template('YCRstep07.html')

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
    return render_template('YCRstep08.html', progress=progress)

@app.route("/step09", methods=['GET', 'POST'])
def step09():
    global firstqrcode
    global pubdesc
    if request.method == 'POST':
        firstqrcode = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        firstqrcode = firstqrcode.decode("utf-8")
        pubdesc = firstqrcode[:-2]
        return redirect('/step10')
    return render_template('YCRstep09.html')

@app.route("/step10", methods=['GET', 'POST'])
def step10():
    global firstqrcode
    global pubdesc
    if request.method == 'GET':
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": "'+pubdesc+'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        subprocess.Popen('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli rescanblockchain 600000',shell=True,start_new_session=True)
    if request.method == 'POST':
        return redirect('/step11')
    return render_template('YCRstep10.html')

###DISPLAY QR CODES
@app.route("/step11", methods=['GET', 'POST'])
def step11():
    global adrlist
    global color
    global sourceaddress
    addresses = []
    if request.method == 'GET':
        subprocess.call(['rm -r ~/yeticold/static/address*'],shell=True)
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli deriveaddresses "'+pubdesc+'" "[0,999]"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        response = response[0].decode("utf-8")
        response = json.loads(response)
        adrlist = response
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
            print(response)
            print(adrlist[i])
            print(bal)
            bal = "{:.8f}".format(float(bal))
            address = {}
            address['utxocount'] = utxocount
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
        sourceaddress = request.form['address']
        return redirect('/step12')
    return render_template('YCRstep11.html', addresses=addresses, len=len(addresses))

#SEND flow
## SCAN RECIPIENT
@app.route("/step12", methods=['GET', 'POST'])
def step12():
    global secondqrcode
    global error
    global receipentaddress
    if request.method == 'POST':
        error = None
        secondqrcode = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        secondqrcode = secondqrcode.decode("utf-8").replace('\n', '')
        if (secondqrcode.split(':')[0] == 'bitcoin'):
            secondqrcode = secondqrcode.split(':')[1].split('?')[0]
        if (secondqrcode[:3] == 'bc1') or (secondqrcode[:1] == '3') or (secondqrcode[:1] == '1'):
            if not (len(secondqrcode) >= 26) and (len(secondqrcode) <= 35):
                error = secondqrcode + ' is not a valid bitcoin address, address should have a length from 26 to 35 instead of ' + str(len(secondqrcode)) + '.'
        else: 
            error = secondqrcode + ' is not a valid bitcoin address, address should have started with bc1, 3 or 1 instead of ' + secondqrcode[:1] + ', or ' + secondqrcode[:3] + '.'
        if error:
            return redirect('/step12')
        receipentaddress = secondqrcode
        return redirect('/step13')
    return render_template('YCRstep12.html', error=error)

#close bitcoin
@app.route("/step13", methods=['GET', 'POST'])
def step13():
    if request.method == 'POST':
        return redirect('/step14')
    return render_template('YCRstep13.html')
#repackage everything
@app.route("/step14", methods=['GET', 'POST'])
def step14():
    if request.method == 'GET':
        subprocess.call(['gnome-terminal -- bash -c "sudo chmod +x ~/yeticold/scripts/rpkg-script.sh; sudo ~/yeticold/scripts/rpkg-script.sh"'],shell=True)
    if request.method == 'POST':
        return redirect('/step15')
    return render_template('YCRstep14.html')

#move files to LARGE EXTERNAL DRIVE
@app.route("/step15", methods=['GET', 'POST'])
def step15():
    if request.method == 'POST':
        return redirect('/step16')
    return render_template('YCRstep15.html')

#open bitcoin 
@app.route("/step16", methods=['GET', 'POST'])
def step16():
    if request.method == 'POST':
        subprocess.Popen('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        return redirect('/step17')
    return render_template('YCRstep16.html')

#finish opening
@app.route('/step17', methods=['GET', 'POST'])
def step17():
    global progress
    if request.method == 'GET':
        progress = BTCprogress()
    if request.method == 'POST':
        if progress >= 99:
            return redirect('/step18')
        else:
            return redirect('/step17')
    return render_template('YCRstep17.html', progress=progress)

#COPY TO THE OFFLINE
@app.route("/step18", methods=['GET', 'POST'])
def step18():
    if request.method == 'POST':
        return redirect('/step22')
    return render_template('YCRstep18.html')
###SWITCH TO OFFLINE


#open bitcoin
@app.route("/step19", methods=['GET', 'POST'])
def step19():
    if request.method == 'POST':
        subprocess.Popen('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        return redirect('/step20')
    return render_template('YCRstep19.html')

#finish opening
@app.route('/step20', methods=['GET', 'POST'])
def step20():
    global progress
    if request.method == 'GET':
        progress = BTCprogress()
    if request.method == 'POST':
        if progress >= 99:
            return redirect('/step21')
        else:
            return redirect('/step20')
    return render_template('YCRstep20.html', progress=progress)

#scan Recipient, source, and balance qr code
@app.route("/step21", methods=['GET', 'POST'])
def step21():
    global firstqrcode
    global receipentaddress
    global balance
    global sourceaddress
    global txid
    global vout
    if request.method == 'POST':
        firstqrcode = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        firstqrcode = firstqrcode.decode("utf-8")
        firstqrcode = firstqrcode.split('&')
        print("spliced qr code")
        print(firstqrcode)
        receipentaddress = firstqrcode[0]
        sourceaddress = firstqrcode[1]
        balance = firstqrcode[2]
        txid = firstqrcode[3]
        vout = firstqrcode[4]

        return redirect('/step23')
    return render_template('YCRstep21.html')
###SWITCH TO ONLINE


#display Recipient, source, and balance qr code Then switch to the offline
@app.route("/step22", methods=['GET', 'POST'])
def step22():
    global sourceaddress
    global receipentaddress
    global balance
    if request.method == 'GET':
        rpc = RPC()
        testlist = []
        testlist.append(sourceaddress)
        response = rpc.listunspent(0, 9999999, testlist)
        txid = response[0]['txid']
        vout = str(response[0]['vout'])
        bal = response[0]['amount']
        balance = bal
        thirdqrcode = receipentaddress + '&' + sourceaddress + '&' + str(bal) + '&' + txid + '&' + vout
        print(thirdqrcode)
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
        img.save(home + '/yeticold/static/thirdqrcode' + thirdqrname + '.png')
        route = url_for('static', filename='thirdqrcode' + thirdqrname + '.png')
    if request.method == 'POST':
        return redirect('/step31')
    return render_template('YCRstep22.html', qrdata=thirdqrcode, route=route)
#SWITCH TO OFFLINE


#scan descriptor
@app.route("/step23", methods=['GET', 'POST'])
def step23():
    global secondqrcode
    global pubdesc
    if request.method == 'POST':
        secondqrcode = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        pubdesc = secondqrcode
        return redirect('/step2426')
    return render_template('YCRstep23.html')

#import 3 seeds
@app.route('/step2426', methods=['GET', 'POST'])
def step2426():
    global privkeylist
    global xprivlist
    global newxpublist
    global privkeycount
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
        privkeylist.append(PassphraseToWIF(privkey))
        error = None
        privkeycount = privkeycount + 1
        if (privkeycount >= 3):
            newxpublist = []
            for i in range(0,3):
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
                xprivlist.append(privkeyline)
                response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getdescriptorinfo "pk('+privkeyline+')"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                print("xpub response")
                print(response)
                xpub = response[0].decode("utf-8").split('(')[1].split(')')[0]
                print("xpub")
                print(xpub)
                newxpublist.append(xpub)
                privkeycount = 0
            return redirect('/step27')
        else:
            return redirect('/step2426')
    return render_template('YCRstep2426.html', x=privkeycount + 1, error=error,i=privkeycount + 26 )

#stop bitocin qt and delete wallet
@app.route("/step27", methods=['GET', 'POST'])
def step27():
    if request.method == 'POST':
        subprocess.call('gnome-terminal -- bash -c "sudo python3 ~/yeticold/utils/deleteallwallets.py; echo "DONE, Close this window.""', shell=True)
        return redirect('/step28')
    return render_template('YCRstep27.html')

#reopen bitcoin
@app.route("/step28", methods=['GET', 'POST'])
def step28():
    if request.method == 'POST':
        subprocess.Popen('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        return redirect('/step29')
    return render_template('YCRstep28.html')

#finish reopen bitcoin
@app.route('/step29', methods=['GET', 'POST'])
def step29():
    global progress
    if request.method == 'GET':
        progress = BTCprogress()
    if request.method == 'POST':
        if progress >= 99:
            return redirect('/step30')
        else:
            return redirect('/step29')
    return render_template('YCRstep29.html', progress=progress)

#GEN trans qr code
@app.route("/step30", methods=['GET', 'POST'])
def step30():
    global firstqrcode
    global secondqrcode
    global thirdqrcode
    global firstqrname
    global secondqrname
    global thirdqrname
    global privkeylist
    global xprivlist
    global newxpublist
    global transnum
    global utxoresponse
    global pubdesc
    global sourceaddress
    global receipentaddress
    global balance
    global txid
    global vout
    global minerfee
    global amount
    if request.method == 'GET':
        xpublist = pubdesc.decode("utf-8").split(',')[1:]
        xpublist[6] = xpublist[6].split('))')[0]
        descriptorlist = xpublist
        for i in range(0,3):
            xpub = newxpublist[i] + '/*'
            for x in range(0,7):
                oldxpub = xpublist[x]
                if xpub == oldxpub:
                    descriptorlist[x] = (xprivlist[i] + '/*')
                    break
        desc = '"wsh(multi(3,'+descriptorlist[0]+','+descriptorlist[1]+','+descriptorlist[2]+','+descriptorlist[3]+','+descriptorlist[4]+','+descriptorlist[5]+','+descriptorlist[6]+'))'
        ##### CALCULATE WITCH XPRIVS YOU HAVE TO REPLACE XPUBS
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getdescriptorinfo '+desc+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print("descriptor info")
        print(response)
        response = response[0].decode("utf-8")
        response = json.loads(response)
        checksum = response["checksum"]
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli importmulti \'[{ "desc": '+desc+'#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print("importmulti")
        print(response)
        rpc = RPC()
        minerfee = float(rpc.estimatesmartfee(6)["feerate"])
        kilobytespertrans = 0.200
        amo = (float(balance) - (minerfee * kilobytespertrans))
        minerfee = (minerfee * kilobytespertrans)
        amo = "{:.8f}".format(float(amo))
        ##### GET TRANS INFO LIST UNSPENT OR GET ADDRESS INFO 
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createrawtransaction \'[{ "txid": "'+txid+'", "vout": '+vout+'}]\' \'[{"'+receipentaddress+'" : '+str(amo)+'}]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print("createrawtransaction")
        print(response)
        transonehex = response[0].decode("utf-8")[:-1]
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli signrawtransactionwithwallet '+transonehex],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print("signrawtransactionwithwallet")
        print(response)
        transone = json.loads(response[0].decode("utf-8"))
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
        img.save(home + '/yeticold/static/firsttransqrcode'+firstqrname+'.png')
        route = url_for('static', filename='firsttransqrcode' + firstqrname + '.png')
    if request.method == 'POST':
        return redirect('/step')
    return render_template('YCRstep30.html', qrdata=firstqrcode, route=route)

#SWITCH TO ONLINE

#scan trans qr code
@app.route("/step31", methods=['GET', 'POST'])
def step31():
    global firstqrcode
    global receipentaddress
    global minerfee
    global amount
    global balance
    if request.method == 'POST':
        rpc = RPC()
        firstqrcode = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        minerfee = float(rpc.estimatesmartfee(6)["feerate"])
        kilobytespertrans = 0.200
        amount = (float(balance) - (minerfee * kilobytespertrans))
        amount = "{:.8f}".format(float(amo))
        minerfee = (minerfee * kilobytespertrans)
        minerfee = "{:.8f}".format(minerfee)
        return redirect('/step32')
    return render_template('YCRstep31.html')

#confirm send qr code give extra data
@app.route("/step32", methods=['GET', 'POST'])
def step32():
    global receipentaddress
    global minerfee
    global amount
    global balance
    global firstqrcode
    if request.method == 'POST':
        parsedfirstqrcode = firstqrcode.decode("utf-8").split('\'')[3]
        print(parsedfirstqrcode)
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli sendrawtransaction '+parsedfirstqrcode+''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return redirect('/step33')
    return render_template('YCRstep32.html', amount=amount, minerfee=minerfee, recipient=receipentaddress)

#confirm trans
@app.route("/step33", methods=['GET', 'POST'])
def step33():
    global firstqrcode
    if request.method == 'POST':
        return redirect('/step')
    return render_template('YCRstep33.html')



@app.route("/step")
def step():
    return "This page has not been added yet"
if __name__ == "__main__":
    app.run()
