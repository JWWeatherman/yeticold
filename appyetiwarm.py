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
from datetime import datetime
import time
import sys
app = Flask(__name__)

#VARIBALES 
home = os.getenv("HOME")
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
walletimported = False
pubdesc = None
adrlist = []
transnum = 0
progress = 0
samedesc = False
utxo = None
rescan = False
oldkeys = None

#FILE IMPORTS
sys.path.append(home + '/yeticold/utils/')
from formating import *
import testblockchain

#RPC
rpcpsw = str(random.randrange(0,1000000))
settings = {"rpc_username": "rpcuser","rpc_password": rpcpsw,"rpc_host": "127.0.0.1","rpc_port": 8332,"address_chunk": 100}
wallet_template = "http://{rpc_username}:{rpc_password}@{rpc_host}:{rpc_port}/wallet/{wallet_name}"

def BTCprogress():
    if not (os.path.exists(home + "/.bitcoin")):
        return 0
    response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli getblockchaininfo'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if not (len(response[0]) == 0):
        bitcoinprogress = json.loads(response[0].decode("utf-8"))['verificationprogress']
        bitcoinprogress = bitcoinprogress * 100
        bitcoinprogress = round(bitcoinprogress, 3)
    else:
        bitcoinprogress = 0
    return bitcoinprogress

def BTCFinished():
    if not (os.path.exists(home + "/.bitcoin")):
        return False
    response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli getblockchaininfo'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if not (len(response[0]) == 0):
        bitcoinprogress = json.loads(response[0].decode("utf-8"))['initialblockdownload']
    else:
        bitcoinprogress = True
    return not bitcoinprogress

def BTCClosed():
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
    wallet_name = 'yetiwarm'
    uri = wallet_template.format(**settings, wallet_name=wallet_name)
    rpc = AuthServiceProxy(uri, timeout=600)  # 1 minute timeout
    return rpc

def get_blockheight():
    rpc = RPC()
    Blockinfo = rpc.getblockchaininfo()
    blockheight = 0
    if Blockinfo['pruned']:
        blockheight = Blockinfo['pruneheight']
    return str(blockheight)

def choose_blockchain(request):
    if request.form['option'] == 'downloadblockchain':
        testblockchain.get_test_blockchain()
    else:
        subprocess.call(['mkdir ~/.bitcoin'],shell=True)
        if request.form['date'] == '':
            subprocess.call('echo "server=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword='+rpcpsw+'" >> '+home+'/.bitcoin/bitcoin.conf', shell=True)
        else:
            fmt = '%Y-%m-%d %H:%M:%S'
            today = str(datetime.today()).split('.')[0]
            d1 = datetime.strptime(request.form['date'] + ' 12:0:0', fmt)
            d2 = datetime.strptime(today, fmt)
            d1_ts = time.mktime(d1.timetuple())
            d2_ts = time.mktime(d2.timetuple())
            diff = (int(d2_ts - d1_ts) / 60) / 10
            add = diff / 10
            blockheight = diff + add + 550
            blockheight = int(blockheight)
            subprocess.call('echo "server=1\nrpcport=8332\nrpcuser=rpcuser\nprune='+str(blockheight)+'\nrpcpassword='+rpcpsw+'" >> '+home+'/.bitcoin/bitcoin.conf', shell=True)

def populate_bitcoin_conf():
    if (os.path.exists(home + "/.bitcoin/bitcoin.conf")):
        with open(home + "/.bitcoin/bitcoin.conf","r+") as f:
            old = f.read()
            f.seek(0)
            new = "server=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword="+rpcpsw+"\n"
            f.write(new + old)
    else:
        subprocess.call('echo "server=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword='+rpcpsw+'" >> '+home+'/.bitcoin/bitcoin.conf', shell=True)

#FLOW
#FLOW ONE
#YWblockchain 
#YWopenbitcoin - step 6
#YWmenu - step 7
#CHOOSE CREATE NEW
#YWgetseeds - step 8
#YWdisplayseeds - step 9 - 15
#YWcheckseeds - step 16 - 22
#YWprintdescriptor - step 23
#YWcopyseeds - step 24
#FLOW TWO
#YWblockchain
#YWopenbitcoin - step 6
#YWmenu - step 7
#CHOOSE RECOVER WALLET
#YWRscanddescriptor - step 8
#YWRrescanwallet - step 9
#YWRdisplaywallet - WP 
#YWRscanrecipent - step 1
#YWRimportseeds - step 2 - 4
#YWRsendtransaction - step 5
#FLOW THREE
#YWRdisplaywallet - WP
#YWRscanrecipent - step 1
#YWRsendtransactionB - step 2 

