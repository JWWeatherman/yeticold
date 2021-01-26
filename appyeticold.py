import os
import sys
home = os.getenv("HOME")
sys.path.append(home + '/yeticold/utils/')
from btcrpcfunctions import blockheight
from yetiroutefunctions import *
from yetifunctions import *
from formating import *
from imports import *
import forgetnetworks
import variables as v
v.rpcpsw = str(random.randrange(0,1000000))
v.settings = {"rpc_username": "rpcuser","rpc_password": v.rpcpsw, "rpc_host": "127.0.0.1","rpc_port": 8332,"address_chunk": 100}
v.wallet_template = "http://{rpc_username}:{rpc_password}@{rpc_host}:{rpc_port}/wallet/{wallet_name}"
app = Flask(__name__)

@app.errorhandler(werkzeug.exceptions.InternalServerError)
def handle_bad_request(e):
    if e.original_exception != None:
        e = e.original_exception
    return render_template('error.html', error=e, yeti='Cold'), 500


@app.route("/", methods=['GET', 'POST'])
def redirectroute():
    return redirect('/menu')
@app.route("/offimp", methods=['GET', 'POST'])
def redirectrouteoffimp():
    v.mode = "YetiLevelThreeSecondaryLoad"
    v.route = '/switchlaptopOffLoad'
    return redirect('/syncstep')
@app.route("/off", methods=['GET', 'POST'])
def redirectrouteoff():
    v.mode = "YetiLevelThreeSecondaryCreate"
    v.route = '/getseedsOff'
    subprocess.run('python3 ~/yeticold/utils/oldwallets.py 2> /dev/null', shell=True, check=False)
    return redirect('/syncstep')
@app.route("/offrec", methods=['GET', 'POST'])
def redirectrouteoffrec():
    v.mode = "YetiLevelThreeSecondaryRecover"
    v.route = '/scandescriptorOffRec'
    subprocess.run('python3 ~/yeticold/utils/oldwallets.py 2> /dev/null', shell=True, check=False)
    return redirect('/syncstep')

@app.route("/menu", methods=['GET', 'POST'])
def menu():
    if request.method == 'GET':
        v.wallet = os.path.exists(home + "/.bitcoin/yetiwalletpub") or os.path.exists(home + "/.bitcoin/wallets/yetiwalletpub")
    if request.method == 'POST':
        if request.form['option'] == 'recover':
            v.route = '/scandescriptorRec'
            v.mode = "YetiLevelThreePrimaryRecover"
            v.shortcut = "L3Recover"
            v.url = "rec.yeticold.com"
            subprocess.run('python3 ~/yeticold/utils/oldwallets.py 2> /dev/null', shell=True, check=False)
        elif request.form['option'] == 'load':
            v.route = '/recoverredirect'
            v.mode = "YetiLevelThreePrimaryLoad"
            v.shortcut = "L3Load"
            v.url = "load.yeticold.com"
        elif request.form['option'] == 'create':
            v.route = '/scandescriptor'
            v.mode = "YetiLevelThreePrimaryCreate"
            v.shortcut = "L3Create"
            v.url = "disc.yeticold.com"
            subprocess.run('python3 ~/yeticold/utils/oldwallets.py 2> /dev/null', shell=True, check=False)
        elif request.form['option'] == 'watch':
            v.mode = "YetiLevelThreePrimaryWatch"
            v.route = '/scandescriptorWatch'
            subprocess.run('python3 ~/yeticold/utils/oldwallets.py 2> /dev/null', shell=True, check=False)
        return redirect('/blockchain')
    return render_template('menu.html', wallet=v.wallet, yeti='Cold')

@app.route("/blockchain", methods=['GET', 'POST'])
def blockchain():
    route = blockChain(request, '/openbitcoin', mode=v.mode, shortcut='/shortcut')
    if route:
        return route
    return render_template('blockchain.html')

