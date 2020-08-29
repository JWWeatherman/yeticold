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

# @app.route("/test", methods=['GET', 'POST'])       
# def test():
#     if request.method == 'GET':
#         print(thirdqrcode)
#         thirdqrcode = 1
#         print(thirdqrcode)
#         print("hi")
#         print(thirdqrcode)
#     return render_template('v.error.html', error="hi")


#ROUTES
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
    getSeeds(request, '/YWprintdescriptor')
    return render_template('YWgetseeds.html')

#display for print
@app.route("/YWprintdescriptor", methods=['GET', 'POST'])
def YWprintdescriptor():
    if request.method == 'GET':
        path = makeQrCode(v.pubdesc)
    if request.method == 'POST':
        return redirect('/YWdisplayseeds')
    return render_template('YWprintdescriptor.html', qrdata=v.pubdesc, path=v.path)

@app.route('/YWdisplayseeds', methods=['GET', 'POST'])
def YWdisplayseeds():
    route = displaySeeds(request, '/YWdisplayseeds', '/YWcheckseeds')
    if route != None:
        return route
    return render_template('YWdisplayseeds.html', PPL=v.passphraselist, x=v.privkeycount + 1, i=v.privkeycount + 9)

@app.route('/YWcheckseeds', methods=['GET', 'POST'])
def YWcheckseeds():
    checkSeeds(request, '/YWcheckseeds', '/YWcopyseeds')
    return render_template('YWcheckseeds.html', x=v.privkeycount + 1, error=v.error,i=v.privkeycount + 16,oldkeys=v.oldkeys)

@app.route("/YWcopyseeds", methods=['GET', 'POST'])
def YWcopyseeds():
    if request.method == 'POST':
        return redirect('/YWRdisplaywallet')
    return render_template('YWcopyseeds.html')

@app.route("/YWRscandescriptor", methods=['GET', 'POST'])
def YWRscandescriptor():
    if request.method == 'POST':
        pubdesc = handleResponse('python3 ~/yeticold/utils/scanqrcode.py').replace('\n', '')
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
    if request.method == 'GET':
        v.addresses = []
        v.totalwalletbal = 0
        subprocess.call(['rm -r ~/yeticold/static/qrcode*'],shell=True)
        adrlist = handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwallet deriveaddresses "'+pubdesc+'" "[0,999]"', True)
        rpc = RPC("yetiwallet")
        for i in range(0, len(adrlist)):
            adr = adrlist[i]
            randomnum = str(random.randrange(0,1000000))
            route = url_for('static', filename='qrcode'+adr+''+randomnum+'.png')
            response = rpc.listunspent(0, 9999999, [adr])
            if response == []:
                rpc.importaddress(adrlist[i],False,False)
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
                v.addresses.append(address)
            else:
                for x in range(0, len(response)):
                    utxo = response[x]
                    txid = utxo['txid']
                    vout = utxo['vout']
                    scriptPubKey = utxo['scriptPubKey']
                    numamount = utxo['amount']
                    v.totalwalletbal = v.totalwalletbal + numamount
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
                    v.addresses.append(address)
        v.addresses.sort(key=lambda x: x['balance'], reverse=True)
        for i in range(0, len(v.addresses)):
            makeQrCode(v.addresses[i]['address'], home+'/yeticold/'+v.addresses[i]['route'])
    if request.method == 'POST':
        for i in range(0, len(v.addresses)):
            if v.addresses[i]['txid'] == request.form['txid']:
                sourceaddress = v.addresses[i]
        return redirect('/YWRscanrecipent')
    return render_template('YWRdisplaywallet.html', addresses=v.addresses, len=len(v.addresses), TWB=v.totalwalletbal)

@app.route("/YWRscanrecipent", methods=['GET', 'POST'])
def YWRscanrecipent():
    if request.method == 'POST':
        v.error = None
        if request.form['option'] == 'scan':
            v.receipentaddress = handleResponse('python3 ~/yeticold/utils/scanqrcode.py').replace('\n', '')
        else:
            v.receipentaddress = request.form['option']
        if (v.receipentaddress.split(':')[0] == 'bitcoin'):
            v.receipentaddress = v.receipentaddress.split(':')[1].split('?')[0]
        if (v.receipentaddress[:3] == 'bc1') or (v.receipentaddress[:1] == '3') or (v.receipentaddress[:1] == '1'):
            if not (len(v.receipentaddress) >= 26) and (len(v.receipentaddress) <= 35):
                v.error = v.receipentaddress + ' is not a valid bitcoin address, address should have a length from 26 to 35 instead of ' + str(len(v.receipentaddress)) + '.'
        else: 
            v.error = v.receipentaddress + ' is not a valid bitcoin address, address should have started with bc1, 3 or 1 instead of ' + v.receipentaddress[:1] + ', or ' + v.receipentaddress[:3] + '.'
        if v.error:
            return redirect('/YWRscanrecipent')
        return redirect('/YWRimportseeds')
    return render_template('YWRscanrecipent.html', error=v.error, recipent=v.receipentaddress)

@app.route('/YWRimportseeds', methods=['GET', 'POST'])
def YWRimportseeds():
    importSeeds(request, '/YWRimportseeds', '/YWRsendtransaction')
    return render_template('YWRimportseeds.html', x=v.privkeycount + 1, error=v.error,i=v.privkeycount + 2 )

#GEN trans qr code
@app.route("/YWRsendtransaction", methods=['GET', 'POST'])
def YWRsendtransaction():
    sendTransaction(request, '/YWRsendtransaction', '/YWRdisplaywallet')
    return render_template('YWRsendtransaction.html', amount=v.amo, minerfee=v.minerfee, recipent=v.receipentaddress, error=v.error)

#GEN trans qr code
@app.route("/YWRsendtransactionB", methods=['GET', 'POST'])
def YWRsendtransactionB():
    sendTransaction(request, '/YWRsendtransactionB', '/YWRdisplaywallet')
    return render_template('YWRsendtransactionB.html', amount=v.amo, minerfee=v.minerfee, recipent=v.receipentaddress, error=v.error)

@app.route("/YWopenbitcoinB", methods=['GET', 'POST'])
def YWopenbitcoinB():

    openBitcoin(request, '/YWopenbitcoinB', '/YWRimportseeds')
    return render_template('YWopenbitcoinB.html', progress=v.progress, IBD=v.IBD)

if __name__ == "__main__":
    app.run()
