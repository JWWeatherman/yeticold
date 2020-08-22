#IMPORTS
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
import sys

#VARIABLES
app = Flask(__name__)
home = os.getenv("HOME")
IBD = False
progress = 0
privkeylist = []
privkeycount = 0
xprivlist = []
pubdesc = ''
selectedutxo = ''
addresmses = ''
walletimported = False
error = ''
testblockchain = False
oldkeys = None

#FILE IMPORTS
sys.path.append(home + '/yeticold/utils/')
from formating import *
import forgetnetworks

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
    wallet_name = 'yeticold'
    uri = wallet_template.format(**settings, wallet_name=wallet_name)
    rpc = AuthServiceProxy(uri, timeout=600)  # 1 minute timeout
    return rpc

def blockheight():
    rpc = RPC()
    Blockinfo = rpc.getblockchaininfo()
    blockheight = 0
    if Blockinfo['pruned']:
        blockheight = Blockinfo['pruneheight']
    return str(blockheight)



#FLOW


#ROUTES

@app.route("/", methods=['GET', 'POST'])
def redirectroute():
    return redirect('/YCmenu')

@app.route("/YCmenu", methods=['GET', 'POST'])
def YCmenu():
    if request.method == 'POST':
        if request.form['option'] == 'startup':
            return redirect('/YCblockchain')
        else:
            return redirect('/YCRblockchain')
    return render_template('YCmenu.html')

#RECOVERY

@app.route("/YCRblockchain", methods=['GET', 'POST'])
def YCRblockchain():
    global home
    global rpcpsw
    global testblockchain
    if request.method == 'GET':
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
            testblockchain = True
            subprocess.Popen('python3 ~/yeticold/utils/testblockchain.py',shell=True,start_new_session=True)
        else:
            subprocess.call(['mkdir ~/.bitcoin'],shell=True)
            if request.form['date'] == '':
                subprocess.call('echo "server=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword='+rpcpsw+'" >> '+home+'/.bitcoin/bitcoin.conf', shell=True)
                return redirect('/YCopenbitcoin')
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
            subprocess.call('echo "server=1\nrpcport=8332\nrpcuser=rpcuser\nprune='+str(blockheight)+'\nrpcpassword='+rpcpsw+'" >> '+home+'/.bitcoin/bitcoin.conf', shell=True)
        return redirect('/YCRopenbitcoin')
    return render_template('YCRblockchain.html')

@app.route("/YCRopenbitcoin", methods=['GET', 'POST'])
def YCRopenbitcoin():
    global home
    global progress
    global IBD
    global testblockchain
    if request.method == 'GET':
        home = os.getenv("HOME")
        if (os.path.exists(home + "/.bitcoin")):
            testblockchain = False
        if BTCClosed():
            if testblockchain == False:
                subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        IBD = BTCFinished()
        progress = BTCprogress()
    if request.method == 'POST':
        if IBD:
            subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yeticold"'],shell=True)
            return redirect('/YCRscandescriptor')
        else:
            return redirect('/YCRopenbitcoin')
    return render_template('YCRopenbitcoin.html', progress=progress, IBD=IBD)

#SWITCH TO OFFLINE
@app.route("/YCRblockchainB", methods=['GET', 'POST'])
def YCRblockchainB():
    global rpcpsw
    global testblockchain
    global home
    if request.method == 'GET':
        if (os.path.exists(home + "/.bitcoin")):
            if (os.path.exists(home + "/.bitcoin/bitcoin.conf")):
                with open(".bitcoin/bitcoin.conf","r+") as f:
                    old = f.read()
                    f.seek(0)
                    new = "server=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword="+rpcpsw+"\n"
                    f.write(new + old)
            else:
                subprocess.call('echo "server=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword='+rpcpsw+'" >> '+home+'/.bitcoin/bitcoin.conf', shell=True)
        else:
            subprocess.call('echo "server=1\nrpcport=8332\nrpcuser=rpcuser\nprune=550\nrpcpassword='+rpcpsw+'" >> '+home+'/.bitcoin/bitcoin.conf', shell=True)
    return redirect('/YCRopenbitcoinB')

@app.route("/YCRopenbitcoinB", methods=['GET', 'POST'])
def YCRopenbitcoinB():
    global home
    global progress
    global IBD
    global testblockchain
    if request.method == 'GET':
        home = os.getenv("HOME")
        if (os.path.exists(home + "/.bitcoin")):
            testblockchain = False
        if BTCClosed():
            if testblockchain == False:
                subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        IBD = BTCFinished()
        progress = BTCprogress()
    if request.method == 'POST':
        if IBD:
            subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yeticold"'],shell=True)
            return redirect('/YCRconnection')
        else:
            return redirect('/YCRopenbitcoinB')
    return render_template('YCRopenbitcoinB.html', progress=progress, IBD=IBD)

