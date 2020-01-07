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

settings = {"rpc_username": "rpcuser","rpc_password": rpcpsw,"rpc_host": "127.0.0.1","rpc_port": 8332,"address_chunk": 100}
wallet_template = "http://{rpc_username}:{rpc_password}@{rpc_host}:{rpc_port}/wallet/{wallet_name}"
progress = 0
parsedutxos = []
selectedutxo = {}
error = ""
receipentaddress = ""
signtransactionhex = ""
totalamount = ""

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
    wallet_name = ''
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

#BCblockchain - step X - #download crap bitcoin directory?
#Open bitcoin - step 6 - Open bitcoin - Online
#Setup Disconnected - step 9 - Online # go to off.yeticold.com
#Open bitcoin - auto redirect - Disconnected
#Import keys - step 10 - Disconnected //Have user manuly import keys to default wallet
#Display utxos - WP - Disconnected //Make sure utxos are spendable before displaying
#Scan recipent - step 1 - Disconnected 
#Confirm send transaction - step 2 - Online //Create the transaction if user confirms data
#Display signed transaction - step 3 - Disconnected # On your Online showing step (9 or 5) click next to display step 4
#Scan sign transaction - step 4 - Online
#Sent page - step 5 - Online # On your Disconnected currently showing step 3 click next to display your wallet page

@app.route("/", methods=['GET', 'POST'])
def redirectroute():
    return redirect('/BCopenbitcoin')

@app.route("/BCopenbitcoin", methods=['GET', 'POST'])
def BCopenbitcoin():
    global progress
    if request.method == 'GET':
        home = os.getenv("HOME")
        if BTCClosed():
            subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        progress = BTCprogress()
    if request.method == 'POST':
        if progress >= 99.9:
            return redirect('/BConlinestartup')
        else:
            return redirect('/BCopenbitcoin')
    return render_template('BCopenbitcoin.html', progress=progress)

@app.route("/BConlinestartup", methods=['GET', 'POST'])
def BConlinestartup():
    if request.method == 'POST':
        return redirect('/BCscantransaction')
    return render_template('BConlinestartup.html')

@app.route("/BCblockchain", methods=['GET', 'POST'])
def BCblockchain():
    global rpcpsw
    global blockchain
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
            return redirect('/BCopenbitcoin')
        subprocess.call(['nmcli n on'],shell=True)
        time.sleep(5)
    if request.method == 'POST':
        if request.form['option'] == 'downloadblockchain':
            subprocess.call(['sshpass -p "download" scp -r download@199.192.30.178:.bitcoin ~/.bitcoin'],shell=True)
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
        return redirect('/BCopenbitcoinC')
    return render_template('BCblockchain.html')

@app.route("/BCopenbitcoinC", methods=['GET', 'POST'])
def BCopenbitcoinC():
    if request.method == 'GET':
        if BTCClosed():
            subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
    if request.method == 'POST':
        IBD = BTCRunning()
        if IBD:
            subprocess.call(['nmcli n off'],shell=True)
            return redirect('/BCimportkeys')
        else:
            return redirect('/BCopenbitcoinC')
    return render_template('BCopenbitcoinC.html', progress=progress)

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
            response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet= rescanblockchain '+blockheight()],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return redirect('/BCrescan')
    return render_template('BCimportkeys.html')

@app.route("/BCrescan", methods=['GET', 'POST'])
def BCrescan():
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
        utxos = rpc.listunspent()
        for x in range(0, len(response)):
            utxo = response[x]
            if utxo['spendable']:
                txid = utxo['txid']
                vout = utxo['vout']
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
        addresses.sort(key=lambda x: x['amount'], reverse=True)
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
        amount = float(selectedutxo['amount'])
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
        return redirect('/BCswitchlaptop')
    return render_template('BCscantransaction.html')

@app.route("/BCswitchlaptop", methods=['GET', 'POST'])
def BCswitchlaptop():
    if request.method == 'POST':
        return redirect('/BCscantransaction')
    return render_template('BCswitchlaptop.html')



if __name__ == "__main__":
    app.run()