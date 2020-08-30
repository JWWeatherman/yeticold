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
from btcrpcfunctions import *
from yetifunctions import *
from yetiroutefunctions import * 

app = Flask(__name__)
rpc = RPC("yetiwarm")


@app.errorhandler(werkzeug.exceptions.InternalServerError)
def handle_bad_request(e):
    if e.original_exception != None:
        e = e.original_exception
    return render_template('error.html', error=e), 500

@app.route("/", methods=['GET', 'POST'])
def redirectroute():
    if request.method == 'GET':
        return redirect('/YWblockchain')
    return render_template('redirect.html')

@app.route("/YWblockchain", methods=['GET', 'POST'])
def YWblockchain():
    route = blockChain(request, '/YWopenbitcoin')
    if route:
        return route
    return render_template('YWblockchain.html')

@app.route("/YWopenbitcoin", methods=['GET', 'POST'])
def YWopenbitcoin():
    route = openBitcoin(request, '/YWopenbitcoin', '/YWmenu')
    if route:
        return route
    return render_template('YWopenbitcoin.html', progress=v.progress, IBD=v.IBD)


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
    route = getSeeds(request, '/YWprintdescriptor')
    if route:
        return route
    return render_template('YWgetseeds.html')

@app.route("/YWprintdescriptor", methods=['GET', 'POST'])
def YWprintdescriptor():
    if request.method == 'GET':
        path = makeQrCode(v.pubdesc)
    if request.method == 'POST':
        return redirect('/YWdisplayseeds')
    return render_template('YWprintdescriptor.html', qrdata=v.pubdesc, path=path)

@app.route('/YWdisplayseeds', methods=['GET', 'POST'])
def YWdisplayseeds():
    route = displaySeeds(request, '/YWdisplayseeds', '/YWcheckseeds')
    if route != None:
        return route
    return render_template('YWdisplayseeds.html', PPL=v.passphraselist, x=v.privkeycount + 1, i=v.privkeycount + 9)

@app.route('/YWcheckseeds', methods=['GET', 'POST'])
def YWcheckseeds():
    route = checkSeeds(request, '/YWcheckseeds', '/YWcopyseeds')
    if route:
        return route
    return render_template('YWcheckseeds.html', x=v.privkeycount + 1, error=v.error,i=v.privkeycount + 16,oldkeys=v.oldkeys)

@app.route("/YWcopyseeds", methods=['GET', 'POST'])
def YWcopyseeds():
    if request.method == 'POST':
        return redirect('/YWRdisplaywallet')
    return render_template('YWcopyseeds.html')

@app.route("/YWRscandescriptor", methods=['GET', 'POST'])
def YWRscandescriptor():
    if request.method == 'POST':
        v.pubdesc = handleResponse('python3 ~/yeticold/utils/scanqrcode.py').replace('\n', '')
        return redirect('/YWRrescanwallet')
    return render_template('YWRscandescriptor.html', pubdesc=v.pubdesc)

@app.route("/YWRrescanwallet", methods=['GET', 'POST'])
def YWRrescanwallet():
    if request.method == 'GET':
        handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwallet importmulti \'[{ "desc": "'+v.pubdesc+'", "timestamp": "now", "range": [0,999], "watchonly": false}]\' \'{"rescan": true}\'')
        handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwallet rescanblockchain '+blockheight())
    if request.method == 'POST':
        return redirect('/YWRdisplaywallet')
    return render_template('YWRrescanwallet.html')

@app.route("/YWRdisplaywallet", methods=['GET', 'POST'])
def YWRdisplaywallet():
    route = displaywallet(request, '/YWRscanrecipent')
    if route:
        return route
    return render_template('YWRdisplaywallet.html', addresses=v.addresses, len=len(v.addresses), TWB=v.totalwalletbal)

@app.route("/YWRscanrecipent", methods=['GET', 'POST'])
def YWRscanrecipent():
    route = scanrecipent(request, '/YWRscanrecipent', '/YWRimportseeds')
    if route:
        return route
    return render_template('YWRscanrecipent.html', error=v.error, recipent=v.receipentaddress)

@app.route('/YWRimportseeds', methods=['GET', 'POST'])
def YWRimportseeds():    
    route = importSeeds(request, '/YWRimportseeds', '/YWRsendtransaction')
    if route:
        return route
    return render_template('YWRimportseeds.html', x=v.privkeycount + 1, error=v.error,i=v.privkeycount + 2 )

#GEN trans qr code
@app.route("/YWRsendtransaction", methods=['GET', 'POST'])
def YWRsendtransaction():
    route = sendTransaction(request, '/YWRsendtransaction', '/YWRdisplaywallet')
    if route:
        return route
    return render_template('YWRsendtransaction.html', amount=v.amo, minerfee=v.minerfee, recipent=v.receipentaddress, error=v.error)

#GEN trans qr code
@app.route("/YWRsendtransactionB", methods=['GET', 'POST'])
def YWRsendtransactionB():
    route = sendTransaction(request, '/YWRsendtransactionB', '/YWRdisplaywallet')
    if route:
        return route
    return render_template('YWRsendtransactionB.html', amount=v.amo, minerfee=v.minerfee, recipent=v.receipentaddress, error=v.error)

@app.route("/YWopenbitcoinB", methods=['GET', 'POST'])
def YWopenbitcoinB():
    route = openBitcoin(request, '/YWopenbitcoinB', '/YWRimportseeds')
    if route:
        return route
    return render_template('YWopenbitcoinB.html', progress=v.progress, IBD=v.IBD)

if __name__ == "__main__":
    app.run()