@app.route("/YCRconnection", methods=['GET', 'POST'])
def YCRconnection():
    if request.method == 'POST':
        forgetnetworks.forget_networks()
        return redirect('/YCRswitchlaptop')
    return render_template('YCRconnection.html')

@app.route("/YCRswitchlaptop", methods=['GET', 'POST'])
def YCRswitchlaptop():
    if request.method == 'POST':
        return redirect('/YCRscanutxo')
    return render_template('YCRswitchlaptop.html')

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
    global rpcpsw
    global walletimported
    global pubdesc
    if request.method == 'GET':
        subprocess.call(['rm -r ~/yeticold/static/address*'],shell=True)
        pubdesc = pubdesc.replace('\n', '')
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
            print(response)
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
        if walletimported:
            return redirect('/YCRdisplayutxoB')
        return redirect('/YCRdisplayutxo')
    return render_template('YCRdisplaywallet.html', addresses=addresses, len=len(addresses), TWB=totalwalletbal)

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
        return redirect('/YCRscandescriptorB')
    return render_template('YCRscanutxo.html')

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
    global error
    global privkeylist
    global walletimported
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
            walletimported = True
            return redirect('/YCRscanrecipent')
        else:
            return redirect('/YCRimportseeds')
    return render_template('YCRimportseeds.html', x=privkeycount + 1, error=error,i=privkeycount + 4)

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
        amount = float(selectedutxo['balance'])
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
        return redirect('/YCRscanutxoB')
    return render_template('YCRdisplaytransaction.html', qrdata=transhex, path=path)

@app.route("/YCRscantransaction", methods=['GET', 'POST'])
def YCRscantransaction():
    if request.method == 'POST':
        response = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        transactionhex = response.decode("utf-8")
        print(transactionhex)
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet= sendrawtransaction '+transactionhex],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return redirect('/YCRdisplaywallet')
    return render_template('YCRscantransaction.html')

#REPEAT RECOVERY

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
        selectedutxo = eval(selectedutxo.decode("utf-8"))
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
        rpc = RPC()
        amount = float(selectedutxo['balance'])
        minerfee = float(rpc.estimatesmartfee(1)["feerate"])
        kilobytespertrans = 0.200
        amo = (amount - (minerfee * kilobytespertrans))
        minerfee = (minerfee * kilobytespertrans)
        amo = "{:.8f}".format(float(amo))
        minerfee = "{:.8f}".format(float(minerfee))
    if request.method == 'POST':
        return redirect('/YCRdisplaytransactionB')
    return render_template('YCRconfirmsendB.html', amount=amo, minerfee=minerfee, recipent=receipentaddress)

@app.route("/YCRdisplaytransactionB", methods=['GET', 'POST'])
def YCRdisplaytransactionB():
    global selectedutxo
    global receipentaddress
    if request.method == 'GET':
        rpc = RPC()
        amount = float(selectedutxo['balance'])
        minerfee = float(rpc.estimatesmartfee(1)["feerate"])
        kilobytespertrans = 0.200
        amo = (amount - (minerfee * kilobytespertrans))
        minerfee = (minerfee * kilobytespertrans)
        amo = float("{:.8f}".format(float(amo)))
        if amo <= 0:
            error = "Amount is too small to account for the fee. Try sending a larger amount. You will need to restart both laptops and follow the steps on yeticold.com/"
            return error
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
    return render_template('YCRdisplaytransactionB.html', qrdata=transhex, path=path)

@app.route("/YCRscantransactionB", methods=['GET', 'POST'])
def YCRscantransactionB():
    if request.method == 'POST':
        response = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        transactionhex = response.decode("utf-8")
        print(transactionhex)
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet= sendrawtransaction '+transactionhex],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return redirect('/YCRdisplaywallet')
    return render_template('YCRscantransactionB.html')

#SETUP
@app.route("/YCblockchain", methods=['GET', 'POST'])
def YCblockchain():
    global home
    global rpcpsw
    global testblockchain
    if request.method == 'GET':
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
            testblockchain = True
            subprocess.Popen('python3 ~/yeticold/utils/testblockchain.py',shell=True,start_new_session=True)
        elif request.form['option'] == 'largeharddrive':
            subprocess.call('echo "server=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword='+rpcpsw+'" >> '+home+'/.bitcoin/bitcoin.conf', shell=True)
            return redirect('/YCopenbitcoin')
        elif request.form['option'] == 'smallharddrive':
            subprocess.call(['mkdir ~/.bitcoin'],shell=True)
            subprocess.call('echo "server=1\nrpcport=8332\nrpcuser=rpcuser\nprune=550\nrpcpassword='+rpcpsw+'" >> '+home+'/.bitcoin/bitcoin.conf', shell=True)
        return redirect('/YCopenbitcoin')
    return render_template('YCblockchain.html')

