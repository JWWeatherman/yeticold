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
        return redirect('/YHblockchain')
    return render_template('redirect.html')

@app.route("/YHblockchain", methods=['GET', 'POST'])
def YHblockchain():
    route = blockChain(request, '/YHopenbitcoin')
    if route:
        return route
    return render_template('blockchain.html')

@app.route("/YHopenbitcoin", methods=['GET', 'POST'])
def YHopenbitcoin():
    route = openBitcoin(request, '/YHopenbitcoin', '/YHmenu')
    v.progress
    if route:
        return route
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD, step=5)

@app.route("/YHmenu", methods=['GET', 'POST'])
def YHmenu():
    subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetiwalletpriv" false true "" false true'],shell=True)
    if request.method == 'POST':
        if request.form['option'] == 'recovery':
            return redirect('/YHRinputseed')
        else:
            return redirect('/YHgetseed')
    return render_template('menu.html', yeti="hot")

@app.route("/YHgetseed", methods=['GET', 'POST'])
def YHgetseed():
    global privkey
    global xpriv
    global pubdesc
    if request.method == 'POST':
        if request.form['skip'] == 'skip':
            newbinary = '1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
        else:
            newbinary = request.form['binary']
        subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetihot"','~/yeticold/bitcoin/bin/bitcoin-cli loadwallet "yetihot"'],shell=True)
        rpc = RPC()
        adr = rpc.getnewaddress()
        newprivkey = rpc.dumpprivkey(adr)
        binary = bin(decode58(newprivkey))[2:][8:-40]
        privkey = ConvertToWIF(xor(binary,newbinary))
        home = os.getenv('HOME')
        path = home + '/yetihotwallet'
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetihot sethdseed true "'+privkey+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return redirect('/YHdisplayseed')
    return render_template('getseed.html', yeti="hot", step=5)

@app.route('/YHdisplayseed', methods=['GET', 'POST'])
def YHdisplayseed():
    global privkey
    global privkeycount
    if request.method == 'GET':
        passphraselist = ConvertToPassphrase(privkey)
    if request.method == 'POST':
        home = os.getenv('HOME')
        path = home + '/Documents'
        subprocess.call('rm '+path+'/yhseed.txt', shell=True)
        subprocess.call('touch '+path+'/yhseed.txt', shell=True)
        file = ''
        for i in range(0,13):
            file = file + request.form['displayrow' + str(i+1)] + '\n'
        subprocess.call('echo "'+file+'" >> '+path+'/yhseed.txt', shell=True)
        return redirect('/YHcheckseed')
    return render_template('displayseed.html', x=1, PPL=passphraselist, yeti="hot", step=6)
#confirm privkey
@app.route('/YHcheckseed', methods=['GET', 'POST'])
def YHcheckseed():
    global privkey
    global xpriv
    global error
    global oldkeys
    if request.method == 'POST':
        passphraselist = ConvertToPassphrase(privkey)
        privkeylisttoconfirm = []
        oldkeys = []
        for i in range(1,14):
            inputlist = request.form['row' + str(i)]
            oldkeys.append(inputlist)
            inputlist = inputlist.split(' ')
            inputlist = inputlist[0:4]
            privkeylisttoconfirm.append(inputlist[0])
            privkeylisttoconfirm.append(inputlist[1])
            privkeylisttoconfirm.append(inputlist[2])
            privkeylisttoconfirm.append(inputlist[3])
        if privkeylisttoconfirm == passphraselist:
            oldkeys = None
            return redirect('/YHcopyseed')
        else:
            error = 'The seed words you entered are incorrect. This is probably because you entered a line twice or put them in the wrong order.'
    return render_template('checkseed.html', x=1, error=error, step=7,oldkeys=oldkeys, yeti="hot")

@app.route("/YHcopyseed", methods=['GET', 'POST'])
def YHcopyseed():
    if request.method == 'POST':
        return redirect('/YHRdisplaywallet')
    return render_template('copyseed.html', yeti="hot", step=8)

@app.route("/YHRdisplaywallet", methods=['GET', 'POST'])
def YHRdisplaywallet():
    return render_template('displaywallet.html', yeti='hot')
    
@app.route('/YHRinputseed', methods=['GET', 'POST'])
def YHRinputseed():
    global error 
    if request.method == 'POST':
        privkey = []
        for i in range(1,14):
            inputlist = request.form['row' + str(i)]
            inputlist = inputlist.split(' ')
            inputlist = inputlist[0:4]
            privkey.append(inputlist[0])
            privkey.append(inputlist[1])
            privkey.append(inputlist[2])
            privkey.append(inputlist[3])
        privkey = PassphraseListToWIF(privkey)
        error = None
        rpc = RPC()
        subprocess.call(['~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetihot" false true'],shell=True)
        response = subprocess.Popen(['~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetihot sethdseed true "'+privkey+'"'],shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        return redirect('/YHRdisplaywallet')
    return render_template('inputseed.html', x=1, error=error, yeti="hot", step=5)

if __name__ == "__main__":
    app.run()
