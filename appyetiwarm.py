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
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD, yeti='warm', step=5)


@app.route("/YWmenu", methods=['GET', 'POST'])
def YWmenu():
    subprocess.call(['bitcoin-cli createwallet "yetiwalletpriv" false true "" false true'],shell=True)
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
    return render_template('getseeds.html', yeti='warm', step=6)

@app.route("/YWprintdescriptor", methods=['GET', 'POST'])
def YWprintdescriptor():
    if request.method == 'GET':
        path = makeQrCode(v.pubdesc)
    if request.method == 'POST':
        return redirect('/YWdisplayseeds')
    return render_template('printdescriptor.html', qrdata=v.pubdesc, path=path, yeti='warm', step=7)

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
        v.pubdesc = handleResponse('python3 ~/yeticold/utils/scanqrcode.py').replace('\n', '')
        return redirect('/YWRimportseeds')
    return render_template('scandescriptor.html', pubdesc=v.pubdesc, yeti='warm', step=6)

@app.route('/YWRimportseeds', methods=['GET', 'POST'])
def YWRimportseeds():    
    route = importSeeds(request, '/YWRimportseeds', '/YWRrescanwallet')
    if route:
        return route
    return render_template('importseeds.html', x=v.privkeycount + 1, error=v.error, step=v.privkeycount + 7, yeti='warm')

@app.route("/YWRdisplaywallet", methods=['GET', 'POST'])
def YWRdisplaywallet():
    return render_template('displaywallet.html', yeti='warm')

if __name__ == "__main__":
    app.run()