#ROUTES
@app.route("/", methods=['GET', 'POST'])
def redirectroute():
    if request.method == 'GET':
        return redirect('/YWblockchain')
    return render_template('redirect.html')

@app.route("/YWblockchain", methods=['GET', 'POST'])
def YWblockchain():
    if request.method == 'GET':
        if (os.path.exists(home + "/.bitcoin")):
            populate_bitcoin_conf()
            return redirect('/YWopenbitcoin')
    if request.method == 'POST':
        choose_blockchain(request)
        return redirect('/YWopenbitcoin')
    return render_template('YWblockchain.html')

@app.route("/YWopenbitcoin", methods=['GET', 'POST'])
def YWopenbitcoin():
    global home
    global progress
    global IBD
    if request.method == 'GET':
        home = os.getenv("HOME")
        if BTCClosed():
            subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        IBD = BTCFinished()
        progress = BTCprogress()
    if request.method == 'POST':
        if IBD:
            subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetiwarm"'],shell=True)
            return redirect('/YWmenu')
        else:
            return redirect('/YWopenbitcoin')
    return render_template('YWopenbitcoin.html', progress=progress, IBD=IBD)


@app.route("/YWmenu", methods=['GET', 'POST'])
def YWmenu():
    if request.method == 'POST':
        if request.form['option'] == 'recovery':
            return redirect('/YWRscandescriptor')
        else:
            return redirect('/YWgetseeds')
    return render_template('YWmenu.html')

@app.route("/YWgetseeds", methods=['GET', 'POST'])
def YWgetseeds():
    global privkeylist
    global privkeycount
    global xprivlist
    global pubdesc
    global walletimported
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
            pathtwo = home + '/yetiwarmwallet' + str(i)
            path = home + '/yetiwarmwallettwo' + str(i)
            subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetiwarmwallettwo'+str(i)+'"'],shell=True)
            response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwarmwallettwo'+str(i)+' sethdseed true "'+privkeylist[i]+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            print(response)
            response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwarmwallettwo'+str(i)+' dumpwallet "yetiwarmwallettwo'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
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
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwarm getdescriptorinfo "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        response = json.loads(response[0].decode("utf-8"))
        print(response)
        checksum = response["checksum"]
        pubdesc = response["descriptor"].replace('\n', '')
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwarm importmulti \'[{ "desc": "'+pubdesc+'", "timestamp": "now", "range": [0,999], "watchonly": false}]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetiwarmpriv"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwarmpriv importmulti \'[{ "desc": "wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))#'+checksum+'", "timestamp": "now", "range": [0,999], "watchonly": false}]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        walletimported = True
        print(walletimported)
        home = os.getenv('HOME')
        path = home + '/Documents'
        subprocess.call('rm -r '+path+'/ywseed*', shell=True)
        return redirect('/YWprintdescriptor')
    return render_template('YWgetseeds.html')

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
        return redirect('/YWdisplayseeds')
    return render_template('YWprintdescriptor.html', qrdata=pubdesc, path=path)

@app.route('/YWdisplayseeds', methods=['GET', 'POST'])
def YWdisplayseeds():
    global privkeylist
    global privkeycount
    global pubdesc
    if request.method == 'GET':
        privkey = privkeylist[privkeycount]
        passphraselist = ConvertToPassphrase(privkey)
    if request.method == 'POST':
        home = os.getenv('HOME')
        path = home + '/Documents'
        subprocess.call('mkdir '+path+'/ywseed'+str(privkeycount + 1), shell=True)
        subprocess.call('touch '+path+'/ywseed'+str(privkeycount + 1)+'/ywseed'+str(privkeycount + 1)+'.txt', shell=True)
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
        subprocess.call('echo "'+file+'" >> '+path+'/ywseed'+str(privkeycount + 1)+'/ywseed'+str(privkeycount + 1)+'.txt', shell=True)
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
        img.save(home + '/Documents/ywseed'+str(privkeycount + 1)+'/descriptor.png')
        privkeycount = privkeycount + 1
        if (privkeycount == 7):
            privkeycount = 0
            return redirect('/YWcheckseeds')
        else:
            return redirect('/YWdisplayseeds')
    return render_template('YWdisplayseeds.html', PPL=passphraselist, x=privkeycount + 1, i=privkeycount + 9)