@app.route("/YCopenbitcoin", methods=['GET', 'POST'])
def YCopenbitcoin():
    global home
    global progress
    global IBD
    global testblockchain
    if request.method == 'GET':
        home = os.getenv("HOME")
        if (os.path.exists(home + "/.bitcoin")):
            testblockchain = False
        if BTCClosed():
            if testblockchain == False:
                subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        IBD = BTCFinished()
        progress = BTCprogress()
    if request.method == 'POST':
        if IBD:
            subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yeticold"'],shell=True)
            return redirect('/YCscandescriptor')
        else:
            return redirect('/YCopenbitcoin')
    return render_template('YCopenbitcoin.html', progress=progress, IBD=IBD)

#SWITCH TO OFFLINE
@app.route("/YCblockchainB", methods=['GET', 'POST'])
def YCblockchainB():
    global rpcpsw
    global testblockchain
    global home
    if request.method == 'GET':
        if (os.path.exists(home + "/.bitcoin")):
            if (os.path.exists(home + "/.bitcoin/bitcoin.conf")):
                with open(".bitcoin/bitcoin.conf","r+") as f:
                    old = f.read()
                    f.seek(0)
                    new = "server=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword="+rpcpsw+"\n"
                    f.write(new + old)
            else:
                subprocess.call('echo "server=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword='+rpcpsw+'" >> '+home+'/.bitcoin/bitcoin.conf', shell=True)
        else:
            testblockchain = True
            subprocess.Popen('python3 ~/yeticold/utils/testblockchain.py',shell=True,start_new_session=True)
            subprocess.call('echo "server=1\nrpcport=8332\nrpcuser=rpcuser\nprune=550\nrpcpassword='+rpcpsw+'" >> '+home+'/.bitcoin/bitcoin.conf', shell=True)
    return redirect('/YCopenbitcoinB')

@app.route("/YCopenbitcoinB", methods=['GET', 'POST'])
def YCopenbitcoinB():
    global home
    global progress
    global IBD
    global testblockchain
    if request.method == 'GET':
        home = os.getenv("HOME")
        if (os.path.exists(home + "/.bitcoin")):
            testblockchain = False
        if BTCClosed():
            if testblockchain == False:
                subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        IBD = BTCFinished()
        progress = BTCprogress()
    if request.method == 'POST':
        if IBD:
            subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yeticold"'],shell=True)
            return redirect('/YCconnection')
        else:
            return redirect('/YCopenbitcoinB')
    return render_template('YCopenbitcoinB.html', progress=progress, IBD=IBD)

@app.route("/YCconnection", methods=['GET', 'POST'])
def YCconnection():
    if request.method == 'POST':
        forgetnetworks.forget_networks()
        return redirect('/YCgetseeds')
    return render_template('YCconnection.html')

@app.route("/YCgetseeds", methods=['GET', 'POST'])
def YCgetseeds():
    global privkeylist
    global privkeycount
    global xprivlist
    global pubdesc
    global home
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
            pathtwo = home + '/yeticoldwallet' + str(i)
            path = home + '/yeticoldwallettwo' + str(i)
            subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yeticoldwallettwo'+str(i)+'"'],shell=True)
            subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli loadwallet "yeticoldwallettwo'+str(i)+'"'],shell=True)
            response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwallettwo'+str(i)+' sethdseed true "'+privkeylist[i]+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            if not (len(response[1]) == 0): 
                print(response)
                return "error response from sethdseed: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwallettwo'+str(i)+' sethdseed true "'+privkeylist[i]+'"'
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
        pubdesc = response["descriptor"]
        seedpath = home + '/Documents'
        subprocess.call('rm -r '+seedpath+'/ycseed*', shell=True)
        privdesc = '"wsh(multi(3,'+xprivlist[0]+'/*,'+xprivlist[1]+'/*,'+xprivlist[2]+'/*,'+xprivlist[3]+'/*,'+xprivlist[4]+'/*,'+xprivlist[5]+'/*,'+xprivlist[6]+'/*))'
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yeticoldpriv"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldpriv getdescriptorinfo '+privdesc+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        response = json.loads(response[0].decode("utf-8"))
        checksum = response["checksum"]
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldpriv importmulti \'[{ "desc": '+privdesc+'#'+ checksum +'", "timestamp": "now", "range": [0,999], "watchonly": false}]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        walletimported = True
        return redirect('/YCdisplaydescriptor')
    return render_template('YCgetseeds.html')

