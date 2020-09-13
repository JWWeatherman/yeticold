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


@app.errorhandler(werkzeug.exceptions.InternalServerError)
def handle_bad_request(e):
    if e.original_exception != None:
        e = e.original_exception
    return render_template('error.html', error=e), 500

@app.route("/", methods=['GET', 'POST'])
def redirectroute():
    if request.method == 'GET':
        return redirect('/YWblockchain')
    return render_template('redirect.html', yeti='warm')

@app.route("/YWblockchain", methods=['GET', 'POST'])
def YWblockchain():
    route = blockChain(request, '/YWopenbitcoin')
    if route:
        return route
    return render_template('blockchain.html', yeti='warm')

@app.route("/YWopenbitcoin", methods=['GET', 'POST'])
def YWopenbitcoin():
    route = openBitcoin(request, '/YWopenbitcoin', '/YWmenu')
    if route:
        return route
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD, yeti='warm')


@app.route("/YWmenu", methods=['GET', 'POST'])
def YWmenu():
    if request.method == 'POST':
        if request.form['option'] == 'recovery':
            return redirect('/YWRscandescriptor')
        else:
            return redirect('/YWgetseeds')
    return render_template('menu.html', yeti='warm')

@app.route("/YWgetseeds", methods=['GET', 'POST'])
def YWgetseeds():
    route = getSeeds(request, '/YWprintdescriptor')
    if route:
        return route
    return render_template('getseeds.html', yeti='warm')

@app.route("/YWprintdescriptor", methods=['GET', 'POST'])
def YWprintdescriptor():
    if request.method == 'GET':
        path = makeQrCode(v.pubdesc)
    if request.method == 'POST':
        return redirect('/YWdisplayseeds')
    return render_template('printdescriptor.html', qrdata=v.pubdesc, path=path, yeti='warm')

@app.route('/YWdisplayseeds', methods=['GET', 'POST'])
def YWdisplayseeds():
    route = displaySeeds(request, '/YWdisplayseeds', '/YWcheckseeds')
    if route:
        return route
    return render_template('displayseeds.html', PPL=v.passphraselist, x=v.privkeycount + 1, i=v.privkeycount + 9, yeti='warm')

@app.route('/YWcheckseeds', methods=['GET', 'POST'])
def YWcheckseeds():
    route = checkSeeds(request, '/YWcheckseeds', '/YWcopyseeds')
    if route:
        return route
    return render_template('checkseeds.html', x=v.privkeycount + 1, error=v.error,i=v.privkeycount + 16,oldkeys=v.oldkeys, yeti='warm')

@app.route("/YWcopyseeds", methods=['GET', 'POST'])
def YWcopyseeds():
    if request.method == 'POST':
        return redirect('/YWRdisplaywallet')
    return render_template('copyseeds.html', yeti='warm')

@app.route("/YWRscandescriptor", methods=['GET', 'POST'])
def YWRscandescriptor():
    if request.method == 'POST':
        v.pubdesc = handleResponse('python3 ~/yeticold/utils/scanqrcode.py').replace('\n', '')
        return redirect('/YWRrescanwallet')
    return render_template('scandescriptor.html', pubdesc=v.pubdesc, yeti='warm')

@app.route("/YWRrescanwallet", methods=['GET', 'POST'])
def YWRrescanwallet():
    if request.method == 'GET':
        handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwallet importmulti \'[{ "desc": "'+v.pubdesc+'", "timestamp": "now", "range": [0,999], "watchonly": false}]\' \'{"rescan": true}\'')
        handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwallet rescanblockchain '+blockheight())
        return redirect('/YWRdisplaywallet')
    return render_template('rescanwallet.html', yeti='warm')

@app.route("/YWRdisplaywallet", methods=['GET', 'POST'])
def YWRdisplaywallet():
    route = displaywallet(request, '/YWRscanrecipent')
    if route:
        return route
    return render_template('displaywallet.html', addresses=v.addresses, len=len(v.addresses), TWB=v.totalwalletbal, yeti='warm')

@app.route("/YWRscanrecipent", methods=['GET', 'POST'])
def YWRscanrecipent():
    route = scanrecipent(request, '/YWRscanrecipent', '/YWRimportseeds')
    if route:
        return route
    return render_template('scanrecipent.html', error=v.error, recipent=v.receipentaddress, yeti='warm')

@app.route('/YWRimportseeds', methods=['GET', 'POST'])
def YWRimportseeds():    
    route = importSeeds(request, '/YWRimportseeds', '/YWRsetFee')
    if route:
        return route
    return render_template('importseeds.html', x=v.privkeycount + 1, error=v.error,i=v.privkeycount + 2, yeti='warm')

@app.route('/YWRsetFee', methods=['GET', 'POST'])
def YWRsetFee():
    route = setFee(request, '/YWRsetFee', '/YWRsendtransaction')
    if route:
        return route
    return render_template('setFee.html', amount=v.amount, minerfee=v.minerfee, amo=v.amo, yeti='warm')

#GEN trans qr code
@app.route("/YWRsendtransaction", methods=['GET', 'POST'])
def YWRsendtransaction():
    route = sendTransaction(request, '/YWRsendtransaction', '/YWRdisplaywallet')
    if route:
        return route
    return render_template('sendtransaction.html', amount=v.amo, minerfee=v.minerfee, recipent=v.receipentaddress, error=v.error, step=4, yeti='warm')

if __name__ == "__main__":
    app.run()

