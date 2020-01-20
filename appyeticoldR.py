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
address = []
xprivlist = []
privkeylist = []
error = None
pubdesc = None
selectedutxo = None
receipentaddress = None
progress = 0
privkeycount = 0
init = True
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
    return not bitcoinprogress

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
    wallet_name = 'yeticold'
    uri = wallet_template.format(**settings, wallet_name=wallet_name)
    rpc = AuthServiceProxy(uri, timeout=600)  # 1 minute timeout
    return rpc

def PassphraseToWIF(passphraselist):
    Privkey = ''
    for i in range(len(passphraselist)):
        Privkey += switcher.get(str(passphraselist[i]))
    return Privkey

def blockheight():
    rpc = RPC()
    Blockinfo = rpc.getblockchaininfo()
    blockheight = 0
    if Blockinfo['pruned']:
        blockheight = Blockinfo['pruneheight']
    return str(blockheight)


#YCRblockchain - step X - #download crap bitcoin directory?
#Open bitcoin - step 7 - Open bitcoin - Online
#Scan Descriptor - step 8 - Online
#Rescan Wallet - step 9 - Online
#Display Wallet - WP - Online
#Setup Disconnected - step 3 - Online # go to rec.yeticold.com and follow steps
#Open bitcoin - auto redirect - Open bitcoin - Disconnected
#Scan descriptor - step 4 - Disconnected
#Import keys - step 5 - Disconnected # seed 1
#Import keys - step 6 - Disconnected # seed 2
#Import keys - step 7 - Disconnected # seed 3
#Switch laptop - step 8 - Disconnected # On your online laptop showing step 3 click next and continue on step 9
#Display utxo - step 9 - Online # On your Disconnected laptop showing step 8 click next and continue on step 10
#Scan utxo - step 10 - Disconnected # Scan the qr code from your online laptop displaing step 9
#Scan recipent - step 11 - Disconnected
#Confirm transaction - step 12 - Disconnected
#Display transaction - step 13 - Disconnected # On your Online laptop currently showing step 9 click next and contiue on step 14
#Scan transaction - step 14 - Online #Scan the transaction from your Disconnected laptop currently showing step 13

#Display wallet - WP - Online
#Display utxo B - step 1 - Online # On your Disconnected laptop showing step (13 or 5) click next and continue on step 2
#Scan utxo B - step 2 - Disconnected # Scan the qr code from your online laptop displaing step 1
#Scan recipent B - step 3 - Disconnected
#Confirm transaction B - step 4 - Disconnected
#Display transaction B - step 5 - Disconnected # On your Online laptop currently showing step 1 click next and contiue on step 6
#Scan transaction B - step 6 - Online #Scan the transaction from your Disconnected laptop currently showing step 5

@app.route("/", methods=['GET', 'POST'])
def redirectroute():
    if request.method == 'GET':
        return redirect('/YCRblockchain')
    return render_template('redirect.html')

@app.route("/YCRblockchain", methods=['GET', 'POST'])
def YCRblockchain():
    global rpcpsw
    if request.method == 'GET':
        home = os.getenv("HOME")
        if (os.path.exists(home + "/.bitcoin")):
            if (os.path.exists(home + "/.bitcoin/bitcoin.conf")):
                with open(".bitcoin/bitcoin.conf","r+") as f:
                    old = f.read()
                    f.seek(0)
                    new = "server=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword="+rpcpsw+"\n"
                    f.write(new + old)
            else:
                subprocess.call('echo "server=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword='+rpcpsw+'" >> '+home+'/.bitcoin/bitcoin.conf', shell=True)
            return redirect('/YCRopenbitcoin')
    if request.method == 'POST':
        if request.form['option'] == 'downloadblockchain':
            subprocess.call(['python3 ~/yeticold/utils/testblockchain.py'],shell=True)
        else:
            fmt = '%Y-%m-%d %H:%M:%S'
            today = str(datetime.today()).split('.')[0]
            print(request.form['date'] + ' 12:0:0')
            print(today)
            d1 = datetime.strptime(request.form['date'] + ' 12:0:0', fmt)
            d2 = datetime.strptime(today, fmt)
            d1_ts = time.mktime(d1.timetuple())
            d2_ts = time.mktime(d2.timetuple())
            diff = (int(d2_ts - d1_ts) / 60) / 10
            add = diff / 10
            blockheight = diff + add + 550
            blockheight = int(blockheight)
            home = os.getenv("HOME")
            subprocess.call(['mkdir ~/.bitcoin'],shell=True)
            subprocess.call('echo "server=1\nrpcport=8332\nrpcuser=rpcuser\nprune='+str(blockheight)+'\nrpcpassword='+rpcpsw+'" >> '+home+'/.bitcoin/bitcoin.conf', shell=True)
        return redirect('/YCRopenbitcoin')
    return render_template('YCRblockchain.html')

