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
import time
import qrcode
app = Flask(__name__)
home = os.getenv("HOME")
rpcpsw = str(random.randrange(0,1000000))
if not (os.path.exists(home + "/.bitcoin")):
    subprocess.call(['mkdir ~/.bitcoin'],shell=True)
else:
    subprocess.call(['rm ~/.bitcoin/bitcoin.conf'],shell=True)
subprocess.call('echo "server=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword='+rpcpsw+'" >> ~/.bitcoin/bitcoin.conf', shell=True)

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
transnum = None
utxoresponse = None
receipentaddress = None
pubdesc = None
adrlist = []
transnum = 0
progress = 0
samedesc = False
utxo = None
rescan = False
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
        bitcoinprogress = 0
    return bitcoinprogress

def BTCFinished():
    response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli getblockchaininfo'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if not (len(response[0]) == 0):
        bitcoinprogress = json.loads(response[0])['initialblockdownload']
    else:
        bitcoinprogress = True
    return bitcoinprogress

def BTCRunning():
    home = os.getenv("HOME")
    if (subprocess.call('lsof -n -i :8332', shell=True) != 1):
        return True
    elif os.path.exists(home + "/.bitcoin/bitcoind.pid"):
        subprocess.call('rm -r ~/.bitcoin/bitcoind.pid', shell=True)
    return False

def RPCYW():
    name = 'username'
    wallet_name = 'yetiwarm'
    print(settings)
    uri = wallet_template.format(**settings, wallet_name=wallet_name)
    rpc = AuthServiceProxy(uri, timeout=600)  # 1 minute timeout
    return rpc

def RPC():
    name = 'username'
    wallet_name = ''
    print(settings)
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
        return redirect('/YWopenbitcoin')
    return render_template('redirect.html')

