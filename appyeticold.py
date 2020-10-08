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
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD, step=5, switch=True, url="rec.yeticold.com")

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
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD, step=7)

#OFF
@app.route("/YCRconnection", methods=['GET', 'POST'])
def YCRconnection():
    if request.method == 'POST':
        subprocess.call(['python3 ~/yeticold/utils/forgetnetworks.py'],shell=True)
        subprocess.call(['nmcli n off'],shell=True)
        return redirect('/YCRswitchlaptop')
    return render_template('connection.html', step=8)

#OFF
@app.route("/YCRswitchlaptop", methods=['GET', 'POST'])
def YCRswitchlaptop():
    if request.method == 'POST':
        return redirect('/YCRscandescriptorB')
    return render_template('switchlaptop.html', step=9, instructions="Switch to your Primary laptop currently Showing step 5. Click next to show step 10.", laptop="Primary")

#ON
@app.route("/YCRscandescriptor", methods=['GET', 'POST'])
def YCRscandescriptor():
    if request.method == 'POST':
        v.pubdesc = handleResponse('python3 ~/yeticold/utils/scanqrcode.py').replace('\n', '')
        return redirect('/YCRrescanwallet')
    return render_template('scandescriptor.html', step=10)

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
    oldstep = "6, 10" if v.walletimported else "9"
    if request.method == 'GET':
        v.path = makeQrCode(str(v.selectedutxo))
    if request.method == 'POST':
        return redirect('/YCRscantransaction')
    return render_template('displayutxo.html', qrdata=v.selectedutxo, path=v.path, step=1, instructions="Switch to your Secondary laptop currently showing step "+oldstep+". Click next to show step 2", laptop="Secondary")

#OFF
@app.route("/YCRscandescriptorB", methods=['GET', 'POST'])
def YCRscandescriptorB():
    if v.walletimported:
        return redirect('/YCRscanutxo')
    if request.method == 'POST':
        v.pubdesc = handleResponse('python3 ~/yeticold/utils/scanqrcode.py').replace('\n', '')
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
    step = 2 if v.walletimported else 6
    if request.method == 'POST':
        v.selectedutxo = handleResponse('python3 ~/yeticold/utils/scanqrcode.py')
        v.selectedutxo = eval(v.selectedutxo)
        return redirect('/YCRscanrecipent')
    return render_template('scanutxo.html',step=step)

#OFF
@app.route("/YCRscanrecipent", methods=['GET', 'POST'])
def YCRscanrecipent():
    step = 3 if v.walletimported else 7
    route = scanrecipent(request, '/YCRscanrecipent', '/YCRsetFee')
    if route:
        return route
    return render_template('scanrecipent.html', error=v.error,receipentaddress=v.receipentaddress,step=step)

#OFF
@app.route('/YCRsetFee', methods=['GET', 'POST'])
def YCRsetFee():
    step = 4 if v.walletimported else 8
    route = setFee(request, '/YCRsetFee', '/YCRconfirmsend')
    if route:
        return route
    return render_template('setFee.html', amount=v.amount, minerfee=v.minerfee, amo=v.amo,step=step)

#OFF
@app.route("/YCRconfirmsend", methods=['GET', 'POST'])
def YCRconfirmsend():
    step = 5 if v.walletimported else 9
    if request.method == 'GET':
        createTransactions()
    if request.method == 'POST':
        return redirect('/YCRdisplaytransaction')
    return render_template('confirmsend.html', amount=v.amo, minerfee=v.minerfee, recipent=v.receipentaddress,step=step)

#OFF
@app.route("/YCRdisplaytransaction", methods=['GET', 'POST'])
def YCRdisplaytransaction():
    step = 6 if v.walletimported else 10
    if request.method == 'GET':
        v.path = makeQrCode(v.transnum)
    if request.method == 'POST':
        walletimported = True
        return redirect('/YCRscanutxo')
    return render_template('displaytransaction.html', qrdata=v.transnum, path=v.path,step=step, instructions="Switch to your Primary laptop currently showing step 1, Click next to show step "+str(step+1), laptop="Primary")