@app.route("/YCdisplaydescriptor", methods=['GET', 'POST'])
def YCdisplaydescriptor():
    global privkeylist
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
        return redirect('/YCdisplayseeds')
    return render_template('YCdisplaydescriptor.html', qrdata=pubdesc, path=path)

@app.route("/YCscandescriptor", methods=['GET', 'POST'])
def YCscandescriptor():
    global pubdesc
    if request.method == 'POST':
        pubdesc = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        pubdesc = pubdesc.decode("utf-8")
        pubdesc = pubdesc.replace('\n', '')
        subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticold importmulti \'[{ "desc": "'+pubdesc+'", "timestamp": "now", "range": [0,999], "watchonly": false}]\' \'{"rescan": true}\''],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return redirect('/YCprintpage')
    return render_template('YCscandescriptor.html')

@app.route("/YCprintpage", methods=['GET', 'POST'])
def YCprintpage():
    global pubdesc
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
        qr.add_data(pubdesc)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        home = os.getenv("HOME")
        img.save(home + '/yeticold/static/firstqrcode' + firstqrname + '.png')
    if request.method == 'POST':
        return redirect('/YCswitchlaptop')
    return render_template('YCprintpage.html', qrdata=pubdesc, path=path)

@app.route("/YCswitchlaptop", methods=['GET', 'POST'])
def YCswitchlaptop():
    if request.method == 'POST':
        return redirect('/YCRdisplaywallet')
    return render_template('YCswitchlaptop.html')

@app.route('/YCdisplayseeds', methods=['GET', 'POST'])
def YCdisplayseeds():
    global privkeylist
    global privkeycount
    global pubdesc
    if request.method == 'GET':
        privkey = privkeylist[privkeycount]
        passphraselist = ConvertToPassphrase(privkey)
    if request.method == 'POST':
        home = os.getenv('HOME')
        path = home + '/Documents'
        subprocess.call('mkdir '+path+'/ycseed'+str(privkeycount + 1), shell=True)
        subprocess.call('touch '+path+'/ycseed'+str(privkeycount + 1)+'/ycseed'+str(privkeycount + 1)+'.txt', shell=True)
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
        subprocess.call('echo "'+file+'" >> '+path+'/ycseed'+str(privkeycount + 1)+'/ycseed'+str(privkeycount + 1)+'.txt', shell=True)
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
        img.save(home + '/Documents/ycseed'+str(privkeycount + 1)+'/descriptor.png')
        privkeycount = privkeycount + 1
        if (privkeycount == 7):
            privkeycount = 0
            return redirect('/YCcheckseeds')
        else:
            return redirect('/YCdisplayseeds')
    return render_template('YCdisplayseeds.html', PPL=passphraselist, x=privkeycount + 1, i=privkeycount + 16)

@app.route('/YCcheckseeds', methods=['GET', 'POST'])
def YCcheckseeds():
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
                    home = os.getenv('HOME')
                    path = home + '/yeticoldwallet' + str(i)
                    subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yeticoldwallet'+str(i)+'" false true'],shell=True)
                    subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli loadwallet "yeticoldwallet'+str(i)+'"'],shell=True)
                    response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwallet'+str(i)+' sethdseed true "'+privkeylist[i]+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                    if not (len(response[1]) == 0): 
                        print(response)
                        return "error response from sethdseed: " + str(response[1]) + '\n' + '~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yeticoldwallet'+str(i)+' sethdseed true "'+privkeylist[i]+'"'
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
            error = 'The seed words you entered are incorrect. This is probably because you entered a line twice or put them in the wrong order.'
    return render_template('YCcheckseeds.html', x=privkeycount + 1, error=error,i=privkeycount + 23,oldkeys=oldkeys)

@app.route("/YCcopyseeds", methods=['GET', 'POST'])
def YCcopyseeds():
    if request.method == 'POST':
        return redirect('/YCswitchlaptopB')
    return render_template('YCcopyseeds.html')

@app.route("/YCswitchlaptopB", methods=['GET', 'POST'])
def YCswitchlaptopB():
    if request.method == 'POST':
        return redirect('/YCRscanutxoB')
    return render_template('YCswitchlaptopB.html')

if __name__ == "__main__":
    app.run()