@app.route("/YCRopenbitcoin", methods=['GET', 'POST'])
def YCRopenbitcoin():
    global progress
    if request.method == 'GET':
        home = os.getenv("HOME")
        if BTCClosed():
            subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        progress = BTCprogress()
    if request.method == 'POST':
        if progress >= 99.9:
            subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yeticold"'],shell=True)
            return redirect('YCRscandescriptor')
        else:
            return redirect('/YCRopenbitcoin')
    return render_template('YCRopenbitcoin.html', progress=progress)

@app.route("/YCRscandescriptor", methods=['GET', 'POST'])
def YCRscandescriptor():
    global pubdesc
    if request.method == 'POST':
        pubdesc = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        pubdesc = pubdesc.decode("utf-8")
        pubdesc = pubdesc.replace('\n', '')
        return redirect('/YCRrescanwallet')
    return render_template('YCRscandescriptor.html')

@app.route("/YCRrescanwallet", methods=['GET', 'POST'])
def YCRrescanwallet():
    global pubdesc
    if request.method == 'GET':
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticold importmulti \'[{ "desc": "'+pubdesc+'", "timestamp": "now", "range": [0,999], "watchonly": false}]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        if not (len(response[1]) == 0): 
            print(response)
            return "error response from importmulti: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticold importmulti \'[{ "desc": "'+pubdesc+'", "timestamp": "now", "range": [0,999], "watchonly": false}]\' \'{"rescan": true}\''
        subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticold rescanblockchain '+blockheight(),shell=True,start_new_session=True)
    if request.method == 'POST':
        return redirect('/YCRdisplaywallet')
    return render_template('YCRrescanwallet.html')

@app.route("/YCRdisplaywallet", methods=['GET', 'POST'])
def YCRdisplaywallet():
    global selectedutxo
    global addresses
    global init
    global rpcpsw
    if request.method == 'GET':
        subprocess.call(['rm -r ~/yeticold/static/address*'],shell=True)
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticold deriveaddresses "'+pubdesc+'" "[0,999]"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        adrlist = json.loads(response[0].decode("utf-8"))
        addresses = []
        totalwalletbal = 0
        rpc = RPC()
        for i in range(0, len(adrlist)):
            adr = adrlist[i]
            randomnum = str(random.randrange(0,1000000))
            route = url_for('static', filename='address'+adr+''+randomnum+'.png')
            response = rpc.listunspent(0, 9999999, [adr])
            if response == []:
                totalbal = rpc.getreceivedbyaddress(adrlist[i])
                if totalbal:
                    status = 3
                else:
                    status = 0
                address = {}
                address['txid'] = ''
                address['address'] = adr
                address['balance'] = "0.00000000"
                address['numbal'] = 0
                address['status'] = status
                address['route'] = route
                addresses.append(address)
            else:
                for x in range(0, len(response)):
                    utxo = response[x]
                    txid = utxo['txid']
                    vout = utxo['vout']
                    scriptPubKey = utxo['scriptPubKey']
                    numamount = utxo['amount']
                    totalwalletbal = totalwalletbal + numamount
                    amount = "{:.8f}".format(float(numamount))
                    numamount = float(amount)
                    confs = utxo['confirmations']
                    totalbal = rpc.getreceivedbyaddress(adr)
                    if numamount:
                        if not confs:
                            status = 1
                        else:
                            status = 2
                    elif totalbal:
                        status = 3
                    else:
                        status = 0
                    address = {}
                    address['txid'] = txid
                    address['vout'] = vout 
                    address['scriptPubKey'] = scriptPubKey
                    address['address'] = adr
                    address['balance'] = amount
                    address['numbal'] = numamount
                    address['status'] = status
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
            color = '#e9ecef'
            if (i % 2) == 0:
                color = 'white'
            img = qr.make_image(fill_color="black", back_color=color)
            home = os.getenv("HOME")
            img.save(home + '/yeticold/'+addresses[i]['route'])
    if request.method == 'POST':
        for i in range(0, len(addresses)):
            if request.form['txid'] == addresses[i]['txid']:
                selectedutxo = addresses[i]
                break
        if init:
            return redirect('/YCRstartdisconnected')
        return redirect('/YCRdisplayutxo')
    return render_template('YCRdisplaywallet.html', addresses=addresses, len=len(addresses), TWB=totalwalletbal)

@app.route("/YCRstartdisconnected", methods=['GET', 'POST'])
def YCRstartdisconnected():
    global oldaddresses
    global addresses
    if request.method == 'POST':
        oldaddresses = addresses
        return redirect('/YCRdisplayutxo')
    return render_template('YCRstartdisconnected.html')

