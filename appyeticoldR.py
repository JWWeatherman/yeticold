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
    wallet_name = 'yeticold'
    uri = wallet_template.format(**settings, wallet_name=wallet_name)
    rpc = AuthServiceProxy(uri, timeout=600)  # 1 minute timeout
    return rpc

def PassphraseToWIF(passphraselist):
    Privkey = ''
    for i in range(len(passphraselist)):
        Privkey += switcher.get(str(passphraselist[i]))
    return Privkey


#Open bitcoin - step 7 - Open bitcoin - Online
#Scan Descriptor - step 11 - Online
#Rescan Wallet - step 12 - Online
#Display Wallet - WP - Online
#Package - step 1 - Online
#Copy files to Drive - step 2 - Close bitcoin - Online
#Open bitcoin - auto redirect - Open bitcoin - Online
#Setup Disconnected - step 3 - Online # Run script and follow on the Disconnected 
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
        return redirect('/YCRopenbitcoin')
    return render_template('redirect.html')

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
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticold importmulti \'[{ "desc": "'+pubdesc+'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        if not (len(response[1]) == 0): 
            print(response)
            return "error response from importmulti: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticold importmulti \'[{ "desc": "'+pubdesc+'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''
        subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticold rescanblockchain 600000',shell=True,start_new_session=True)
    if request.method == 'POST':
        return redirect('/YCRdisplaywallet')
    return render_template('YCRrescanwallet.html')

@app.route("/YCRdisplaywallet", methods=['GET', 'POST'])
def YCRdisplaywallet():
    global selectedutxo
    global addresses
    global init
    if request.method == 'GET':
        subprocess.call(['rm -r ~/yeticold/static/address*'],shell=True)
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticold deriveaddresses "'+pubdesc+'" "[0,999]"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        listofaddresses = json.loads(response[0].decode("utf-8"))
        addresses = []
        for i in range(0, len(listofaddresses)):
            address = {}
            rpc = RPC()
            testlist = []
            testlist.append(listofaddresses[i])
            utxo = rpc.listunspent(1, 9999999, testlist)
            utxocount = len(utxo)
            address['utxocount'] = utxocount
            address['address'] = listofaddresses[i]
            if utxo != []:
                address['txid'] = utxo[0]['txid']
                address['vout'] = utxo[0]['vout']
                address['scriptPubKey'] = utxo[0]['scriptPubKey']
                address['amount'] = float(str(utxo[0]['amount']))
                amount = str(utxo[0]['amount'])
            else:
                address['amount'] = 0
                amount = "0.0000000"
            amount = "{:.8f}".format(float(amount))
            address['formatedAmount'] = amount
            total = rpc.getreceivedbyaddress(listofaddresses[i])
            address['totalbal'] = float(str(total))
            randomnum = str(random.randrange(0,1000000))
            route = url_for('static', filename='address'+listofaddresses[i]+''+randomnum+'.png')
            address['route'] = route
            addresses.append(address)
        addresses.sort(key=lambda x: x['amount'], reverse=True)
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
            if request.form['address'] == addresses[i]['address']:
                selectedutxo = addresses[i]
                break
        if init:
            return redirect('/YCRpackage')
        return redirect('/YCRdisplayutxoB')
    return render_template('YCRdisplaywallet.html', addresses=addresses, len=len(addresses))

@app.route("/YCRpackage", methods=['GET', 'POST'])
def YCRpackage():
    if request.method == 'GET':
        subprocess.call(['gnome-terminal -- bash -c "sudo chmod +x ~/yeticold/scripts/rpkg-script.sh; sudo ~/yeticold/scripts/rpkg-script.sh"'],shell=True)
    if request.method == 'POST':
        subprocess.call('python3 ~/yeticold/utils/stopbitcoin.py', shell=True)
        return redirect('/YCRcopyfiles')
    return render_template('YCRpackage.html')

@app.route("/YCRcopyfiles", methods=['GET', 'POST'])
def YCRcopyfiles():
    if request.method == 'POST':
        return redirect('/YCRrestartbitcoin')
    return render_template('YCRcopyfiles.html')

@app.route("/YCRrestartbitcoin", methods=['GET', 'POST'])
def YCRrestartbitcoin():
    global progress
    global IBD
    if request.method == 'GET':
        if BTCClosed():
            subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
    if request.method == 'POST':
        IBD = BTCRunning()
        if IBD:
            subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli loadwallet "yeticold"'],shell=True)
            return redirect('/YCRstartdisconnected')
        return redirect('/YCRrestartbitcoin')
    return render_template('YCRrestartbitcoin.html')

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
    if request.method == 'GET':
        home = os.getenv("HOME")
        if BTCClosed():
            subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
    if request.method == 'POST':
        IBD = BTCRunning()
        if IBD:
            subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yeticold"'],shell=True)
            return redirect('/YCRscandescriptorB')
    return render_template('YCRopenbitcoinB.html', progress=progress)

@app.route("/YCRscandescriptorB", methods=['GET', 'POST'])
def YCRscandescriptorB():
    global pubdesc
    if request.method == 'POST':
        pubdesc = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        return redirect('/YCRimportseeds')
    return render_template('YCRscandescriptorB.html')

@app.route('/YCRimportseeds', methods=['GET', 'POST'])
def YCRimportseeds():
    global pubdesc
    global privkeycount
    global init
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
            response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldpriv importmulti \'[{ "desc": '+desc+'#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false, "label": "test" }]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            print(response)
            init = True
            return redirect('/YCRswitchlaptop')
        else:
            return redirect('/YCRimportseeds')
    return render_template('YCRimportseeds.html', x=privkeycount + 1, error=error,i=privkeycount + 5)