#ON
@app.route("/YCRscantransaction", methods=['GET', 'POST'])
def YCRscantransaction():
    step = 7 if v.walletimported else 11
    if request.method == 'POST':
        v.transnum = handleResponse('python3 ~/yeticold/utils/scanqrcode.py')
        response = handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwallet sendrawtransaction '+v.transnum)
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
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD, step=5, switch=True, url="desc.yeticold.com")

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
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD, step=7)

#OFF
@app.route("/YCconnection", methods=['GET', 'POST'])
def YCconnection():
    if request.method == 'POST':
        subprocess.call(['python3 ~/yeticold/utils/forgetnetworks.py'],shell=True)
        subprocess.call(['nmcli n off'],shell=True)
        return redirect('/YCgetseeds')
    return render_template('connection.html', step=8)

#OFF
@app.route("/YCgetseeds", methods=['GET', 'POST'])
def YCgetseeds():
    route = getSeeds(request, '/YCdisplaydescriptor')
    v.walletimported = True
    if route:
        return route
    return render_template('getseeds.html', step=9)

#OFF
@app.route("/YCdisplaydescriptor", methods=['GET', 'POST'])
def YCdisplaydescriptor():
    if request.method == 'GET':
        v.path = makeQrCode(v.pubdesc)
    if request.method == 'POST':
        return redirect('/YCdisplayseeds')
    return render_template('displaydescriptor.html', qrdata=v.pubdesc, path=v.path, step=10, instructions="Switch to your Primary laptop currently showing step 5, click next to show step 11", laptop="Primary")

#ON
@app.route("/YCscandescriptor", methods=['GET', 'POST'])
def YCscandescriptor():
    if request.method == 'POST':
        v.pubdesc = handleResponse('python3 ~/yeticold/utils/scanqrcode.py').replace('\n', '')
        handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwallet importmulti \'[{ "desc": "'+v.pubdesc+'", "timestamp": "now", "range": [0,999], "watchonly": false}]\' \'{"rescan": true}\'')
        return redirect('/YCprintpage')
    return render_template('scandescriptor.html', step=11, setup=True)

#ON
@app.route("/YCprintpage", methods=['GET', 'POST'])
def YCprintpage():
    if request.method == 'GET':
        v.path = makeQrCode(v.pubdesc)
    if request.method == 'POST':
        return redirect('/YCswitchlaptop')
    return render_template('printpage.html', qrdata=v.pubdesc, path=v.path, step=12)

#ON
@app.route("/YCswitchlaptop", methods=['GET', 'POST'])
def YCswitchlaptop():
    if request.method == 'POST':
        return redirect('/YCRdisplaywallet')
    return render_template('switchlaptop.html', step=13, instructions="Switch to your Secondary laptop currently showing step 10, click next to show step 14", laptop="Secondary")

#OFF
@app.route('/YCdisplayseeds', methods=['GET', 'POST'])
def YCdisplayseeds():
    route = displaySeeds(request, '/YCdisplayseeds', '/YCcheckseeds')
    if route:
        return route
    return render_template('displayseeds.html', PPL=v.passphraselist, x=v.privkeycount + 1, step=14+v.privkeycount)

#OFF
@app.route('/YCcheckseeds', methods=['GET', 'POST'])
def YCcheckseeds():
    route = checkSeeds(request, '/YCcheckseeds', '/YCcopyseeds')
    if route:
        return route
    return render_template('checkseeds.html', x=v.privkeycount + 1, error=v.error,step=21+v.privkeycount,oldkeys=v.oldkeys)

#OFF
@app.route("/YCcopyseeds", methods=['GET', 'POST'])
def YCcopyseeds():
    if request.method == 'POST':
        return redirect('/YCswitchlaptopB')
    return render_template('copyseeds.html', step=28)

#OFF
@app.route("/YCswitchlaptopB", methods=['GET', 'POST'])
def YCswitchlaptopB():
    if request.method == 'POST':
        return redirect('/YCRscanutxo')
    return render_template('switchlaptop.html', step=29, instructions="Switch to your Primary laptop currently showing step 13, click next to show step your wallet.", laptop="Primary")

if __name__ == "__main__":
    app.run()

