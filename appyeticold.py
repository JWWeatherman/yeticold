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


#A
@app.route("/", methods=['GET', 'POST'])
def redirectroute():
    return redirect('/YCmenu')
@app.route("/off", methods=['GET', 'POST'])
def redirectrouteoff():
    v.route = "/YCgetseeds"
    return redirect('/YCopenbitcoinB')
@app.route("/offrec", methods=['GET', 'POST'])
def redirectrouteoffrec():
    v.route = "/YCRscandescriptorB"
    return redirect('/YCopenbitcoinB')

#ON
@app.route("/YCmenu", methods=['GET', 'POST'])
def YCmenu():
    if request.method == 'POST':
        if request.form['option'] == 'recovery':
            v.url = "desc.yeticold.com"
            v.route = "YCRscandescriptor"
        else:
            v.url = "rec.yeticold.com"
            v.route = "YCscandescriptor"
        return redirect('/YCblockchain')
    return render_template('menu.html')

@app.route("/YCblockchain", methods=['GET', 'POST'])
def YCblockchain():
    route = blockChain(request, '/YCopenbitcoin')
    if route:
        return route
    return render_template('blockchain.html')

#ON
@app.route("/YCopenbitcoin", methods=['GET', 'POST'])
def YCopenbitcoin():
    route = openBitcoin(request, '/YCopenbitcoin', v.route)
    if route:
        return route
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD, step=5, switch=True, url=v.url)

#OFF
@app.route("/YCopenbitcoinB", methods=['GET', 'POST'])
def YCopenbitcoinB():
    route = openBitcoin(request, '/YCopenbitcoinB', '/YCconnection', offline=True)
    if route:
        return route
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD, step=7)

#OFF
@app.route("/YCconnection", methods=['GET', 'POST'])
def YCconnection():
    if request.method == 'POST':
        subprocess.call(['python3 ~/yeticold/utils/forgetnetworks.py'],shell=True)
        subprocess.call(['nmcli n off'],shell=True)
        return redirect(v.route)
    return render_template('connection.html', step=8)

#OFF
@app.route("/YCRscandescriptorB", methods=['GET', 'POST'])
def YCRscandescriptorB():
    if request.method == 'POST':
        v.pubdesc = handleResponse('python3 ~/yeticold/utils/scanqrcode.py').replace('\n', '')
        v.privkeycount = 0
        return redirect('/YCRimportseeds')
    return render_template('scandescriptor.html', step=9)

#OFF
@app.route('/YCRimportseeds', methods=['GET', 'POST'])
def YCRimportseeds():
    route = importSeeds(request, '/YCRimportseeds', '/YCRswitchlaptop')
    if route:
        return route
    return render_template('importseeds.html', x=v.privkeycount + 1, error=v.error,step=v.privkeycount + 10)

#OFF
@app.route("/YCRswitchlaptop", methods=['GET', 'POST'])
def YCRswitchlaptop():
    return render_template('switchlaptop.html', step=14, instructions="Switch to your Primary laptop currently Showing step 5. Click next to show step 15.", laptop="Primary")

#ON
@app.route("/YCRscandescriptor", methods=['GET', 'POST'])
def YCRscandescriptor():
    if request.method == 'POST':
        v.pubdesc = handleResponse('python3 ~/yeticold/utils/scanqrcode.py').replace('\n', '')
        return redirect('/YCRrescanwallet')
    return render_template('scandescriptor.html', step=15)

#ON
@app.route("/YCRrescanwallet", methods=['GET', 'POST'])
def YCRrescanwallet():
    handleResponse('bitcoin-cli -rpcwallet=yetiwalletpub importdescriptors \'[{ "desc": "'+v.pubdesc+'", "timestamp": "now"}]\'')
    handleResponse('bitcoin-cli -rpcwallet=yetiwalletpub rescanblockchain '+blockheight())
    return redirect('/YCRdisplaywallet')
#ON
@app.route("/YCRdisplaywallet", methods=['GET', 'POST'])
def YCRdisplaywallet():
    return render_template('YCRdisplaywallet.html', yeti="cold")

#ON

#OFF
@app.route("/YCgetseeds", methods=['GET', 'POST'])
def YCgetseeds():
    route = getSeeds(request, '/YCdisplaydescriptor')
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
        handleResponse('bitcoin-cli -rpcwallet=yetiwalletpub importdescriptors \'[{ "desc": "'+v.pubdesc+'", "timestamp": "now", "active": true}]\'')
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
    return render_template('checkseeds.html', x=v.privkeycount + 1, error=v.error,step=20+v.privkeycount,oldkeys=v.oldkeys)

#OFF
@app.route("/YCcopyseeds", methods=['GET', 'POST'])
def YCcopyseeds():
    if request.method == 'POST':
        return redirect('/YCRdisplaywallet')
    return render_template('copyseeds.html', step=26)


if __name__ == "__main__":
    app.run()

