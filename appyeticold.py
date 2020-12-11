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
    return redirect('/menu')
@app.route("/offimp", methods=['GET', 'POST'])
def redirectrouteoffimp():
    v.info = "yetiColdOffImp"
    return redirect('/blockchainOff')
@app.route("/off", methods=['GET', 'POST'])
def redirectrouteoff():
    v.info = "yetiColdOff"
    return redirect('/blockchainOff')
@app.route("/offrec", methods=['GET', 'POST'])
def redirectrouteoffrec():
    v.info = "yetiColdOffRec"
    return redirect('/blockchainOff')

#ON
@app.route("/menu", methods=['GET', 'POST'])
def menu():
    if request.method == 'GET':
        v.wallet = os.path.exists(home + "/.bitcoin/yetiwalletpub") or os.path.exists(home + "/.bitcoin/wallet/yetiwalletpub")
    if request.method == 'POST':
        if request.form['option'] == 'recovery':
            v.info = "yetiColdRec"
            v.route = '/scandescriptorRec'
            v.url = "rec.yeticold.com"
            subprocess.run('rm -r ~/.bitcoin/yetiwallet* 2> /dev/null', shell=True, check=False)
            subprocess.run('rm -r ~/.bitcoin/wallets/yetiwallet* 2> /dev/null', shell=True, check=False)
        elif request.form['option'] == 'wallet':
            v.info = 'yetiColdImp'
            v.route = '/rescanwalletImp'
            v.url = "loa.yeticlod.com"
        else:
            v.info = "yetiCold"
            v.url = "desc.yeticold.com"
            v.route = '/scandescriptor'
            subprocess.run('rm -r ~/.bitcoin/yetiwallet* 2> /dev/null', shell=True, check=False)
            subprocess.run('rm -r ~/.bitcoin/wallets/yetiwallet* 2> /dev/null', shell=True, check=False)
        return redirect('/blockchain')
    return render_template('menu.html', wallet=v.wallet)

@app.route("/blockchain", methods=['GET', 'POST'])
def blockchain():
    route = blockChain(request, '/openbitcoin')
    if route:
        return route
    return render_template('blockchain.html')

@app.route("/openbitcoin", methods=['GET', 'POST'])
def YCopenbitcoin():
    if v.info == 'yetiColdImp':
        step = 1
    else:
        step = 5
    route = openBitcoin(request, '/openbitcoin', v.route, v.info, offline=False, yeti='cold')
    if route:
        return route
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD, step=step, switch=True, url=v.url)

@app.route("/rescanwalletImp", methods=['GET', 'POST'])
def rescanwalletImp():
    if request.method == 'POST':
        handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpub rescanblockchain '+blockheight())
        return redirect('/coldwalletguide')
    return render_template('rescanwallet.html',step=6)

@app.route("/blockchainOff", methods=['GET', 'POST'])
def blockchainOff():
    route = blockChain(request, '/openbitcoinOff')
    if route:
        return route
    return render_template('blockchain.html')

#OFF
@app.route("/openbitcoinOff", methods=['GET', 'POST'])
def openbitcoinOff():
    v.step = 7
    if v.info == "yetiColdOffRec":
        v.route = '/scandescriptorOffRec'
    elif v.info == 'yetiColdOffImp':
        v.route = '/switchlaptopOffImp' 
        v.step = 3
    else:
        v.route = '/getseedsOff'
    route = openBitcoin(request, '/openbitcoinOff', '/connectionOff', v.info, offline=True)
    if route:
        return route
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD, step=v.step)

#OFF
@app.route("/connectionOff", methods=['GET', 'POST'])
def connection():
    if request.method == 'POST':
        subprocess.call(['python3 ~/yeticold/utils/forgetnetworks.py'],shell=True)
        subprocess.call(['nmcli n off'],shell=True)
        return redirect(v.route)
    return render_template('connection.html', step=v.step+1)

@app.route("/switchlaptopOffImp", methods=['GET', 'POST'])
def switchlaptopOffImp():
    return render_template('switchlaptop.html', step=5, instructions="Switch to your Primary laptop currently Showing step 1. Click next to show step 6.", laptop="Primary")

#OFF
@app.route("/scandescriptorOffRec", methods=['GET', 'POST'])
def scandescriptorOffRec():
    if request.method == 'POST':
        v.error = None
        v.pubdesc = request.form['descriptor'].replace('\n','')
        response = subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpriv getdescriptorinfo "'+v.pubdesc+'"', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response, "response for function: check descriptor")
        print(repr(v.pubdesc))
        if response[1] != b'':
            v.error = 'Invalid Descriptor'
            return redirect('/scandescriptorOffRec')
        v.privkeycount = 0
        return redirect('/importseedsOff')
    return render_template('scandescriptor.html', step=9, error=v.error, line=16)

