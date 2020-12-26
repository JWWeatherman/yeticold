from imports import *
import variables as v
from yetifunctions import *
from btcrpcfunctions import *
from formating import *
home = os.getenv("HOME")

def blockChain(request, nextroute, mode="Create"):
    if request.method == 'GET':
        if (os.path.exists(home + "/.bitcoin")):
            print("1")
            createOrPrepend('\nserver=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword='+v.rpcpsw+'\n',home+'/.bitcoin/bitcoin.conf')
            return redirect(nextroute)
        elif mode == "Create":
            print("create dir")
            subprocess.call('mkdir ~/.bitcoin',shell=True)
            subprocess.call('sleep 3',shell=True) 
            createOrPrepend('\nserver=1\nrpcport=8332\nrpcuser=rpcuser\nprune=550\nrpcpassword='+v.rpcpsw+'\n',home+'/.bitcoin/bitcoin.conf')
            return redirect(nextroute)
        elif mode == "Load":
            print("3")
            createOrPrepend('\nserver=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword='+v.rpcpsw+'\n',home+'/.bitcoin/bitcoin.conf')
            return redirect(nextroute)
    if request.method == 'POST':
        subprocess.call('mkdir ~/.bitcoin',shell=True)
        if request.form['option'] == 'Skip':
            createOrPrepend('\nserver=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword='+v.rpcpsw+'\n',home+'/.bitcoin/bitcoin.conf')
            return redirect(nextroute)
        createOrPrepend('server=1\nrpcport=8332\nrpcuser=rpcuser\nprune='+str(getPrunBlockheightByDate(request.form['date']))+'\nrpcpassword='+v.rpcpsw+'',home+'/.bitcoin/bitcoin.conf')
        return redirect(nextroute)

def openBitcoin(request, currentroute, nextroute, loadwallet=False, offline=False, yeti='Warm'):
    if request.method == 'GET':
        v.IBD = BTCFinished()
        v.progress = BTCprogress()
        if not os.path.exists(home + "/.bitcoin/bitcoind.pid"):
            subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        if offline:
            response = subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-cli getblockchaininfo', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            if response[1] == b'':
                v.IBD = True
    if request.method == 'POST':
        if v.IBD:
            if loadwallet:
                if yeti == 'Cold' and not offline:
                    handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli loadwallet "yetiwalletpub"')
                elif yeti == 'Hot':
                    handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli loadwallet "yetiwallethot"')
                else:
                    handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli loadwallet "yetiwalletpriv"')
            else:
                if yeti == 'Cold' and not offline:
                    handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetiwalletpub" true true "" false true')     
                elif yeti == 'Hot':
                    handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetiwallethot" false true')
                else: 
                    handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetiwalletpriv" false true "" false true')
            return redirect(nextroute)
        else:
            return redirect(currentroute)

def exportDescriptor(request, nextroute):
    if request.method == 'POST':
        return redirect(nextroute)

def getSeeds(request, nextroute):
    if request.method == 'POST':
        if request.form['skip'] == 'skip':
            v.privkeylist = generatePrivKeys(True)
        else:
            v.privkeylist = generatePrivKeys()
        (v.newxpublist, v.xprivlist) = getxprivs(v.privkeylist)
        v.addresses = []
        checksumSTR = None
        response = handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpriv getdescriptorinfo "wsh(multi(3,'+v.xprivlist[0]+'/*,'+v.xprivlist[1]+'/*,'+v.xprivlist[2]+'/*,'+v.xprivlist[3]+'/*,'+v.xprivlist[4]+'/*,'+v.xprivlist[5]+'/*,'+v.xprivlist[6]+'/*))"', True)
        checksumSTR = response["checksum"]
        v.pubdesc = response["descriptor"].replace('\n', '')
        desc = 'wsh(multi(3,'+v.xprivlist[0]+'/*,'+v.xprivlist[1]+'/*,'+v.xprivlist[2]+'/*,'+v.xprivlist[3]+'/*,'+v.xprivlist[4]+'/*,'+v.xprivlist[5]+'/*,'+v.xprivlist[6]+'/*))#'+checksumSTR
        handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpriv importdescriptors \'[{ "desc": "'+desc+'", "timestamp": "now", "active": true}]\'')
        v.walletimported = True
        path = home + '/Documents'
        for i in range(1,8):
            privkey = v.privkeylist[i-1]
            v.passphraselist = ConvertToPassphrase(privkey)
            subprocess.call('mkdir '+path+'/yetiseed'+str(i), shell=True)
            subprocess.call('touch '+path+'/yetiseed'+str(i)+'/yetiseed'+str(i)+'.txt', shell=True)
            file = ''
            phrasenum = 0
            for x in range(0,13):
                line = ""
                for y in range(0,4):
                    line = line + v.passphraselist[phrasenum] + ' '
                    phrasenum = phrasenum + 1
                line = line + checksum(line)
                file = file + line + '\n'
            file = file + '\n\nThis is your descriptor in text format you have a copy of this descriptor on both your yetiseed files and descriptor.txt files.\n' + v.pubdesc + '\n'
            file = file + v.coldfile
            createOrPrepend(file, path+'/yetiseed'+str(i)+'/yetiseed'+str(i)+'.txt')
        createOrPrepend(v.pubdesc, path+'/Descriptor.txt')
        return redirect(nextroute)

