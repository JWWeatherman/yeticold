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
    return render_template('error.html', error=e, yeti='Warm'), 500

@app.route("/", methods=['GET', 'POST'])
def redirectroute():
    if request.method == 'GET':
        return redirect('/YWmenu')
    return render_template('redirect.html', yeti='Warm')

@app.route("/YWmenu", methods=['GET', 'POST'])
def YWmenu():
    if request.method == 'GET':
        v.wallet = os.path.exists(home + "/.bitcoin/yetiwalletpriv") or os.path.exists(home + "/.bitcoin/wallets/yetiwalletpriv")
    if request.method == 'POST':
        if request.form['option'] == 'recover':
            subprocess.run('python3 ~/yeticold/utils/oldwallets.py 2> /dev/null', shell=True, check=False)
            v.mode = "YetiLevelTwoRecover"
            v.route = '/YWRscandescriptor'
        elif request.form['option'] == 'load':
            v.route = '/recoverredirect'
            v.mode = "YetiLevelTwoLoad"
        elif request.form['option'] == 'create':
            v.mode = "YetiLevelTwoCreate"
            subprocess.run('python3 ~/yeticold/utils/oldwallets.py 2> /dev/null', shell=True, check=False)
            v.route = '/YWgetseeds'
        return redirect('/YWblockchain')
    return render_template('menu.html', yeti='Warm', wallet=v.wallet)

@app.route("/YWblockchain", methods=['GET', 'POST'])
def YWblockchain():
    route = blockChain(request, '/YWopenbitcoin', mode=v.mode)
    if route:
        return route
    return render_template('blockchain.html', yeti='Warm')

@app.route("/YWopenbitcoin", methods=['GET', 'POST'])
def YWopenbitcoin():
    route = openBitcoin(request, '/YWopenbitcoin', v.route, mode=v.mode)
    if route:
        return route
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD, yeti='Warm', step=5, offline=False, mode=v.mode)

@app.route("/YWgetseeds", methods=['GET', 'POST'])
def YWgetseeds():
    route = getSeeds(request, '/YWcopyseeds')
    if route:
        return route
    return render_template('getseeds.html', yeti='Warm', step=6)

@app.route("/YWcopyseeds", methods=['GET', 'POST'])
def YWcopyseeds():
    if request.method == 'POST':
        return redirect('/YWcheckseeds')
    return render_template('copyseeds.html', yeti='Warm', step=7, cdnum="seven")

@app.route('/YWcheckseeds', methods=['GET', 'POST'])
def YWcheckseeds():
    route = checkSeeds(request, '/YWcheckseeds', '/createredirect', yeti='Warm')
    if route:
        return route
    return render_template('checkseeds.html', x=v.privkeycount + 1, error=v.error,step=v.privkeycount + 8, oldkeys=v.oldkeys, yeti='Warm',nextroute='/createredirect')

@app.route("/createredirect", methods=['GET', 'POST'])
def createredirect():
    return render_template('createredirect.html', yeti='Warm', url='guide2.yeticold.com', step=14)

@app.route("/YWRscandescriptor", methods=['GET', 'POST'])
def YWRscandescriptor():
    route = scanDescriptor(request, '/YWRscandescriptor', '/YWRimportseeds')
    if route:
        return route
    return render_template('scandescriptorOff.html', pubdesc=v.pubdesc, yeti='Warm', step=6, line=16)

@app.route('/YWRimportseeds', methods=['GET', 'POST'])
def YWRimportseeds():    
    route = importSeeds(request, '/YWRimportseeds', '/recoverredirect')
    if route:
        return route
    return render_template('importseeds.html', x=v.privkeycount + 1, error=v.error, step=v.privkeycount + 7, yeti='Warm')

@app.route("/recoverredirect", methods=['GET', 'POST'])
def recoverredirect():
    return render_template('recoverredirect.html', yeti='Warm', url='Core2.yeticold.com')

if __name__ == "__main__":
    app.run()