@app.route("/shortcut", methods=['GET', 'POST'])
def shortcut():
    if request.method == 'POST':
        if request.form['option'] == 'Yes':
            v.disconnected = True
        else:
            v.disconnected = False
        return redirect('/openbitcoin')
    return render_template('shortcut.html')

@app.route("/openbitcoin", methods=['GET', 'POST'])
def YCopenbitcoin():
    route = openBitcoin(request, '/openbitcoin', v.route, mode=v.mode, yeti='Cold')
    if route:
        return route
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD, step=5, switch=True, disconnected=v.disconnected, shortcut=v.shortcut, url=v.url, offline=False, mode=v.mode)

@app.route("/syncstep", methods=['GET', 'POST'])
def syncstep():
    if request.method == 'GET':
        if not os.path.exists(home + "/yeticold/connectionOff"):
            return redirect('/blockchainOff')
    if request.method == 'POST':
        return redirect('/blockchainOff')
    return render_template('syncstep.html', step=6)

@app.route("/blockchainOff", methods=['GET', 'POST'])
def blockchainOff():
    if (os.path.exists(home + "/.bitcoin")):
        createOrPrepend('\nserver=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword='+v.rpcpsw+'\n',home+'/.bitcoin/bitcoin.conf')
    else:
        subprocess.call('mkdir ~/.bitcoin',shell=True)
        createOrPrepend('\nserver=1\nrpcport=8332\nrpcuser=rpcuser\nprune=25000\nrpcpassword='+v.rpcpsw+'\n',home+'/.bitcoin/bitcoin.conf')
    return redirect('/openbitcoinOff')

@app.route("/openbitcoinOff", methods=['GET', 'POST'])
def openbitcoinOff():
    route = openBitcoin(request, '/openbitcoinOff', '/connectionOff', mode=v.mode)
    if route:
        return route
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD, step=7, offline=True, mode=v.mode)

@app.route("/connectionOff", methods=['GET', 'POST'])
def connection():
    if request.method == 'POST':
        forgetnetworks.forget_networks()
        return redirect(v.route)
    return render_template('connection.html', step=8)

##LOAD ROUTES

@app.route("/switchlaptopOffLoad", methods=['GET', 'POST'])
def switchlaptopOffLoad():
    return render_template('switchlaptop.html', step=9, instructions="Switch to your Primary laptop currently Showing step 5. Click next to show step 10.", laptop="Primary")

##WATCH ROUTES

@app.route("/scandescriptorWatch", methods=['GET', 'POST'])
def scandescriptorWatch():
    route = scanDescriptor(request, '/scandescriptorWatch', '/rescanWatch', offline=False)
    if route:
        return route
    return render_template('scandescriptor.html', step=6, error=v.error, line=0)

@app.route("/rescanWatch", methods=['GET', 'POST'])
def rescanWatch():
    if request.method == 'POST':
        return redirect('/recoverredirect')
    return render_template('rescanwallet.html', step=7)


##RECOVER ROUTES

@app.route("/scandescriptorOffRec", methods=['GET', 'POST'])
def scandescriptorOffRec():
    route = scanDescriptor(request, '/scandescriptorOffRec', '/importseedsOff')
    if route:
        return route
    return render_template('scandescriptorOff.html', step=9, error=v.error, line=16)

@app.route('/importseedsOff', methods=['GET', 'POST'])
def importseedsOff():
    route = importSeeds(request, '/importseedsOff', '/switchlaptopOffRec')
    if route:
        return route
    return render_template('importseeds.html', x=v.privkeycount + 1, error=v.error,step=v.privkeycount + 10)

@app.route("/switchlaptopOffRec", methods=['GET', 'POST'])
def switchlaptopOffRec():
    return render_template('switchlaptop.html', step=13, instructions="Switch to your Primary Laptop currently Showing step 5 and on your Primary Laptop click Next to show step 14.", laptop="Primary")

