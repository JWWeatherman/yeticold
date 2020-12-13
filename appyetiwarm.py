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
        return redirect('/YWmenu')
    return render_template('redirect.html', yeti='warm')

@app.route("/YWmenu", methods=['GET', 'POST'])
def YWmenu():
    if request.method == 'GET':
        v.wallet = os.path.exists(home + "/.bitcoin/yetiwalletpub") or os.path.exists(home + "/.bitcoin/wallet/yetiwalletpriv")
    if request.method == 'POST':
        if request.form['option'] == 'recovery':
            subprocess.run('rm -r ~/.bitcoin/yetiwallet* 2> /dev/null', shell=True, check=False)
            subprocess.run('rm -r ~/.bitcoin/wallets/yetiwallet* 2> /dev/null', shell=True, check=False)
            v.route = '/YWRscandescriptor'
        elif request.form['option'] == 'wallet':
            v.step = 6
            v.route = '/YWRrescanwallet'
            v.loadwallet = True
        else:
            subprocess.run('rm -r ~/.bitcoin/yetiwallet* 2> /dev/null', shell=True, check=False)
            subprocess.run('rm -r ~/.bitcoin/wallets/yetiwallet* 2> /dev/null', shell=True, check=False)
            v.route = '/YWgetseeds'
        return redirect('/YWblockchain')
    return render_template('menu.html', yeti='warm', wallet=v.wallet)

@app.route("/YWblockchain", methods=['GET', 'POST'])
def YWblockchain():
    route = blockChain(request, '/YWopenbitcoin')
    if route:
        return route
    return render_template('blockchain.html', yeti='warm')

@app.route("/YWopenbitcoin", methods=['GET', 'POST'])
def YWopenbitcoin():
    route = openBitcoin(request, '/YWopenbitcoin', v.route, v.loadwallet)
    if route:
        return route
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD, yeti='warm', step=5)

@app.route("/YWgetseeds", methods=['GET', 'POST'])
def YWgetseeds():
    route = getSeeds(request, '/YWprintdescriptor')
    if route:
        return route
    return render_template('getseeds.html', yeti='warm', step=6)

@app.route("/YWprintdescriptor", methods=['GET', 'POST'])
def YWprintdescriptor():
    if request.method == 'POST':
        return redirect('/YWdisplayseeds')
    return render_template('printpage.html', desc=v.pubdesc, yeti='warm', step=7)

@app.route('/YWdisplayseeds', methods=['GET', 'POST'])
def YWdisplayseeds():
    route = displaySeeds(request, '/YWdisplayseeds', '/YWcheckseeds')
    if route:
        return route
    return render_template('displayseeds.html', PPL=v.passphraselist, x=v.privkeycount + 1, step=v.privkeycount + 8, yeti='warm')

@app.route('/YWcheckseeds', methods=['GET', 'POST'])
def YWcheckseeds():
    route = checkSeeds(request, '/YWcheckseeds', '/YWcopyseeds')
    if route:
        return route
    return render_template('checkseeds.html', x=v.privkeycount + 1, error=v.error,step=v.privkeycount + 14, oldkeys=v.oldkeys, yeti='warm')

@app.route("/YWcopyseeds", methods=['GET', 'POST'])
def YWcopyseeds():
    if request.method == 'POST':
        return redirect('/YWRdisplaywallet')
    return render_template('copyseeds.html', yeti='warm', step=20)

@app.route("/YWRscandescriptor", methods=['GET', 'POST'])
def YWRscandescriptor():
    if request.method == 'POST':
        v.error = None
        v.pubdesc = request.form['descriptor'].replace('\n','')
        response = subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpub getdescriptorinfo "'+v.pubdesc+'"', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response, "response for function: check descriptor")
        if response[1] != b'':
            v.error = 'Invalid Descriptor'
            return redirect('/YWRscandescriptor')
        return redirect('/YWRimportseeds')
    return render_template('scandescriptor.html', pubdesc=v.pubdesc, yeti='warm', step=6, line=16)

@app.route('/YWRimportseeds', methods=['GET', 'POST'])
def YWRimportseeds():    
    v.step = 10
    route = importSeeds(request, '/YWRimportseeds', '/YWRrescanwallet')
    if route:
        return route
    return render_template('importseeds.html', x=v.privkeycount + 1, error=v.error, step=v.privkeycount + 7, yeti='warm')

@app.route("/YWRrescanwallet", methods=['GET', 'POST'])
def YWRrescanwallet():
    if request.method == 'POST':
        handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpriv rescanblockchain '+blockheight())
        return redirect('/YWRdisplaywallet')
    return render_template('rescanwallet.html', yeti='warm', step=16)

@app.route("/YWRdisplaywallet", methods=['GET', 'POST'])
def YWRdisplaywallet():
    return render_template('displaywallet.html', yeti='warm')

if __name__ == "__main__":
    app.run()