def displaySeeds(request, currentroute, nextroute):
    if request.method == 'GET':
        privkey = v.privkeylist[v.privkeycount]
        v.passphraselist = ConvertToPassphrase(privkey)
    if request.method == 'POST':
        v.privkeycount = v.privkeycount + 1
        if (v.privkeycount == 7):
            v.privkeycount = 0
            return redirect(nextroute)
        else:
            return redirect(currentroute)

def checkSeeds(request, currentroute, nextroute):
    if request.method == 'POST':
        if request.form['option'] == 'Skip':
            return redirect(nextroute)
        privkey = v.privkeylist[v.privkeycount]
        passphraselist = ConvertToPassphrase(privkey)
        passphraselisttoconfirm = []
        v.oldkeys = []
        for i in range(1,14):
            inputlist = request.form['row' + str(i)]
            v.oldkeys.append(inputlist)
            inputlist = inputlist.split(' ')
            inputlist = inputlist[0:4]
            passphraselisttoconfirm.append(inputlist[0])
            passphraselisttoconfirm.append(inputlist[1])
            passphraselisttoconfirm.append(inputlist[2])
            passphraselisttoconfirm.append(inputlist[3])
        if passphraselisttoconfirm == passphraselist:
            v.error = None
            v.privkeycount = v.privkeycount + 1
            if (v.privkeycount >= 7):
                return redirect(nextroute)
            else:
                v.oldkeys = []
                return redirect(currentroute)
        else:
            v.error = 'The seed words you entered are incorrect. This is probably because you entered a line twice or put them in the wrong order.'

def importSeeds(request, currentroute, nextroute):
    if request.method == 'GET':
        if v.walletimported:
            return redirect(nextroute)
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
        v.privkeylist.append(PassphraseListToWIF(privkey))
        error = None
        v.privkeycount = v.privkeycount + 1
        if (v.privkeycount >= 3):
            (v.newxpublist, v.xprivlist) = getxprivs(v.privkeylist)
            v.privkeycount = 0
            xpublist = v.pubdesc.split(',')[1:]
            xpublist[6] = xpublist[6].split('))')[0]
            descriptorlist = xpublist
            for i in range(0,3):
                xpub = v.newxpublist[i] + '/*'
                for x in range(0,7):
                    oldxpub = xpublist[x]
                    if xpub == oldxpub:
                        descriptorlist[x] = (v.xprivlist[i] + '/*')
                        break
            desc = '"wsh(multi(3,'+descriptorlist[0]+','+descriptorlist[1]+','+descriptorlist[2]+','+descriptorlist[3]+','+descriptorlist[4]+','+descriptorlist[5]+','+descriptorlist[6]+'))'
            response = handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpriv getdescriptorinfo '+desc+'"', True)
            checksum = response["checksum"]
            handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpriv importdescriptors \'[{ "desc": '+desc+'#'+ checksum +'", "timestamp": "now", "active": true}]\'')
            handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpriv rescanblockchain '+blockheight())
            return redirect(nextroute)
        else:
            return redirect(currentroute)