@app.route("/YCRopenbitcoinB", methods=['GET', 'POST'])
def YCRopenbitcoinB():
    global progress
    global IBD
    if request.method == 'GET':
        home = os.getenv("HOME")
        if BTCClosed():
            if (os.path.exists(home + "/.bitcoin/bitcoin.conf")):
                with open(".bitcoin/bitcoin.conf","r+") as f:
                    old = f.read()
                    f.seek(0)
                    new = "server=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword="+rpcpsw+"\n"
                    f.write(new + old)
            else:
                subprocess.call('echo "server=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword='+rpcpsw+'" >> '+home+'/.bitcoin/bitcoin.conf', shell=True)
            subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        IBD = BTCFinished()
        progress = BTCprogress()
    if request.method == 'POST':
        if IBD:
            subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yeticold"'],shell=True)
            return redirect('/YCRscandescriptorB')
        else:
            return redirect('/YCRopenbitcoinB')
    return render_template('YCRopenbitcoinB.html', progress=progress, IBD=IBD)

@app.route("/YCRscandescriptorB", methods=['GET', 'POST'])
def YCRscandescriptorB():
    global pubdesc
    if request.method == 'POST':
        pubdesc = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        return redirect('/YCRimportseeds')
    return render_template('YCRscandescriptorB.html')

@app.route('/YCRimportseeds', methods=['GET', 'POST'])
def YCRimportseeds():
    global init
    global pubdesc
    global privkeycount
    global error
    global privkeylist
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
            xpublist = []
            for i in range(0,3):
                rpc = RPC()
                home = os.getenv('HOME')
                path = home + '/yeticoldwallet' + str(i)
                subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yeticoldwallet'+str(i)+'" false true','~/yeticold/bitcoin/bin/bitcoin-cli loadwallet "yeticoldwallet'+str(i)+'"'],shell=True)
                response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwallet'+str(i)+' sethdseed true "'+privkeylist[i]+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                print(response)
                response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwallet'+str(i)+' dumpwallet "yeticoldwallet'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
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
                response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticold getdescriptorinfo "pk('+privkeyline+')"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                print(response)
                response = response[0].decode("utf-8")
                xpub = response.split('(')[1].split(')')[0]
                xpublist.append(xpub)
            privkeycount = 0
            descriptorxpubs = pubdesc.decode("utf-8").split(',')[1:]
            descriptorxpubs[6] = descriptorxpubs[6].split('))')[0]
            descriptorlist = descriptorxpubs
            for i in range(0,3):
                xpub = xpublist[i] + '/*'
                for x in range(0,7):
                    oldxpub = descriptorxpubs[x]
                    if xpub == oldxpub:
                        descriptorlist[x] = (xprivlist[i] + '/*')
                        break
            desc = '"wsh(multi(3,'+descriptorlist[0]+','+descriptorlist[1]+','+descriptorlist[2]+','+descriptorlist[3]+','+descriptorlist[4]+','+descriptorlist[5]+','+descriptorlist[6]+'))'
            response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yeticoldpriv"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldpriv getdescriptorinfo '+desc+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            print(response)
            response = json.loads(response[0].decode("utf-8"))
            checksum = response["checksum"]
            response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldpriv importmulti \'[{ "desc": '+desc+'#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false}]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            print(response)
            return redirect('/YCRswitchlaptop')
        else:
            return redirect('/YCRimportseeds')
    return render_template('YCRimportseeds.html', x=privkeycount + 1, error=error,i=privkeycount + 4)

@app.route("/YCRswitchlaptop", methods=['GET', 'POST'])
def YCRswitchlaptop():
    if request.method == 'POST':
        return redirect('/YCRscanutxo')
    return render_template('YCRswitchlaptop.html', progress=progress)

@app.route("/YCRdisplayutxo", methods=['GET', 'POST'])
def YCRdisplayutxo():
    global init
    global selectedutxo
    if request.method == 'GET':
        randomnum = str(random.randrange(0,1000000))
        qrname = randomnum
        qr = qrcode.QRCode(
               version=1,
               error_correction=qrcode.constants.ERROR_CORRECT_L,
               box_size=10,
               border=4,
        )
        qr.add_data(str(selectedutxo))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        home = os.getenv("HOME")
        img.save(home + '/yeticold/static/qrcode' + qrname + '.png')
        path = url_for('static', filename='qrcode' + qrname + '.png')
    if request.method == 'POST':
        return redirect('/YCRscantransaction')
    if init:
        return render_template('YCRdisplayutxo.html', qrdata=selectedutxo, path=path)
    return render_template('YCRdisplayutxoB.html', qrdata=selectedutxo, path=path)

