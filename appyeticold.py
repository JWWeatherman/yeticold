import os
import sys
home = os.getenv("HOME")
sys.path.append(home + '/yeticold/utils/')
from imports import *
import variables as v
v.rpcpsw = str(random.randrange(0,1000000))
v.settings = {"rpc_username": "rpcuser","rpc_password": v.rpcpsw, "rpc_host": "127.0.0.1","rpc_port": 8332,"address_chunk": 100}
v.wallet_template = "http://{rpc_username}:{rpc_password}@{rpc_host}:{rpc_port}/wallet/{wallet_name}"
from formating import *
from btcrpcfunctions import blockheight
from yetifunctions import *
from yetiroutefunctions import * 
app = Flask(__name__)

#ROUTES


#A
@app.route("/", methods=['GET', 'POST'])
def redirectroute():
    return redirect('/YCmenu')

#ON
@app.route("/YCmenu", methods=['GET', 'POST'])
def YCmenu():
    if request.method == 'POST':
        if request.form['option'] == 'recovery':
            return redirect('/YCRblockchain')
        else:
            return redirect('/YCblockchain')
    return render_template('menu.html')

#ON
@app.route("/YCRblockchain", methods=['GET', 'POST'])
def YCRblockchain():
    route = blockChain(request, '/YCRopenbitcoin')
    if route:
        return route
    return render_template('blockchain.html')

#ON
@app.route("/YCRopenbitcoin", methods=['GET', 'POST'])
def YCRopenbitcoin():
    route = openBitcoin(request, '/YCRopenbitcoin', '/YCRscandescriptor')
    if route:
        return route
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD)

#ON
@app.route("/YCRscandescriptor", methods=['GET', 'POST'])
def YCRscandescriptor():
    if request.method == 'POST':
        v.pubdesc = handleResponse('python3 ~/yeticold/utils/scanqrcode.py').replace('\n', '')
        return redirect('/YCRrescanwallet')
    return render_template('scandescriptor.html')

#ON
@app.route("/YCRrescanwallet", methods=['GET', 'POST'])
def YCRrescanwallet():
    if request.method == 'GET':
        handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwallet importmulti \'[{ "desc": "'+v.pubdesc+'", "timestamp": "now", "range": [0,999], "watchonly": false}]\' \'{"rescan": true}\'')
        handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwallet rescanblockchain '+blockheight())
        return redirect('/YCRdisplaywallet')
    return render_template('rescanwallet.html')

#ON
@app.route("/YCRdisplaywallet", methods=['GET', 'POST'])
def YCRdisplaywallet():
    route = displaywallet(request, '/YCRdisplayutxo')
    if route:
        return route
    return render_template('displaywallet.html', addresses=v.addresses, len=len(v.addresses), TWB=v.totalwalletbal)

#ON
@app.route("/YCRdisplayutxo", methods=['GET', 'POST'])
def YCRdisplayutxo():
    if request.method == 'GET':
        v.path = makeQrCode(str(v.sourceaddress))
    if request.method == 'POST':
        return redirect('/YCRscantransaction')
    return render_template('displayutxo.html', qrdata=v.sourceaddress, path=v.path)

#ON
@app.route("/YCRscantransaction", methods=['GET', 'POST'])
def YCRscantransaction():
    if request.method == 'POST':
        v.transactionhex = handleResponse('python3 ~/yeticold/utils/scanqrcode.py')
        print(v.transactionhex)
        response = handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwallet sendrawtransaction '+v.transactionhex)
        return redirect('/YCRdisplaywallet')
    return render_template('scantransaction.html')


#OFF
@app.route("/YCRblockchainB", methods=['GET', 'POST'])
def YCRblockchainB():
    route = blockChain(request, '/YCRopenbitcoinB')
    if route:
        return route
    return render_template('blockchain.html')

#OFF
@app.route("/YCRopenbitcoinB", methods=['GET', 'POST'])
def YCRopenbitcoinB():
    route = openBitcoin(request, '/YCRopenbitcoinB', '/YCRconnection')
    if route:
        return route
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD)

#OFF
@app.route("/YCRconnection", methods=['GET', 'POST'])
def YCRconnection():
    if request.method == 'POST':
        subprocess.call(['python3 ~/yeticold/utils/forgetnetworks.py'],shell=True)
        subprocess.call(['nmcli n off'],shell=True)
        return redirect('/YCRswitchlaptop')
    return render_template('connection.html')

#OFF
@app.route("/YCRswitchlaptop", methods=['GET', 'POST'])
def YCRswitchlaptop():
    if request.method == 'POST':
        return redirect('/YCRscandescriptorB')
    return render_template('switchlaptop.html')

#OFF
@app.route("/YCRscandescriptorB", methods=['GET', 'POST'])
def YCRscandescriptorB():
    if request.method == 'POST':
        v.pubdesc = handleResponse('python3 ~/yeticold/utils/scanqrcode.py', True)
        return redirect('/YCRimportseeds')
    return render_template('scandescriptor.html')

#OFF
@app.route('/YCRimportseeds', methods=['GET', 'POST'])
def YCRimportseeds():
    route = importSeeds(request, '/YCRimportseeds', '/YCRscanutxo')
    if route:
        return route
    return render_template('importseeds.html', x=v.privkeycount + 1, error=v.error,i=v.privkeycount + 2)

#OFF
@app.route("/YCRscanutxo", methods=['GET', 'POST'])
def YCRscanutxo():
    if request.method == 'POST':
        v.selectedutxo = handleResponse('python3 ~/yeticold/utils/scanqrcode.py', True)
        return redirect('/YCRscanrecipent')
    return render_template('scanutxo.html')

