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
app = Flask(__name__)

#VARIBLES
home = os.getenv("HOME")
progress = 0
parsedutxos = []
selectedutxo = {}
error = ""
receipentaddress = ""
signtransactionhex = ""
totalamount = ""
testblockchain = False

#FILE IMPORTS
sys.path.append(home + '/yeticold/utils/')
from formating import *

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

def get_blockheight():
    rpc = RPC()
    Blockinfo = rpc.getblockchaininfo()
    blockheight = 0
    if Blockinfo['pruned']:
        blockheight = Blockinfo['pruneheight']
    return str(blockheight)

def choose_blockchain(request, testblockchain):
    if request.form['option'] == 'downloadblockchain':
        testblockchain = True
        subprocess.Popen('python3 ~/yeticold/utils/testblockchain.py',shell=True,start_new_session=True)
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
    return testblockchain

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
#BCblockchain - ONLINE
#Open bitcoin - step 6 - ONLINE
#BCstartdisconnected - step 7 - ONLINE
#off.yeticold.com - step 8 - DISCONNECTED
#BCblockchainB - DISCONNECTED
#BCopenbitcoinB - step 9 - DISCONNECTED
#BCconnection - step 10 - DISCONNECTED
#Import keys - step 11 - DISCONNECTED
#Display utxos - WP - DISCONNECTED
#Scan recipent - step 1 - DISCONNECTED 
#Confirm send transaction - step 2 - DISCONNECTED
#Display signed transaction - step 3 - DISCONNECTED 
#Scan sign transaction - step 4 - ONLINE
#BCswitchlaptop - step 5 - ONLINE

@app.route("/", methods=['GET', 'POST'])
def redirectroute():
    return redirect('/BCblockchain')

@app.route("/BCblockchain", methods=['GET', 'POST'])
def BCblockchain():
    global testblockchain
    if request.method == 'GET':
        if (os.path.exists(home + "/.bitcoin")):
            populate_bitcoin_conf()
            return redirect('/BCopenbitcoin')
        time.sleep(5)
    if request.method == 'POST':
        testblockchain = choose_blockchain(request, testblockchain)
        return redirect('/BCopenbitcoin')
    return render_template('BCblockchain.html')

@app.route("/BCopenbitcoin", methods=['GET', 'POST'])
def BCopenbitcoin():
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
            return redirect('/BCstartdisconnected')
        else:
            return redirect('/BCopenbitcoin')
    return render_template('BCopenbitcoin.html', progress=progress, IBD=IBD)

@app.route("/BCstartdisconnected", methods=['GET', 'POST'])
def BCstartdisconnected():
    if request.method == 'POST':
        return redirect('/BCscantransaction')
    return render_template('BCstartdisconnected.html')

@app.route("/BCblockchainB", methods=['GET', 'POST'])
def BCblockchainB():
    global testblockchain
    if request.method == 'GET':
        if (os.path.exists(home + "/.bitcoin")):
            populate_bitcoin_conf()
            return redirect('/BCopenbitcoinC')
        time.sleep(5)
    if request.method == 'POST':
        testblockchain = choose_blockchain(request, testblockchain)
        return redirect('/BCopenbitcoinC')
    return render_template('BCblockchainB.html')

@app.route("/BCopenbitcoinC", methods=['GET', 'POST'])
def BCopenbitcoinC():
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
            return redirect('/BCimportkeys')
        else:
            return redirect('/BCopenbitcoinC')
    return render_template('BCopenbitcoinC.html', progress=progress, IBD=IBD)

@app.route("/BCimportkeys", methods=['GET', 'POST'])
def BCimportkeys():
    if request.method == 'POST':
        text = request.form['textarea']
        if text:
            textlist = text.split('\n')
            for i in range(0,len(textlist) - 1):
                privkey = textlist[i].split(',')[3]
                if privkey[1] == 'L' or privkey[1] == 'K':
                    rpc = RPC()
                    rpc.importprivkey(privkey, 'privkeylabel', False)
        return redirect('/BCrescan')
    return render_template('BCimportkeys.html')