@app.route('/YWcheckseeds', methods=['GET', 'POST'])
def YWcheckseeds():
    global privkeylist
    global xprivlist
    global privkeycount
    global error
    global oldkeys
    if request.method == 'POST':
        privkey = privkeylist[privkeycount]
        passphraselist = ConvertToPassphrase(privkey)
        privkeylisttoconfirm = []
        oldkeys = []
        for i in range(1,14):
            inputlist = request.form['row' + str(i)]
            oldkeys.append(inputlist)
            inputlist = inputlist.split(' ')
            inputlist = inputlist[0:4]
            privkeylisttoconfirm.append(inputlist[0])
            privkeylisttoconfirm.append(inputlist[1])
            privkeylisttoconfirm.append(inputlist[2])
            privkeylisttoconfirm.append(inputlist[3])
        if privkeylisttoconfirm == passphraselist:
            oldkeys = None
            error = None
            privkeycount = privkeycount + 1
            if (privkeycount >= 7):
                privkeycount = 7
                newxprivlist = []
                for i in range(0,7):
                    rpc = RPC()
                    home = os.getenv('HOME')
                    path = home + '/yetiwarmwallettwo' + str(i)
                    subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetiwarmwallettwo'+str(i)+'" false true'],shell=True)
                    response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwarmwallettwo'+str(i)+' sethdseed true "'+privkeylist[i]+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                    print(response)
                    response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwarmwallettwo'+str(i)+' dumpwallet "yetiwarmwallettwo'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
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
                return redirect('/YWcopyseeds')
            else:
                return redirect('/YWcheckseeds')
        else:
            error = 'The seed words you entered are incorrect. This is probably because you entered a line twice or put them in the wrong order.'
    return render_template('YWcheckseeds.html', x=privkeycount + 1, error=error,i=privkeycount + 16,oldkeys=oldkeys)



@app.route("/YWcopyseeds", methods=['GET', 'POST'])
def YWcopyseeds():
    if request.method == 'POST':
        return redirect('/YWRdisplaywallet')
    return render_template('YWcopyseeds.html')

@app.route("/YWRscandescriptor", methods=['GET', 'POST'])
def YWRscandescriptor():
    global firstqrcode
    global pubdesc
    if request.method == 'POST':
        firstqrcode = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        pubdesc = firstqrcode.decode("utf-8").replace('\n', '')
        return redirect('/YWRrescanwallet')
    return render_template('YWRscandescriptor.html', pubdesc=pubdesc)

@app.route("/YWRrescanwallet", methods=['GET', 'POST'])
def YWRrescanwallet():
    global firstqrcode
    global pubdesc
    if request.method == 'GET':
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwarm importmulti \'[{ "desc": "'+pubdesc+'", "timestamp": "now", "range": [0,999], "watchonly": false}]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwarm rescanblockchain '+get_blockheight(),shell=True,start_new_session=True)
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
        totalwalletbal = 0
        subprocess.call(['rm -r ~/yeticold/static/address*'],shell=True)
        adrlist = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwarm deriveaddresses "'+pubdesc+'" "[0,999]"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        adrlist = json.loads(adrlist[0].decode("utf-8"))
        rpc = RPC()
        for i in range(0, len(adrlist)):
            adr = adrlist[i]
            randomnum = str(random.randrange(0,1000000))
            route = url_for('static', filename='address'+adr+''+randomnum+'.png')
            response = rpc.listunspent(0, 9999999, [adr])
            if response == []:
                # rpc.importaddress(adrlist[i],False,False)
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
            if addresses[i]['txid'] == request.form['txid']:
                sourceaddress = addresses[i]
        return redirect('/YWRscanrecipent')
    return render_template('YWRdisplaywallet.html', addresses=addresses, len=len(addresses), TWB=totalwalletbal)

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
            receipentaddress = request.form['option']
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
    global imported
    global walletimported
    if request.method == 'GET':
        if walletimported:
            return redirect('/YWRsendtransactionB')
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
                path = home + '/yetiwarmwallet' + str(i)
                subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetiwarmwallet'+str(i)+'" false true'],shell=True)
                response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwarmwallet'+str(i)+' sethdseed true "'+privkeylist[i]+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwarmwallet'+str(i)+' dumpwallet "yetiwarmwallet'+str(i)+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
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
                response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwarm getdescriptorinfo "pk('+privkeyline+')"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                print(response)
                response = response[0].decode("utf-8")
                xpub = response.split('(')[1].split(')')[0]
                newxpublist.append(xpub)
            privkeycount = 0
            xpublist = pubdesc.split(',')[1:]
            xpublist[6] = xpublist[6].split('))')[0]
            descriptorlist = xpublist
            print(xpublist)
            print(newxpublist)
            for i in range(0,3):
                xpub = newxpublist[i] + '/*'
                for x in range(0,7):
                    oldxpub = xpublist[x]
                    print('match')
                    print(xpub)
                    print(oldxpub)
                    print(x)
                    print(i)
                    print()
                    if xpub == oldxpub:
                        descriptorlist[x] = (xprivlist[i] + '/*')
                        break
            desc = '"wsh(multi(3,'+descriptorlist[0]+','+descriptorlist[1]+','+descriptorlist[2]+','+descriptorlist[3]+','+descriptorlist[4]+','+descriptorlist[5]+','+descriptorlist[6]+'))'
            print(desc)
            response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetiwarmpriv"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwarmpriv getdescriptorinfo '+desc+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            print(response)
            response = json.loads(response[0].decode("utf-8"))
            checksum = response["checksum"]
            response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwarmpriv importmulti \'[{ "desc": '+desc+'#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false}]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            walletimported = True
            print(response)
            return redirect('/YWRsendtransaction')
        else:
            return redirect('/YWRimportseeds')
    return render_template('YWRimportseeds.html', x=privkeycount + 1, error=error,i=privkeycount + 2 )

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
    global error
    if request.method == 'GET':
        rpc = RPC()
        minerfee = float(rpc.estimatesmartfee(1)["feerate"])
        kilobytespertrans = 0.200
        minerfee = (minerfee * kilobytespertrans)
        amo = (float(sourceaddress['numbal']) - minerfee)
        amo = "{:.8f}".format(float(amo))
        print(amo)
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwarmpriv createrawtransaction \'[{ "txid": "'+sourceaddress['txid']+'", "vout": '+str(sourceaddress['vout'])+'}]\' \'[{"'+receipentaddress+'" : '+str(amo)+'}]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        response = response[0].decode("utf-8")
        transonehex = response[:-1]
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwarmpriv signrawtransactionwithwallet '+transonehex],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        response = json.loads(response[0].decode("utf-8"))
        if not response['complete']:
            error = response['errors'][0]['error']
            return redirect('/YWRerror')
        transnum = response
        minerfee = "{:.8f}".format(minerfee)
    if request.method == 'POST':
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwarmpriv sendrawtransaction '+transnum['hex']+''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        return redirect('/YWRdisplaywallet')
    return render_template('YWRsendtransaction.html', amount=amo, minerfee=minerfee, recipent=receipentaddress)