@app.route("/YCRscanutxo", methods=['GET', 'POST'])
def YCRscanutxo():
    global init
    global selectedutxo
    if request.method == 'POST':
        selectedutxo = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        selectedutxo = eval(selectedutxo.decode("utf-8"))
        return redirect('/YCRscanrecipent')
    if init:
        return render_template('YCRscanutxo.html')
    return render_template('YCRscanutxoB.html')

@app.route("/YCRscanrecipent", methods=['GET', 'POST'])
def YCRscanrecipent():
    global init
    global error
    global receipentaddress
    if request.method == 'POST':
        error = None
        if request.form['option'] == 'scan':
            receipentaddress = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
            receipentaddress = receipentaddress.decode("utf-8").replace('\n', '')
        else:
            receipentaddress = request.form['option']
        if (receipentaddress.split(':')[0] == 'bitcoin'):
            receipentaddress = receipentaddress.split(':')[1].split('?')[0]
        if (receipentaddress[:3] == 'bc1') or (receipentaddress[:1] == '3') or (receipentaddress[:1] == '1'):
            if not (len(receipentaddress) >= 26) and (len(receipentaddress) <= 35):
                error = receipentaddress + ' is not a valid bitcoin address, address should have a length from 26 to 35 instead of ' + str(len(receipentaddress)) + '.'
        else: 
            error = receipentaddress + ' is not a valid bitcoin address, address should have started with bc1, 3 or 1 instead of ' + receipentaddress[:1] + ', or ' + receipentaddress[:3] + '.'
        if error:
            return redirect('/YCRscanrecipent')
        return redirect('/YCRconfirmsend')
    if init:
        return render_template('YCRscanrecipent.html', error=error)
    return render_template('YCRscanrecipentB.html', error=error)

@app.route("/YCRconfirmsend", methods=['GET', 'POST'])
def YCRconfirmsend():
    global init
    global receipentaddress
    if request.method == 'GET':
        rpc = RPC()
        amount = float(selectedutxo['balance'])
        minerfee = float(rpc.estimatesmartfee(1)["feerate"])
        kilobytespertrans = 0.200
        amo = (amount - (minerfee * kilobytespertrans))
        minerfee = (minerfee * kilobytespertrans)
        amo = "{:.8f}".format(float(amo))
        minerfee = "{:.8f}".format(float(minerfee))
    if request.method == 'POST':
        return redirect('/YCRdisplaytransaction')
    if init:
        return render_template('YCRconfirmsend.html', amount=amo, minerfee=minerfee, recipent=receipentaddress)
    return render_template('YCRconfirmsendB.html', amount=amo, minerfee=minerfee, recipent=receipentaddress)

@app.route("/YCRdisplaytransaction", methods=['GET', 'POST'])
def YCRdisplaytransaction():
    global init
    global selectedutxo
    global receipentaddress
    if request.method == 'GET':
        rpc = RPC()
        amount = float(selectedutxo['balance'])
        minerfee = float(rpc.estimatesmartfee(1)["feerate"])
        kilobytespertrans = 0.200
        amo = (amount - (minerfee * kilobytespertrans))
        minerfee = (minerfee * kilobytespertrans)
        amo = "{:.8f}".format(float(amo))
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldpriv createrawtransaction \'[{ "txid": "'+selectedutxo['txid']+'", "vout": '+str(selectedutxo['vout'])+'}]\' \'[{"'+receipentaddress+'" : '+str(amo)+'}]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        response = response[0].decode("utf-8")
        transonehex = response[:-1]
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldpriv signrawtransactionwithwallet '+transonehex+' \'[{"txid":"'+selectedutxo['txid']+'","vout":'+str(selectedutxo['vout'])+',"scriptPubKey":"'+selectedutxo['scriptPubKey']+'","amount":"'+str(amount)+'"}]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        transhex = json.loads(response[0].decode("utf-8"))['hex']
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
            )
        qr.add_data(transhex)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        home = os.getenv("HOME")
        randomnum = str(random.randrange(0,1000000))
        img.save(home + '/yeticold/static/qrcode'+randomnum+'.png')
        path = url_for('static', filename='qrcode'+randomnum+'.png')
    if request.method == 'POST':
        return redirect('/YCRscanutxo')
    if init:
        init = False
        return render_template('YCRdisplaytransaction.html', qrdata=transhex, path=path)
    return render_template('YCRdisplaytransactionB.html', qrdata=transhex, path=path)

@app.route("/YCRscantransaction", methods=['GET', 'POST'])
def YCRscantransaction():
    global init
    if request.method == 'POST':
        response = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        transactionhex = response.decode("utf-8")
        print(transactionhex)
        init = False
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet= sendrawtransaction '+transactionhex],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return redirect('/YCRdisplaywallet')
    if init:
        return render_template('YCRscantransaction.html')
    return render_template('YCRscantransactionB.html')


if __name__ == "__main__":
    app.run()
