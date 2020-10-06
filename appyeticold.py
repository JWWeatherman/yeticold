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
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD, step=5, switch=True)

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
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD, step=6)

#OFF
@app.route("/YCRconnection", methods=['GET', 'POST'])
def YCRconnection():
    if request.method == 'POST':
        subprocess.call(['python3 ~/yeticold/utils/forgetnetworks.py'],shell=True)
        subprocess.call(['nmcli n off'],shell=True)
        return redirect('/YCRswitchlaptop')
    return render_template('connection.html', step=7)

#OFF
@app.route("/YCRswitchlaptop", methods=['GET', 'POST'])
def YCRswitchlaptop():
    if request.method == 'POST':
        return redirect('/YCRscandescriptorB')
    return render_template('switchlaptop.html', step=8, instructions="")

#ON
@app.route("/YCRscandescriptor", methods=['GET', 'POST'])
def YCRscandescriptor():
    if request.method == 'POST':
        v.pubdesc = handleResponse('python3 ~/yeticold/utils/scanqrcode.py').replace('\n', '')
        return redirect('/YCRrescanwallet')
    return render_template('scandescriptor.html', step=9)

#ON
@app.route("/YCRrescanwallet", methods=['GET', 'POST'])
def YCRrescanwallet():
    handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwallet importmulti \'[{ "desc": "'+v.pubdesc+'", "timestamp": "now", "range": [0,999], "watchonly": false}]\' \'{"rescan": true}\'')
    handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwallet rescanblockchain '+blockheight())
    return redirect('/YCRdisplaywallet')
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
    return render_template('displayutxo.html', qrdata=v.sourceaddress, path=v.path, step=1)

#OFF
@app.route("/YCRscandescriptorB", methods=['GET', 'POST'])
def YCRscandescriptorB():
    if v.walletimported:
        return redirect('/YCRscanutxo')
    if request.method == 'POST':
        v.pubdesc = handleResponse('python3 ~/yeticold/utils/scanqrcode.py', True)
        v.privkeycount = 0
        return redirect('/YCRimportseeds')
    return render_template('scandescriptor.html', step=2)

#OFF
@app.route('/YCRimportseeds', methods=['GET', 'POST'])
def YCRimportseeds():
    route = importSeeds(request, '/YCRimportseeds', '/YCRscanutxo')
    if route:
        return route
    return render_template('importseeds.html', x=v.privkeycount + 1, error=v.error,i=v.privkeycount + 2, step=3+v.privkeycount)

#OFF
@app.route("/YCRscanutxo", methods=['GET', 'POST'])
def YCRscanutxo():
    step = 2 if walletimported else 6
    if request.method == 'POST':
        v.selectedutxo = handleResponse('python3 ~/yeticold/utils/scanqrcode.py', True)
        return redirect('/YCRscanrecipent')
    return render_template('scanutxo.html',step=step)

#OFF
@app.route("/YCRscanrecipent", methods=['GET', 'POST'])
def YCRscanrecipent():
    step = 3 if walletimported else 7
    route = scanrecipent(request, '/YCRscanrecipent', '/YCRsetFee')
    if route:
        return route
    return render_template('scanrecipent.html', error=v.error,step=step)

#OFF
@app.route('/YCRsetFee', methods=['GET', 'POST'])
def YCRsetFee():
    step = 4 if walletimported else 8
    route = setFee(request, '/YCRsetFee', '/YCRconfirmsend')
    if route:
        return route
    return render_template('setFee.html', amount=v.amount, minerfee=v.minerfee, amo=v.amo,step=step)

#OFF
@app.route("/YCRconfirmsend", methods=['GET', 'POST'])
def YCRconfirmsend():
    step = 5 if walletimported else 9
    if request.method == 'GET':
        createTransactions()
    if request.method == 'POST':
        return redirect('/YCRdisplaytransaction')
    return render_template('confirmsend.html', amount=v.amo, minerfee=v.minerfee, recipent=v.receipentaddress,step=step)

#OFF
@app.route("/YCRdisplaytransaction", methods=['GET', 'POST'])
def YCRdisplaytransaction():
    step = 6 if walletimported else 10
    if request.method == 'GET':
        step = 
        v.path = makeQrCode(v.transnum)
    if request.method == 'POST':
        walletimported = True
        return redirect('/YCRscanutxo')
    return render_template('displaytransaction.html', qrdata=v.transhex, path=v.path,step=step)