#GEN trans qr code
@app.route("/YWRsendtransactionB", methods=['GET', 'POST'])
def YWRsendtransactionB():
    global xprivlist
    global newxpublist
    global pubdesc
    global sourceaddress
    global receipentaddress
    global minerfee
    global transnum
    global error
    if request.method == 'GET':
        rpc = RPC()
        minerfee = float(rpc.estimatesmartfee(1)["feerate"])
        kilobytespertrans = 0.200
        minerfee = (minerfee * kilobytespertrans)
        amo = (float(sourceaddress['numbal']) - minerfee)
        amo = "{:.8f}".format(float(amo))
        if amo <= 0:
            error = "Amount is too small to account for the fee. Try sending a larger amount."
            return redirect('/YWRerror')
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwarmpriv createrawtransaction \'[{ "txid": "'+sourceaddress['txid']+'", "vout": '+str(sourceaddress['vout'])+'}]\' \'[{"'+receipentaddress+'" : '+str(amo)+'}]\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        response = response[0].decode("utf-8")
        transonehex = response[:-1]
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwarmpriv signrawtransactionwithwallet '+transonehex],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        response = json.loads(response[0].decode("utf-8"))
        if not response['complete']:
            error = response['errors'][0]['error']
            return redirect('/YWRerror')
        transnum = response
        minerfee = "{:.8f}".format(minerfee)
    if request.method == 'POST':
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwarmpriv sendrawtransaction '+transnum['hex']+''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        return redirect('/YWRdisplaywallet')
    return render_template('YWRsendtransactionB.html', amount=amo, minerfee=minerfee, recipent=receipentaddress)

#GEN trans qr code
@app.route("/YWRerror", methods=['GET', 'POST'])
def YWRerror():
    global error
    global walletimported
    if request.method == 'POST':
        error = None
        subprocess.call('python3 ~/yeticold/utils/stopbitcoin.py', shell=True)
        subprocess.call('rm -r ~/.bitcoin/yetiwarmpriv', shell=True)
        walletimported = False
        return redirect('/YWRopenbitcoinB')
    return render_template('YWRerror.html',error=error)

@app.route("/YWopenbitcoinB", methods=['GET', 'POST'])
def YWopenbitcoinB():
    global home
    global progress
    global IBD
    if request.method == 'GET':
        home = os.getenv("HOME")
        if BTCClosed():
            subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        IBD = BTCFinished()
        progress = BTCprogress()
    if request.method == 'POST':
        if IBD:
            subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetiwarm"'],shell=True)
            return redirect('/YWRimportseeds')
        else:
            return redirect('/YWopenbitcoinB')
    return render_template('YWopenbitcoinB.html', progress=progress, IBD=IBD)

if __name__ == "__main__":
    app.run()