#OFF
@app.route('/importseedsOff', methods=['GET', 'POST'])
def importseedsOff():
    route = importSeeds(request, '/importseedsOff', '/switchlaptopOffRec')
    if route:
        return route
    return render_template('importseeds.html', x=v.privkeycount + 1, error=v.error,step=v.privkeycount + 10)

#OFF
@app.route("/switchlaptopOffRec", methods=['GET', 'POST'])
def switchlaptopOffRec():
    return render_template('switchlaptop.html', step=14, instructions="Switch to your Primary laptop currently Showing step 5. Click next to show step 15.", laptop="Primary")

#ON
@app.route("/scandescriptorRec", methods=['GET', 'POST'])
def scandescriptorRec():
    if request.method == 'POST':
        v.error = None
        v.pubdesc = request.form['descriptor'].replace('\n','')
        response = subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpub getdescriptorinfo "'+v.pubdesc+'"', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response, "response for function: check descriptor")
        if response[1] != b'':
            v.error = 'Invalid Descriptor'
            redirect('/scandescriptorRec')
        return redirect('/rescanwalletRec')
    return render_template('scandescriptor.html', step=15, error=v.error, line=16)

#ON
@app.route("/rescanwalletRec", methods=['GET', 'POST'])
def rescanwalletRec():
    if request.method == 'POST':
        handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpub importdescriptors \'[{ "desc": "'+v.pubdesc+'", "timestamp": "now"}]\'')
        handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpub rescanblockchain '+blockheight())
        return redirect('/coldwalletguide')
    return render_template('rescanwallet.html',step=16)
#ON
@app.route("/coldwalletguide", methods=['GET', 'POST'])
def coldwalletguide():
    return render_template('coldwalletguide.html')
    ##Redirect to yetihosted send/recive guide for yeticold

#ON

#OFF
@app.route("/getseedsOff", methods=['GET', 'POST'])
def getseedsOff():
    route = getSeeds(request, '/exportdescriptorOff')
    if route:
        return route
    return render_template('getseeds.html', step=9)

#OFF
@app.route("/exportdescriptorOff", methods=['GET', 'POST'])
def exportdescriptorOff():
    route = exportDescriptor(request, '/displayseedsOff')
    if route:
        return route
    return render_template('exportdescriptor.html', step=10, instructions="Switch to your Primary laptop currently showing step 5, click next to show step 11", laptop="Primary")

#ON
@app.route("/scandescriptor", methods=['GET', 'POST'])
def scandescriptor():
    if request.method == 'POST':
        v.error = None
        v.pubdesc = request.form['descriptor'].replace('\n','')
        response = subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpub getdescriptorinfo "'+v.pubdesc+'"', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response, "response for function: check descriptor")
        if response[1] != b'':
            v.error = 'Invalid Descriptor'
            redirect('/scandescriptor')
        handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpub importdescriptors \'[{ "desc": "'+v.pubdesc+'", "timestamp": "now", "active": true}]\'')
        return redirect('/printpage')
    return render_template('scandescriptor.html', step=11, setup=True, error=v.error, line=0)

#ON
@app.route("/printpage", methods=['GET', 'POST'])
def printpage():
    if request.method == 'POST':
        return redirect('/switchlaptop')
    return render_template('printpage.html', desc=v.pubdesc, step=12)

#ON
@app.route("/switchlaptop", methods=['GET', 'POST'])
def switchlaptop():
    if request.method == 'POST':
        return redirect('/coldwalletguide')
    return render_template('switchlaptop.html', step=13, instructions="Switch to your Secondary laptop currently showing step 10, click next to show step 14", laptop="Secondary")

#OFF
@app.route('/displayseedsOff', methods=['GET', 'POST'])
def displayseedsOff():
    route = displaySeeds(request, '/displayseedsOff', '/checkseedsOff')
    if route:
        return route
    return render_template('displayseeds.html', PPL=v.passphraselist, x=v.privkeycount + 1, step=14+v.privkeycount)

#OFF
@app.route('/checkseedsOff', methods=['GET', 'POST'])
def checkseedsOff():
    route = checkSeeds(request, '/checkseedsOff', '/copyseedsOff')
    if route:
        return route
    return render_template('checkseeds.html', x=v.privkeycount + 1, error=v.error,step=21+v.privkeycount,oldkeys=v.oldkeys)

#OFF
@app.route("/copyseedsOff", methods=['GET', 'POST'])
def copyseedsOff():
    if request.method == 'POST':
        return redirect('/switchlaptopOff')
    return render_template('copyseeds.html', step=27)

@app.route("/switchlaptopOff", methods=['GET', 'POST'])
def switchlaptopOff():
    return render_template('switchlaptop.html', step=28, instructions="Switch to your Primary laptop currently showing step 13, click next to show your cold wallet guide", laptop="Secondary")


if __name__ == "__main__":
    app.run()