#ON
@app.route("/YCRscantransaction", methods=['GET', 'POST'])
def YCRscantransaction():
    step = 7 if walletimported else 11
    if request.method == 'POST':
        v.transactionhex = handleResponse('python3 ~/yeticold/utils/scanqrcode.py')
        response = handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwallet sendrawtransaction '+v.transactionhex)
        return redirect('/YCRdisplaywallet')
    return render_template('scantransaction.html', step=step)






#SETUP
#ON
@app.route("/YCblockchain", methods=['GET', 'POST'])
def YCblockchain():
    route = blockChain(request, '/YCopenbitcoin')
    if route:
        return route
    return render_template('blockchain.html')

#ON
@app.route("/YCopenbitcoin", methods=['GET', 'POST'])
def YCopenbitcoin():
    route = openBitcoin(request, '/YCopenbitcoin', '/YCscandescriptor')
    if route:
        return route
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD, step=1)

#OFF
@app.route("/YCblockchainB", methods=['GET', 'POST'])
def YCblockchainB():
    route = blockChain(request, '/YCopenbitcoinB')
    if route:
        return route
    return render_template('blockchain.html')

#OFF
@app.route("/YCopenbitcoinB", methods=['GET', 'POST'])
def YCopenbitcoinB():
    route = openBitcoin(request, '/YCopenbitcoinB', '/YCconnection')
    if route:
        return route
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD)

#OFF
@app.route("/YCconnection", methods=['GET', 'POST'])
def YCconnection():
    if request.method == 'POST':
        subprocess.call(['python3 ~/yeticold/utils/forgetnetworks.py'],shell=True)
        subprocess.call(['nmcli n off'],shell=True)
        return redirect('/YCgetseeds')
    return render_template('connection.html')

#OFF
@app.route("/YCgetseeds", methods=['GET', 'POST'])
def YCgetseeds():
    route = getSeeds(request, '/YCdisplaydescriptor')
    if route:
        return route
    return render_template('getseeds.html')

#OFF
@app.route("/YCdisplaydescriptor", methods=['GET', 'POST'])
def YCdisplaydescriptor():
    if request.method == 'GET':
        v.path = makeQrCode(v.pubdesc)
    if request.method == 'POST':
        return redirect('/YCdisplayseeds')
    return render_template('displaydescriptor.html', qrdata=v.pubdesc, path=v.path)

#ON
@app.route("/YCscandescriptor", methods=['GET', 'POST'])
def YCscandescriptor():
    if request.method == 'POST':
        v.pubdesc = handleResponse('python3 ~/yeticold/utils/scanqrcode.py').replace('\n', '')
        handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwallet importmulti \'[{ "desc": "'+v.pubdesc+'", "timestamp": "now", "range": [0,999], "watchonly": false}]\' \'{"rescan": true}\'')
        return redirect('/YCprintpage')
    return render_template('scandescriptor.html')

#ON
@app.route("/YCprintpage", methods=['GET', 'POST'])
def YCprintpage():
    if request.method == 'GET':
        v.path = makeQrCode(v.pubdesc)
    if request.method == 'POST':
        return redirect('/YCswitchlaptop')
    return render_template('printpage.html', qrdata=v.pubdesc, path=v.path)

#ON
@app.route("/YCswitchlaptop", methods=['GET', 'POST'])
def YCswitchlaptop():
    if request.method == 'POST':
        return redirect('/YCRdisplaywallet')
    return render_template('switchlaptop.html')

#SWITCH TO OFFLINE

#OFF
@app.route('/YCdisplayseeds', methods=['GET', 'POST'])
def YCdisplayseeds():
    route = displaySeeds(request, '/YCdisplayseeds', '/YCcheckseeds')
    if route:
        return route
    return render_template('displayseeds.html', PPL=v.passphraselist, x=v.privkeycount + 1, i=v.privkeycount + 9)

#OFF
@app.route('/YCcheckseeds', methods=['GET', 'POST'])
def YCcheckseeds():
    route = checkSeeds(request, '/YCcheckseeds', '/YCcopyseeds')
    if route:
        return route
    return render_template('checkseeds.html', x=v.privkeycount + 1, error=v.error,i=v.privkeycount + 16,oldkeys=v.oldkeys)

#OFF
@app.route("/YCcopyseeds", methods=['GET', 'POST'])
def YCcopyseeds():
    if request.method == 'POST':
        return redirect('/YCswitchlaptopB')
    return render_template('copyseeds.html')

#OFF
@app.route("/YCswitchlaptopB", methods=['GET', 'POST'])
def YCswitchlaptopB():
    if request.method == 'POST':
        return redirect('/YCRscanutxo')
    return render_template('switchlaptop.html')

if __name__ == "__main__":
    app.run()

