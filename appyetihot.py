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

#VARIABLES 
home = os.getenv("HOME")
privkeylist = []
xprivlist = []
error = None
qrdata = None
privkeycount = 0
receipentaddress = None
qrcodescanning = None
pubdesc = None
progress = 0
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
    wallet_name = 'yetihot'
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
#FLOW ONE
#YHblockchain 
#YHopenbitcoin - step 6
#YHmenu - step 7
#CHOOSE CREATE NEW
#YHgetseed - step 8
#YHdisplayseed - step 9
#YHcheckseed - step 10
#YHcopyseed - step 11
#YHwalletinstruction - step 12
#FLOW TWO 
#YHblockchain
#YHopenbitcoin - step 6
#YHmenu - step 7
#CHOOSE RESTORE WALLET
#YHRinputseed - step 8
#YHRwalletinstructions - step 9

#ROUTS
@app.route("/", methods=['GET', 'POST'])
def redirectroute():
    if request.method == 'GET':
        return redirect('/YHblockchain')
    return render_template('redirect.html')

@app.route("/YHblockchain", methods=['GET', 'POST'])
def YHblockchain():
    global blockchain
    global testblockchain
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
            return redirect('/YHopenbitcoin')
    if request.method == 'POST':
        if request.form['option'] == 'downloadblockchain':
            testblockchain = True
            subprocess.Popen('python3 ~/yeticold/utils/testblockchain.py',shell=True,start_new_session=True)
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
        return redirect('/YHopenbitcoin')
    ###ISSUE template needed
    return render_template('YHblockchain.html')

@app.route("/YHopenbitcoin", methods=['GET', 'POST'])
def YHopenbitcoin():
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
            return redirect('/YHmenu')
        else:
            return redirect('/YHopenbitcoin')
    return render_template('YHopenbitcoin.html', progress=progress, IBD=IBD)

@app.route("/YHmenu", methods=['GET', 'POST'])
def YHmenu():
    if request.method == 'POST':
        if request.form['option'] == 'recovery':
            return redirect('/YHRinputseed')
        else:
            return redirect('/YHgetseed')
    return render_template('YHmenu.html')

#randomise priv key and get xprivs
@app.route("/YHgetseed", methods=['GET', 'POST'])
def YHgetseed():
    global privkey
    global xpriv
    global pubdesc
    if request.method == 'POST':
        if request.form['skip'] == 'skip':
            newbinary = '1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
        else:
            newbinary = request.form['binary']
        rpc = RPC()
        adr = rpc.getnewaddress()
        newprivkey = rpc.dumpprivkey(adr)
        binary = bin(decode58(newprivkey))[2:][8:-40]
        privkey = ConvertToWIF(xor(binary,newbinary))
        home = os.getenv('HOME')
        path = home + '/yetihotwallet'
        subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetihot"','~/yeticold/bitcoin/bin/bitcoin-cli loadwallet "yetihot"'],shell=True)
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetihot sethdseed true "'+privkey+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return redirect('/YHdisplayseed')
    return render_template('YHgetseed.html')
#display seeds
@app.route('/YHdisplayseed', methods=['GET', 'POST'])
def YHdisplayseed():
    global privkey
    global privkeycount
    if request.method == 'GET':
        passphraselist = ConvertToPassphrase(privkey)
    if request.method == 'POST':
        home = os.getenv('HOME')
        path = home + '/Documents'
        subprocess.call('rm '+path+'/yhseed.txt', shell=True)
        subprocess.call('touch '+path+'/yhseed.txt', shell=True)
        file = ''
        for i in range(0,13):
            file = file + request.form['displayrow' + str(i+1)] + '\n'
        subprocess.call('echo "'+file+'" >> '+path+'/yhseed.txt', shell=True)
        return redirect('/YHcheckseed')
    return render_template('YHdisplayseed.html', PPL=passphraselist)
#confirm privkey
@app.route('/YHcheckseed', methods=['GET', 'POST'])
def YHcheckseed():
    global privkey
    global xpriv
    global error
    if request.method == 'POST':
        passphraselist = ConvertToPassphrase(privkey)
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
            return redirect('/YHcopyseed')
        else:
            error = 'You enterd the private key incorrectly but the checksums are correct please try agian. This means you probably inputed a valid seed, but not your seed.'
    return render_template('YHcheckseed.html', x=privkeycount + 1, error=error,i=privkeycount + 35 )
#store USB drives
@app.route("/YHcopyseed", methods=['GET', 'POST'])
def YHcopyseed():
    if request.method == 'POST':
        return redirect('/YHwalletinstructions')
    return render_template('YHcopyseed.html')

@app.route('/YHwalletinstructions', methods=['GET', 'POST'])
def YHwalletinstructions():
    global qrdata
    global error
    if request.method == 'POST':
        error = None
        qrdata = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        qrdata = qrdata.decode("utf-8").replace('\n', '')
        if (qrdata.split(':')[0] == 'bitcoin'):
            qrdata = qrdata.split(':')[1].split('?')[0]
        if (qrdata[:3] == 'bc1') or (qrdata[:1] == '3') or (qrdata[:1] == '1'):
            if not (len(qrdata) >= 26) and (len(qrdata) <= 35):
                error = qrdata + ' is not a valid bitcoin address, address should have a length from 26 to 35 instead of ' + str(len(qrdata)) + '.'
        else: 
            error = qrdata + ' is not a valid bitcoin address, address should have started with bc1, 3 or 1 instead of ' + qrdata[:1] + ', or ' + qrdata[:3] + '.'
        if error:
            qrdata = None
        return redirect('/YHwalletinstructions')
    return render_template('YHwalletinstructions.html', error=error, qrdata=qrdata)
#STOP SET UP-----------------------------------------------------------------------------------------------------------------------------------------------------
    
@app.route('/YHRinputseed', methods=['GET', 'POST'])
def YHRinputseed():
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
        privkey = PassphraseListToWIF(privkey)
        error = None
        rpc = RPC()
        subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetihot" false true'],shell=True)
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetihot sethdseed true "'+privkey+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return redirect('/YHRwalletinstructions')
    return render_template('YHRinputseed.html', error=error)

@app.route('/YHRwalletinstructions', methods=['GET', 'POST'])
def YHRwalletinstructions():
    global qrdata
    global error
    global qrcodescanning
    if request.method == 'GET':
        if not qrcodescanning:
            qrcodescanning = False
            subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetihot rescanblockchain '+blockheight(),shell=True,start_new_session=True)
    if request.method == 'POST':
        error = None
        qrdata = subprocess.Popen(['python3 ~/yeticold/utils/scanqrcode.py'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        qrdata = qrdata.decode("utf-8").replace('\n', '')
        if (qrdata.split(':')[0] == 'bitcoin'):
            qrdata = qrdata.split(':')[1].split('?')[0]
        if (qrdata[:3] == 'bc1') or (qrdata[:1] == '3') or (qrdata[:1] == '1'):
            if not (len(qrdata) >= 26) and (len(qrdata) <= 35):
                error = qrdata + ' is not a valid bitcoin address, address should have a length from 26 to 35 instead of ' + str(len(qrdata)) + '.'
        else: 
            error = qrdata + ' is not a valid bitcoin address, address should have started with bc1, 3 or 1 instead of ' + qrdata[:1] + ', or ' + qrdata[:3] + '.'
        if error:
            qrdata = None
        qrcodescanning = True
        return redirect('/YHRwalletinstructions')
    return render_template('YHRwalletinstructions.html', error=error, qrdata=qrdata)

if __name__ == "__main__":
    app.run()