@app.route("/YWopenbitcoin", methods=['GET', 'POST'])
def YWopenbitcoin():
    global progress
    if request.method == 'GET':
        home = os.getenv("HOME")
        if not BTCRunning():
            subprocess.Popen('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        progress = BTCprogress()
    if request.method == 'POST':
        if progress >= 99.9:
            return redirect('YWmenu')
            subprocess.call(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createwallet "yetiwarm"'],shell=True)
            subprocess.call(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli loadwallet "yetiwarm"'],shell=True)
        else:
            return redirect('/YWopenbitcoin')
    return render_template('YWopenbitcoin.html', progress=progress)

@app.route("/YWmenu", methods=['GET', 'POST'])
def YWmenu():
    if request.method == 'POST':
        if request.form['option'] == 'recovery':
            return redirect('/YWRrestartbitcoin')
        else:
            return redirect('/YWrestartbitcoin')
    return render_template('YWmenu.html')

@app.route("/YWrestartbitcoin", methods=['GET', 'POST'])
def YWrestartbitcoin():
    global progress
    global IBD
    if request.method == 'GET':
        subprocess.call('python3 ~/yeticold/utils/stopbitcoin.py', shell=True)
        subprocess.call('rm -r ~/.bitcoin/yetiwarm*', shell=True)
        subprocess.call('rm -r ~/yetiwarmwallet*', shell=True)
        subprocess.Popen('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        progress = BTCprogress()
    if request.method == 'POST':
        IBD = BTCFinished()
        while IBD:
            IBD = BTCFinished()
        subprocess.call(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createwallet "yetiwarm"'],shell=True)
        subprocess.call(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli loadwallet "yetiwarm"'],shell=True)
        return redirect('/YWgetseeds')
    return render_template('YWrestartbitcoin.html')

#randomise priv key and get xprivs
@app.route("/YWgetseeds", methods=['GET', 'POST'])
def YWgetseeds():
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
                binary = bin(decode_base58(newprivkey))[2:][8:-40]
                newbinary = '1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
                WIF = BinaryToWIF(xor(binary,newbinary))
                privkeylisttemp.append(WIF)
            privkeycount = 0
            privkeylist = privkeylisttemp
        else:
            privkeylisttemp = []
            for i in range(1,8):
                rpc = RPC()
                adr = rpc.getnewaddress()
                newprivkey = rpc.dumpprivkey(adr)
                binary = bin(decode_base58(newprivkey))[2:][8:-40]
                WIF = BinaryToWIF(xor(binary,request.form['binary' + str(i)]))
                privkeylisttemp.append(WIF)
            privkeycount = 0
            privkeylist = privkeylisttemp
        for i in range(0,7):
            home = os.getenv('HOME')
            pathtwo = home + '/yetiwarmwallet' + str(i)
            path = home + '/yetiwarmwallettwo' + str(i)
            subprocess.call(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createwallet "yetiwarmwallettwo'+str(i)+'"'],shell=True)
            subprocess.call(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli loadwallet "yetiwarmwallettwo'+str(i)+'"'],shell=True)
            response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=yetiwarmwallettwo'+str(i)+' sethdseed false "'+privkeylist[i]+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            print(response)
            response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=yetiwarmwallettwo'+str(i)+' dumpwallet "yetiwarmwallettwo'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            print(response)
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
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=yetiwarm getdescriptorinfo "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        response = json.loads(response[0].decode("utf-8"))
        print(response)
        print(response["descriptor"])
        checksum = response["checksum"]
        pubdesc = response["descriptor"]
        return redirect('/YWdisplayseeds')
    return render_template('YWgetseeds.html')
#display seeds
@app.route('/YWdisplayseeds', methods=['GET', 'POST'])
def YWdisplayseeds():
    global privkeylist
    global privkeycount
    if request.method == 'GET':
        privkey = privkeylist[privkeycount]
        passphraselist = WIFToPassphraseList(privkey)
    if request.method == 'POST':
        home = os.getenv('HOME')
        path = home + '/Documents'
        subprocess.call('rm '+path+'/ywseed'+str(privkeycount + 1)+'.txt', shell=True)
        subprocess.call('touch '+path+'/ywseed'+str(privkeycount + 1)+'.txt', shell=True)
        file = ''
        for i in range(0,13):
            file = file + request.form['displayrow' + str(i+1)] + '\n'
        subprocess.call('echo "'+file+'" >> '+path+'/ywseed'+str(privkeycount + 1)+'.txt', shell=True)
        privkeycount = privkeycount + 1
        if (privkeycount == 7):
            privkeycount = 0
            return redirect('/YWcheckseeds')
        else:
            return redirect('/YWdisplayseeds')
    return render_template('YWdisplayseeds.html', PPL=passphraselist, x=privkeycount + 1, i=privkeycount + 25)
#confirm privkey
@app.route('/YWcheckseeds', methods=['GET', 'POST'])
def YWcheckseeds():
    global privkeylist
    global xprivlist
    global privkeycount
    global error
    if request.method == 'POST':
        privkey = privkeylist[privkeycount]
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
            error = None
            privkeycount = privkeycount + 1
            if (privkeycount >= 7):
                privkeycount = 7
                newxprivlist = []
                for i in range(0,7):
                    rpc = RPC()
                    home = os.getenv('HOME')
                    path = home + '/yetiwarmwallettwo' + str(i)
                    subprocess.call(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createwallet "yetiwarmwallettwo'+str(i)+'" false true'],shell=True)
                    subprocess.call(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli loadwallet "yetiwarmwallettwo'+str(i)+'"'],shell=True)
                    response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=yetiwarmwallettwo'+str(i)+' sethdseed false "'+privkeylist[i]+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                    print(response)
                    response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=yetiwarmwallettwo'+str(i)+' dumpwallet "yetiwarmwallettwo'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                    print(response)
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
                        return redirect('/YWcheckseeds')
                return redirect('/YWprintdescriptor')
            else:
                return redirect('/YWcheckseeds')
        else:
            error = 'You enterd the private key incorrectly but the checksums are correct please try agian. This means you probably inputed a valid seed, but not your seed ' +str(privkeycount + 1)+' seed.'
    return render_template('YWcheckseeds.html', x=privkeycount + 1, error=error,i=privkeycount + 35 )

#display for print
@app.route("/YWprintdescriptor", methods=['GET', 'POST'])
def YWprintdescriptor():
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
        path = url_for('static', filename='firstqrcode' + firstqrname + '.png')
    if request.method == 'POST':
        return redirect('/YWcopyseeds')
    return render_template('YWprintdescriptor.html', qrdata=pubdesc, path=path)

@app.route("/YWcopyseeds", methods=['GET', 'POST'])
def YWcopyseeds():
    if request.method == 'POST':
        return redirect('/YWmenu')
    return render_template('YWcopyseeds.html')

###END OF SETUP

#### start recovery

#finish open bitcoin
@app.route("/YWRrestartbitcoin", methods=['GET', 'POST'])
def YWRrestartbitcoin():
    global progress
    global IBD
    if request.method == 'GET':
        subprocess.call('python3 ~/yeticold/utils/stopbitcoin.py', shell=True)
        subprocess.call('rm -r ~/.bitcoin/yetiwarm*', shell=True)
        subprocess.call('rm -r ~/yetiwarmwallet*', shell=True)
        subprocess.Popen('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        progress = BTCprogress()
    if request.method == 'POST':
        IBD = BTCFinished()
        while IBD:
            print(IBD)
            IBD = BTCFinished()
        subprocess.call(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createwallet "yetiwarm"'],shell=True)
        subprocess.call(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli loadwallet "yetiwarm"'],shell=True)
        return redirect('/YWRscandescriptor')
    return render_template('YWRrestartbitcoin.html')

@app.route("/YWRscandescriptor", methods=['GET', 'POST'])
def YWRscandescriptor():
    global firstqrcode
    global pubdesc
    global samedesc
    if request.method == 'GET':
        if pubdesc:
            samedesc = True
            if rescan:
                return redirect('/YWRdisplaywallet')
            else:
                return redirect('/YWRrescanwallet')
    if request.method == 'POST':
        firstqrcode = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        pubdesc = firstqrcode.decode("utf-8").replace('\n', '')
        samedesc = False
        return redirect('/YWRrescanwallet')
    return render_template('YWRscandescriptor.html', pubdesc=pubdesc)

@app.route("/YWRrescanwallet", methods=['GET', 'POST'])
def YWRrescanwallet():
    global firstqrcode
    global pubdesc
    global rescan
    if request.method == 'GET':
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=yetiwarm importmulti \'[{ "desc": "'+pubdesc+'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        subprocess.Popen('~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=yetiwarm rescanblockchain 600000',shell=True,start_new_session=True)
        rescan = True
    if request.method == 'POST':
        return redirect('/YWRdisplaywallet')
    return render_template('YWRrescanwallet.html')

@app.route("/YWRdisplaywallet", methods=['GET', 'POST'])
def YWRdisplaywallet():
    global addresses
    global color
    global sourceaddress
    if request.method == 'GET':
        addresses = []
        subprocess.call(['rm -r ~/yeticold/static/address*'],shell=True)
        adrlist = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=yetiwarm deriveaddresses "'+pubdesc+'" "[0,999]"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(adrlist)
        adrlist = json.loads(adrlist[0].decode("utf-8"))
        for i in range(0, len(adrlist)):
            randomnum = str(random.randrange(0,1000000))
            route = url_for('static', filename='address'+randomnum+'.png')
            rpc = RPCYW()
            testlist = []
            testlist.append(adrlist[i])
            response = rpc.listunspent(0, 9999999, testlist)
            print(response)
            if response == []:
                bal = "0.0000000"
                txid = ''
                vout = 0
            else:
                bal = str(response[0]['amount'])
                txid = str(response[0]['txid'])
                vout = str(response[0]['vout'])
            utxocount = len(response)
            response = rpc.getreceivedbyaddress(adrlist[i])
            print(response)
            if response == 0:
                totalbal = "0.0000000"
            else:
                totalbal = str(response)
            bal = "{:.8f}".format(float(bal))
            address = {}
            address['txid'] = txid
            address['vout'] = vout
            address['utxocount'] = utxocount
            address['address'] = adrlist[i]
            address['balance'] = bal
            address['numbal'] = float(bal)
            address['totalbal'] = totalbal
            address['totalnumbal'] = float(totalbal)
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
        for i in range(0, len(addresses)):
            if addresses[i]['address'] == request.form['address']:
                sourceaddress = addresses[i]
        return redirect('/YWRscanrecipent')
    return render_template('YWRdisplaywallet.html', addresses=addresses, len=len(addresses))

@app.route("/YWRscanrecipent", methods=['GET', 'POST'])
def YWRscanrecipent():
    global error
    global receipentaddress
    if request.method == 'POST':
        error = None
        if request.form['option'] == 'scan':
            receipentaddress = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            receipentaddress = receipentaddress.decode("utf-8").replace('\n', '')
        else:
            receipentaddress = request.method['option']
        if (receipentaddress.split(':')[0] == 'bitcoin'):
            receipentaddress = receipentaddress.split(':')[1].split('?')[0]
        if (receipentaddress[:3] == 'bc1') or (receipentaddress[:1] == '3') or (receipentaddress[:1] == '1'):
            if not (len(receipentaddress) >= 26) and (len(receipentaddress) <= 35):
                error = receipentaddress + ' is not a valid bitcoin address, address should have a length from 26 to 35 instead of ' + str(len(receipentaddress)) + '.'
        else: 
            error = receipentaddress + ' is not a valid bitcoin address, address should have started with bc1, 3 or 1 instead of ' + receipentaddress[:1] + ', or ' + receipentaddress[:3] + '.'
        if error:
            return redirect('/YWRscanrecipent')
        return redirect('/YWRimportseeds')
    return render_template('YWRscanrecipent.html', error=error, recipent=receipentaddress)

@app.route('/YWRimportseeds', methods=['GET', 'POST'])
def YWRimportseeds():
    global privkeylist
    global xprivlist
    global newxpublist
    global privkeycount
    global error 
    global samedesc
    if request.method == 'GET':
        if samedesc:
            return redirect('/YWRsendtransaction')
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
        privkeylist.append(PassphraseListToWIF(privkey))
        error = None
        privkeycount = privkeycount + 1
        if (privkeycount >= 3):
            newxpublist = []
            for i in range(0,3):
                rpc = RPC()
                home = os.getenv('HOME')
                path = home + '/yetiwarmwallet' + str(i)
                subprocess.call(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli createwallet "yetiwarmwallet'+str(i)+'" false true'],shell=True)
                subprocess.call(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli loadwallet "yetiwarmwallet'+str(i)+'"'],shell=True)
                response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=yetiwarmwallet'+str(i)+' sethdseed false "'+privkeylist[i]+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                print(response)
                response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=yetiwarmwallet'+str(i)+' dumpwallet "yetiwarmwallet'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                print(response)
                wallet = open(path,'r')
                wallet.readline()
                wallet.readline()
                wallet.readline()
                wallet.readline()
                wallet.readline()
                privkeyline = wallet.readline()
                privkeyline = privkeyline.split(" ")[4][:-1]
                xprivlist.append(privkeyline)
                response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=yetiwarm getdescriptorinfo "pk('+privkeyline+')"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                print(response)
                response = response[0].decode("utf-8")
                xpub = response.split('(')[1].split(')')[0]
                newxpublist.append(xpub)
                privkeycount = 0
            return redirect('/YWRsendtransaction')
        else:
            return redirect('/YWRimportseeds')
    return render_template('YWRimportseeds.html', x=privkeycount + 1, error=error,i=privkeycount + 12 )

#GEN trans qr code
@app.route("/YWRsendtransaction", methods=['GET', 'POST'])
def YWRsendtransaction():
    global xprivlist
    global newxpublist
    global pubdesc
    global sourceaddress
    global receipentaddress
    global minerfee
    global transnum
    if request.method == 'GET':
        xpublist = pubdesc.split(',')[1:]
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
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=yetiwarm getdescriptorinfo '+desc+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        response = json.loads(response[0].decode("utf-8"))
        checksum = response["checksum"]
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=yetiwarm importmulti \'[{ "desc": '+desc+'#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        rpc = RPC()
        minerfee = float(rpc.estimatesmartfee(1)["feerate"])
        kilobytespertrans = 0.200
        minerfee = (minerfee * kilobytespertrans)
        amo = (float(sourceaddress['numbal']) - minerfee)
        amo = "{:.8f}".format(float(amo))
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=yetiwarm createrawtransaction \'[{ "txid": "'+sourceaddress['txid']+'", "vout": '+sourceaddress['vout']+'}]\' \'[{"'+receipentaddress+'" : '+str(amo)+'}]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        response = response[0].decode("utf-8")
        transonehex = response[:-1]
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=yetiwarm signrawtransactionwithwallet '+transonehex],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        response = json.loads(response[0].decode("utf-8"))
        transnum = response
        minerfee = "{:.8f}".format(minerfee)
    if request.method == 'POST':
        response = subprocess.Popen(['~/yeticold/bitcoin-0.19.0rc1/bin/bitcoin-cli -rpcwallet=yetiwarm sendrawtransaction '+transnum['hex']+''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        return redirect('/YWmenu')
    return render_template('YWRsendtransaction.html', amount=amo, minerfee=minerfee, recipent=receipentaddress)

if __name__ == "__main__":
    app.run()