#OFF
@app.route("/YCRscanrecipent", methods=['GET', 'POST'])
def YCRscanrecipent():
    route = scanrecipent(request, '/YCRscanrecipent', '/YCRsetFee')
    if route:
        return route
    return render_template('scanrecipent.html', error=v.error)

#OFF
@app.route('/YCRsetFee', methods=['GET', 'POST'])
def YCRsetFee():
    route = setFee(request, '/YCRsetFee', '/YCRconfirmsend')
    if route:
        return route
    return render_template('setFee.html', amount=v.amount, minerfee=v.minerfee, amo=v.amo)

#OFF
@app.route("/YCRconfirmsend", methods=['GET', 'POST'])
def YCRconfirmsend():
    if request.method == 'GET':
        createTransactions()
    if request.method == 'POST':
        return redirect('/YCRdisplaytransaction')
    return render_template('confirmsend.html', amount=v.amo, minerfee=v.minerfee, recipent=v.receipentaddress)

#OFF
@app.route("/YCRdisplaytransaction", methods=['GET', 'POST'])
def YCRdisplaytransaction():
    if request.method == 'GET':
        v.path = makeQrCode(v.transnum)
    if request.method == 'POST':
        return redirect('/YCRscanutxo')
    return render_template('displaytransaction.html', qrdata=v.transhex, path=v.path)

#SETUP
@app.route("/YCblockchain", methods=['GET', 'POST'])
def YCblockchain():
    route = blockChain(request, '/YCopenbitcoin')
    if route:
        return route
    return render_template('blockchain.html')

@app.route("/YCopenbitcoin", methods=['GET', 'POST'])
def YCopenbitcoin():
    route = openBitcoin(request, '/YCopenbitcoin', '/YCscandescriptor')
    if route:
        return route
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD)

@app.route("/YCscandescriptor", methods=['GET', 'POST'])
def YCscandescriptor():
    if request.method == 'POST':
        v.pubdesc = handleResponse('python3 ~/yeticold/utils/scanqrcode.py').replace('\n', '')
        handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwallet importmulti \'[{ "desc": "'+v.pubdesc+'", "timestamp": "now", "range": [0,999], "watchonly": false}]\' \'{"rescan": true}\'')
        return redirect('/YCprintpage')
    return render_template('scandescriptor.html')

@app.route("/YCprintpage", methods=['GET', 'POST'])
def YCprintpage():
    if request.method == 'GET':
        v.path = makeQrCode(v.pubdesc)
    if request.method == 'POST':
        return redirect('/YCswitchlaptop')
    return render_template('printpage.html', qrdata=v.pubdesc, path=v.path)

@app.route("/YCswitchlaptop", methods=['GET', 'POST'])
def YCswitchlaptop():
    if request.method == 'POST':
        return redirect('/YCRdisplaywallet')
    return render_template('switchlaptop.html')

#SWITCH TO OFFLINE
@app.route("/YCblockchainB", methods=['GET', 'POST'])
def YCblockchainB():
    route = blockChain(request, '/YCopenbitcoinB')
    if route:
        return route
    return render_template('blockchain.html')

@app.route("/YCopenbitcoinB", methods=['GET', 'POST'])
def YCopenbitcoinB():
    route = openBitcoin(request, '/YCopenbitcoinB', '/YCconnection')
    if route:
        return route
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD)

@app.route("/YCconnection", methods=['GET', 'POST'])
def YCconnection():
    if request.method == 'POST':
        subprocess.call(['python3 ~/yeticold/utils/forgetnetworks.py'],shell=True)
        subprocess.call(['nmcli n off'],shell=True)
        return redirect('/YCgetseeds')
    return render_template('connection.html')

@app.route("/YCgetseeds", methods=['GET', 'POST'])
def YCgetseeds():
    route = getSeeds(request, '/YCdisplaydescriptor')
    if route:
        return route
    return render_template('getseeds.html')

@app.route("/YCdisplaydescriptor", methods=['GET', 'POST'])
def YCdisplaydescriptor():
    if request.method == 'GET':
        v.path = makeQrCode(v.pubdesc)
    if request.method == 'POST':
        return redirect('/YCdisplayseeds')
    return render_template('displaydescriptor.html', qrdata=v.pubdesc, path=v.path)

@app.route('/YCdisplayseeds', methods=['GET', 'POST'])
def YCdisplayseeds():
    route = displaySeeds(request, '/YCdisplayseeds', '/YCcheckseeds')
    if route:
        return route
    return render_template('displayseeds.html', PPL=v.passphraselist, x=v.privkeycount + 1, i=v.privkeycount + 9)

@app.route('/YCcheckseeds', methods=['GET', 'POST'])
def YCcheckseeds():
    route = checkSeeds(request, '/YCcheckseeds', '/YCcopyseeds')
    if route:
        return route
    return render_template('checkseeds.html', x=v.privkeycount + 1, error=v.error,i=v.privkeycount + 16,oldkeys=v.oldkeys)

@app.route("/YCcopyseeds", methods=['GET', 'POST'])
def YCcopyseeds():
    if request.method == 'POST':
        return redirect('/YCswitchlaptopB')
    return render_template('copyseeds.html')

@app.route("/YCswitchlaptopB", methods=['GET', 'POST'])
def YCswitchlaptopB():
    if request.method == 'POST':
        return redirect('/YCRscanutxo')
    return render_template('switchlaptop.html')

if __name__ == "__main__":
    app.run()