@app.route("/scandescriptorRec", methods=['GET', 'POST'])
def scandescriptorRec():
    route = scanDescriptor(request, '/scandescriptorRec', '/rescanRec', offline=False)
    if route:
        return route
    return render_template('scandescriptor.html', step=14, error=v.error, line=0)

@app.route("/rescanRec", methods=['GET', 'POST'])
def rescanRec():
    if request.method == 'POST':
        return redirect('/recoverredirect')
    return render_template('rescanwallet.html', step=15)

##CREATE ROUTES

@app.route("/getseedsOff", methods=['GET', 'POST'])
def getseedsOff():
    route = getSeeds(request, '/copyseedsOff')
    if route:
        return route
    return render_template('getseeds.html', step=9)

@app.route("/copyseedsOff", methods=['GET', 'POST'])
def copyseedsOff():
    if request.method == 'POST':
        return redirect('/exportdescriptorOff')
    return render_template('copyseeds.html', step=10, cdnum="fourteen")

@app.route("/exportdescriptorOff", methods=['GET', 'POST'])
def exportdescriptorOff():
    if request.method == 'POST':
        return redirect('/displayseedsOff')
    return render_template('exportdescriptor.html', step=11, instructions="Switch to your Primary Laptop currently showing step 5 and on your Primary Laptop click Next to show step 12.", laptop="Primary")

@app.route("/scandescriptor", methods=['GET', 'POST'])
def scandescriptor():
    route = scanDescriptor(request, '/scandescriptor', '/printpage', offline=False, create=True)
    if route:
        return route
    return render_template('scandescriptor.html', step=12, setup=True, error=v.error, line=0)

@app.route("/printpage", methods=['GET', 'POST'])
def printpage():
    if request.method == 'GET':
        SeedT = readFile(home+'/yeticold/templates/SeedTemplate.txt')
        SeedT.insert(0,v.pubdesc)
    if request.method == 'POST':
        return redirect('/switchlaptop')
    return render_template('printpage.html', txt=SeedT, len=len(SeedT), step=13)

@app.route("/switchlaptop", methods=['GET', 'POST'])
def switchlaptop():
    if request.method == 'POST':
        return redirect('/createredirect')
    return render_template('switchlaptop.html', step=14, instructions="Switch to your Secondary Laptop currently showing step 11 and on your Secondary Laptop click Next to show step 15", laptop="Secondary")

@app.route('/displayseedsOff', methods=['GET', 'POST'])
def displayseedsOff():
    route = displaySeeds(request, '/displayseedsOff', '/checkseedsOff')
    if route:
        return route
    return render_template('displayseeds.html', PPL=v.passphraselist, x=v.privkeycount + 1, step=15+v.privkeycount,nextroute='/checkseedsOff')

@app.route('/checkseedsOff', methods=['GET', 'POST'])
def checkseedsOff():
    route = checkSeeds(request, '/checkseedsOff', '/switchlaptopOff')
    if route:
        return route
    return render_template('checkseeds.html', x=v.privkeycount + 1, error=v.error,step=22+v.privkeycount,oldkeys=v.oldkeys,nextroute='/switchlaptopOff')

@app.route("/switchlaptopOff", methods=['GET', 'POST'])
def switchlaptopOff():
    return render_template('switchlaptop.html', step=29, instructions="Switch to your Primary Laptop currently showing step 14 and on your Primary click next to show step 30", laptop="Primary")

##END ROUTES

@app.route("/recoverredirect", methods=['GET', 'POST'])
def recoverredirect():
    if request.method == 'GET':
        erase()
    return render_template('recoverredirect.html', yeti='Cold', url='Core3.yeticold.com', step=16)

@app.route("/createredirect", methods=['GET', 'POST'])
def createredirect():
    if request.method == 'GET':
        erase()
    return render_template('createredirect.html', yeti='Cold', url='guide3.yeticold.com', step=30)

if __name__ == "__main__":
    app.run()