@app.route("/BCrescan", methods=['GET', 'POST'])
def BCrescan():
    if request.method == 'GET':
        subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet= rescanblockchain '+get_blockheight(),shell=True,start_new_session=True)
    if request.method == 'POST':
        return redirect('/BCdisplayutxos')
    return render_template('BCrescan.html')

@app.route("/BCdisplayutxos", methods=['GET', 'POST'])
def BCdisplayutxos():
    global addresses
    global selectedutxo
    if request.method == 'GET':
        addresses = []
        totalwalletbal = 0
        rpc = RPC()
        response = rpc.listunspent()
        for x in range(0, len(response)):
            utxo = response[x]
            if utxo['spendable']:
                txid = utxo['txid']
                vout = utxo['vout']
                adr = utxo['address']
                scriptPubKey = utxo['scriptPubKey']
                numamount = utxo['amount']
                totalwalletbal = totalwalletbal + numamount
                amount = "{:.8f}".format(float(numamount))
                numamount = float(amount)
                confs = utxo['confirmations']
                totalbal = rpc.getreceivedbyaddress(adr)
                address = {}
                address['txid'] = txid
                address['vout'] = vout 
                address['scriptPubKey'] = scriptPubKey
                address['address'] = adr
                address['balance'] = amount
                address['numbal'] = numamount
                addresses.append(address)
        addresses.sort(key=lambda x: x['numbal'], reverse=True)
    if request.method == 'POST':
        for i in range(0, len(addresses)):
            if request.form['txid'] == addresses[i]['txid']:
                selectedutxo = addresses[i]
        return redirect('/BCscanrecipent')
    return render_template('BCdisplayutxos.html', addresses=addresses, len=len(addresses), TWB=totalwalletbal)

@app.route("/BCscanrecipent", methods=['GET', 'POST'])
def BCscanrecipent():
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
            error = receipentaddress + ' is not a valid bitcoin address, address should have started with bc1, 3 or 1 instead of ' + receipentaddress[:1] + ', or ' + secondqrcode[:3] + '.'
        if error:
            return redirect('/BCscanrecipent')
        return redirect('/BCconfirmsend')
    return render_template('BCscanrecipent.html', error=error)

@app.route("/BCconfirmsend", methods=['GET', 'POST'])
def BCconfirmsend():
    global receipentaddress
    if request.method == 'GET':
        rpc = RPC()
        amount = float(selectedutxo['numbal'])
        minerfee = float(rpc.estimatesmartfee(1)["feerate"])
        kilobytespertrans = 0.200
        amo = (amount - (minerfee * kilobytespertrans))
        minerfee = (minerfee * kilobytespertrans)
        amo = "{:.8f}".format(float(amo))
        minerfee = "{:.8f}".format(float(minerfee))
    if request.method == 'POST':
        return redirect('/BCdisplaytransaction')
    return render_template('BCconfirmsend.html', amount=amo, minerfee=minerfee, recipent=receipentaddress)

@app.route("/BCdisplaytransaction", methods=['GET', 'POST'])
def BCdisplaytransaction():
    global selectedutxo
    global receipentaddress
    if request.method == 'GET':
        rpc = RPC()
        amount = float(selectedutxo['numbal'])
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
        firstqrcode = json.loads(response[0].decode("utf-8"))['hex']
        rpc.sendrawtransaction(json.loads(response[0].decode("utf-8"))['hex'])
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
        path = url_for('static', filename='firsttransqrcode' + firstqrname + '.png')
    if request.method == 'POST':
        return redirect('/BCdisplayutxos')
    return render_template('BCdisplaytransaction.html', qrdata=firstqrcode, path=path)

@app.route("/BCscantransaction", methods=['GET', 'POST'])
def BCscantransaction():
    global signtransactionhex
    global totalamount
    if request.method == 'POST':
        response = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        transactionhex = response.decode("utf-8")
        print(transactionhex)
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet= sendrawtransaction '+transactionhex],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response)
        return redirect('/BCswitchlaptop')
    return render_template('BCscantransaction.html')

@app.route("/BCswitchlaptop", methods=['GET', 'POST'])
def BCswitchlaptop():
    if request.method == 'POST':
        return redirect('/BCscantransaction')
    return render_template('BCswitchlaptop.html')



if __name__ == "__main__":
    app.run()