@app.route("/YCRswitchlaptop", methods=['GET', 'POST'])
def YCRswitchlaptop():
    if request.method == 'POST':
        return redirect('/YCRscanutxo')
    return render_template('YCRswitchlaptop.html', progress=progress)

@app.route("/YCRdisplayutxo", methods=['GET', 'POST'])
def YCRdisplayutxo():
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
    return render_template('YCRdisplayutxo.html', qrdata=selectedutxo, path=path)

@app.route("/YCRscanutxo", methods=['GET', 'POST'])
def YCRscanutxo():
    global selectedutxo
    if request.method == 'POST':
        selectedutxo = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        selectedutxo = eval(selectedutxo.decode("utf-8"))
        return redirect('/YCRscanrecipent')
    return render_template('YCRscanutxo.html')

@app.route("/YCRscanrecipent", methods=['GET', 'POST'])
def YCRscanrecipent():
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
    return render_template('YCRscanrecipent.html', error=error)

@app.route("/YCRconfirmsend", methods=['GET', 'POST'])
def YCRconfirmsend():
    global receipentaddress
    if request.method == 'GET':
        rpc = RPC()
        amount = float(selectedutxo['amount'])
        minerfee = float(rpc.estimatesmartfee(1)["feerate"])
        kilobytespertrans = 0.200
        amo = (amount - (minerfee * kilobytespertrans))
        minerfee = (minerfee * kilobytespertrans)
        amo = "{:.8f}".format(float(amo))
        minerfee = "{:.8f}".format(float(minerfee))
    if request.method == 'POST':
        return redirect('/YCRdisplaytransaction')
    return render_template('YCRconfirmsend.html', amount=amo, minerfee=minerfee, recipent=receipentaddress)

@app.route("/YCRdisplaytransaction", methods=['GET', 'POST'])
def YCRdisplaytransaction():
    global selectedutxo
    global receipentaddress
    if request.method == 'GET':
        rpc = RPC()
        amount = float(selectedutxo['amount'])
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
        return redirect('/YCRscanutxoB')
    return render_template('YCRdisplaytransaction.html', qrdata=transhex, path=path)

@app.route("/YCRscantransaction", methods=['GET', 'POST'])
def YCRscantransaction():
    if request.method == 'POST':
        rpc = RPC()
        response = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        rpc.sendrawtransaction(response.decode("utf-8"))
        return redirect('/YCRdisplaywallet')
    return render_template('YCRscantransaction.html')

##Second folw

@app.route("/YCRdisplayutxoB", methods=['GET', 'POST'])
def YCRdisplayutxoB():
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
        return redirect('/YCRscantransactionB')
    return render_template('YCRdisplayutxoB.html', qrdata=selectedutxo, path=path)

@app.route("/YCRscanutxoB", methods=['GET', 'POST'])
def YCRscanutxoB():
    global selectedutxo
    if request.method == 'POST':
        selectedutxo = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        selectedutxo = json.loads(selectedutxo.decode("utf-8"))
        return redirect('/YCRscanrecipentB')
    return render_template('YCRscanutxoB.html')

@app.route("/YCRscanrecipentB", methods=['GET', 'POST'])
def YCRscanrecipentB():
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
            return redirect('/YCRscanrecipentB')
        return redirect('/YCRconfirmsendB')
    return render_template('YCRscanrecipentB.html', error=error)

@app.route("/YCRconfirmsendB", methods=['GET', 'POST'])
def YCRconfirmsendB():
    global receipentaddress
    if request.method == 'GET':
        amount = float(selectedutxo['amount'])
        minerfee = float(rpc.estimatesmartfee(1)["feerate"])
        kilobytespertrans = 0.200
        amo = (amount - (minerfee * kilobytespertrans))
        minerfee = (minerfee * kilobytespertrans)
        amo = "{:.8f}".format(float(amo))
    if request.method == 'POST':
        return redirect('/YCRdisplaytransactionB')
    return render_template('YCRconfirmsendB.html', amount=amo, minerfee=minerfee, recipent=receipentaddress)

@app.route("/YCRdisplaytransactionB", methods=['GET', 'POST'])
def YCRdisplaytransactionB():
    global selectedutxo
    global receipentaddress
    if request.method == 'GET':
        rpc = RPC()
        amount = float(selectedutxo['amount'])
        minerfee = float(rpc.estimatesmartfee(1)["feerate"])
        kilobytespertrans = 0.200
        amo = (amount - (minerfee * kilobytespertrans))
        minerfee = (minerfee * kilobytespertrans)
        amo = "{:.8f}".format(float(amo))
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet= createrawtransaction \'[{ "txid": "'+selectedutxo['txid']+'", "vout": '+str(selectedutxo['vout'])+'}]\' \'[{"'+receipentaddress+'" : '+str(amo)+'}]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        response = response[0].decode("utf-8")
        transonehex = response[:-1]
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet= signrawtransactionwithwallet '+transonehex+' \'[{"txid":"'+selectedutxo['txid']+'","vout":'+str(selectedutxo['vout'])+',"scriptPubKey":"'+selectedutxo['scriptPubKey']+'","amount":"'+str(amount)+'"}]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
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
        return redirect('/YCRscanutxoB')
    return render_template('YCRdisplaytransactionB.html', qrdata=transhex, path=path)

@app.route("/YCRscantransactionB", methods=['GET', 'POST'])
def YCRscantransactionB():
    if request.method == 'POST':
        rpc = RPC()
        response = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        rpc.sendrawtransaction(response.decode("utf-8"))
        return redirect('/YCRdisplaywallet')
    return render_template('YCRscantransactionB.html')










if __name__ == "__main__":
    app.run()
