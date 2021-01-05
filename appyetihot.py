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
    return render_template('error.html', error=e, yeti='Hot'), 500

@app.route("/", methods=['GET', 'POST'])
def redirectroute():
    if request.method == 'GET':
        return redirect('/YHmenu')
    return render_template('redirect.html')

@app.route("/YHmenu", methods=['GET', 'POST'])
def YHmenu():
    if request.method == 'GET':
        v.wallet = os.path.exists(home + "/.bitcoin/yetiwallethot") or os.path.exists(home + "/.bitcoin/wallets/yetiwallethotyetiwallethot")
    if request.method == 'POST':
        if request.form['option'] == 'recover':
            v.mode = "YetiLevelOneRecover"
            v.route = '/YHRinputseed'
            subprocess.run('python3 ~/yeticold/utils/oldwallets.py 2> /dev/null', shell=True, check=False)
        elif request.form['option'] == 'load':
            v.mode = "YetiLevelOneLoad"
            v.route = '/YHRrescanwallet'
        elif request.form['option'] == 'create':
            v.mode = "YetiLevelOneCreate"
            v.route = '/YHgetseed'
            subprocess.run('python3 ~/yeticold/utils/oldwallets.py 2> /dev/null', shell=True, check=False)
        return redirect('/YHblockchain')
    return render_template('menu.html', yeti='Hot', wallet=v.wallet)

@app.route("/YHblockchain", methods=['GET', 'POST'])
def YHblockchain():
    route = blockChain(request, '/YHopenbitcoin', mode=v.mode)
    if route:
        return route
    return render_template('blockchain.html')

@app.route("/YHopenbitcoin", methods=['GET', 'POST'])
def YHopenbitcoin():
    route = openBitcoin(request, '/YHopenbitcoin', v.route, mode=v.mode, yeti='Hot')
    if route:
        return route
    return render_template('openbitcoin.html', progress=v.progress, IBD=v.IBD, step=5, yeti='Hot', offline=False)

@app.route("/YHgetseed", methods=['GET', 'POST'])
def YHgetseed():
    if request.method == 'POST':
        handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetiwalletgen"')
        if request.form['skip'] == 'skip':
            newbinary = str('1') * 256
        else:
            newbinary = request.form['binary']
        adr = handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletgen getnewaddress')
        print(adr)
        newprivkey =  handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletgen dumpprivkey '+adr)
        binary = bin(decode58(newprivkey))[ 2:][8:-40]
        v.privkey = ConvertToWIF(xor(binary,newbinary))
        handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwallethot sethdseed true "'+v.privkey+'"')
        handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli unloadwallet "yetiwalletgen"')
        v.passphraselist = ConvertToPassphrase(v.privkey)
        file = ''
        phrasenum = 0
        for x in range(0,13):
            line = ""
            for y in range(0,4):
                line = line + v.passphraselist[phrasenum] + ' '
                phrasenum = phrasenum + 1
            line = line + checksum(line)
            file = file + line + '\n'
        createOrPrepend(file, home+'/Documents/yhseed.txt')
        return redirect('/YHcopyseed')
    return render_template('getseed.html', yeti='Hot', step=6)

@app.route("/YHcopyseed", methods=['GET', 'POST'])
def YHcopyseed():
    if request.method == 'POST':
        v.privkeycount = 0
        return redirect('/YHcheckseed')
    return render_template('copyseed.html', yeti='Hot', step=9)

#confirm privkey
@app.route('/YHcheckseed', methods=['GET', 'POST'])
def YHcheckseed():
    if request.method == 'POST':
        privkeylisttoconfirm = []
        v.oldkeys = []
        for i in range(1,14):
            inputlist = request.form['row' + str(i)]
            v.oldkeys.append(inputlist)
            inputlist = inputlist.split(' ')
            inputlist = inputlist[0:4]
            privkeylisttoconfirm.append(inputlist[0])
            privkeylisttoconfirm.append(inputlist[1])
            privkeylisttoconfirm.append(inputlist[2])
            privkeylisttoconfirm.append(inputlist[3])
        if privkeylisttoconfirm == v.passphraselist:
            v.oldkeys = None
            v.privkeycount = v.prinkeycount + 1
            if v.privkeycount == 5:
                return redirect('/YHRdisplaywallet')
            else:
                return redirect('/YHcheckseed')
        else:
            v.error = 'The seed words you entered are incorrect. This is probably because you entered a line twice or put them in the wrong order.'
    return render_template('checkseeds.html', x=v.privkeycount+1, error=v.error, step=v.privkeycount+8,oldkeys=v.oldkeys, yeti='Hot')

@app.route("/YHRdisplaywallet", methods=['GET', 'POST'])
def YHRdisplaywallet():
    return render_template('displaywallet.html', yeti='Hot')
    
@app.route('/YHRinputseed', methods=['GET', 'POST'])
def YHRinputseed():
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
        v.privkey = PassphraseListToWIF(privkey)
        handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwallethot sethdseed true "'+v.privkey+'"')
        return redirect('/YHRrescanwallet')
    return render_template('importseeds.html', x=1, error=v.error, yeti='Hot', step=6)

@app.route("/YHRrescanwallet", methods=['GET', 'POST'])
def YHRrescanwallet():
    if request.method == 'POST':
        handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwallethot rescanblockchain '+blockheight())
        return redirect('/YHRdisplaywallet')
    return render_template('rescanwallet.html', yeti='Hot', step=7)

if __name__ == "__main__":
    app.run()
