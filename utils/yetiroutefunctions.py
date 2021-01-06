from imports import *
import variables as v
from yetifunctions import *
from btcrpcfunctions import *
from formating import *
home = os.getenv("HOME")

def blockChain(request, nextroute, mode):
    if request.method == 'GET':
        if (os.path.exists(home + "/.bitcoin")) or mode == 'YetiLevelThreePrimaryLoad' or mode == 'YetiLevelTwoLoad' or mode == 'YetiLevelOneLoad':
            createOrPrepend('\nserver=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword='+v.rpcpsw+'\n',home+'/.bitcoin/bitcoin.conf')
            return redirect(nextroute)
        else:
            subprocess.call('mkdir ~/.bitcoin',shell=True)
        if mode == 'YetiLevelThreePrimaryCreate' or mode == 'YetiLevelTwoCreate' or mode == 'YetiLevelOneCreate':
            createOrPrepend('\nserver=1\nrpcport=8332\nrpcuser=rpcuser\nprune=550\nrpcpassword='+v.rpcpsw+'\n',home+'/.bitcoin/bitcoin.conf')
            return redirect(nextroute)
    if request.method == 'POST':
        subprocess.call('mkdir ~/.bitcoin',shell=True)
        if request.form['option'] == 'Skip':
            createOrPrepend('\nserver=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword='+v.rpcpsw+'\n',home+'/.bitcoin/bitcoin.conf')
            return redirect(nextroute)
        createOrPrepend('server=1\nrpcport=8332\nrpcuser=rpcuser\nprune='+str(getPrunBlockheightByDate(request.form['date']))+'\nrpcpassword='+v.rpcpsw+'',home+'/.bitcoin/bitcoin.conf')
        return redirect(nextroute)

def openBitcoin(request, currentroute, nextroute, mode, yeti='Warm'):
    if request.method == 'GET':
        v.IBD = BTCFinished()
        v.progress = BTCprogress()
        if not os.path.exists(home + "/.bitcoin/bitcoind.pid"):
            subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-qt -proxy=127.0.0.1:9050',shell=True,start_new_session=True)
        if mode == 'YetiLevelThreeSecondaryCreate' or mode == 'YetiLevelThreeSecondaryRecover' or mode == 'YetiLevelThreeSecondaryLoad':
            response = subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-cli getblockchaininfo', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            if response[1] == b'':
                v.IBD = True
    if request.method == 'POST':
        if v.IBD:
            if mode == 'YetiLevelThreePrimaryCreate' or mode == 'YetiLevelThreePrimaryRecover':
                handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetiwalletpub" true true "" false true')
            elif mode == 'YetiLevelThreePrimaryLoad':
                handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli loadwallet "yetiwalletpub"')
            elif mode == 'YetiLevelThreeSecondaryCreate' or mode == 'YetiLevelThreeSecondaryRecover' or mode == 'YetiLevelTwoCreate' or mode == 'YetiLevelTwoRecover':
                handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetiwalletpriv" false true "" false true')
            elif mode == 'YetiLevelThreeSecondaryLoad' or mode == 'YetiLevelTwoLoad':
                handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli loadwallet "yetiwalletpriv"')
            elif mode == 'YetiLevelOneCreate' or mode == 'YetiLevelOneRecover':
                handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetiwallethot" false true')
            elif mode == 'YetiLevelOneLoad':
               handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli loadwallet "yetiwallethot"') 
            return redirect(nextroute)
        else:
            return redirect(currentroute)

def scanDescriptor(request, currentroute, nextroute, offline=True):
    if request.method == 'POST':
        v.error = None
        v.pubdesc = request.form['descriptor'].replace('\n','')
        if offline:
            response = subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpriv getdescriptorinfo "'+v.pubdesc+'"', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        else:
            response = subprocess.Popen('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpub getdescriptorinfo "'+v.pubdesc+'"', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(response, 'response for function: check descriptor')
        if response[1] != b'':
            v.error = 'Invalid Descriptor: '+v.pubdesc
            return redirect(currentroute)
        if offline:
            handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpriv importdescriptors \'[{ "desc": "'+v.pubdesc+'", "timestamp": "now", "active": true}]\'')
        else:
            handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpub importdescriptors \'[{ "desc": "'+v.pubdesc+'", "timestamp": "now", "active": true}]\'')
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
            subprocess.call('touch '+path+'/yetiseed'+str(i)+'.txt', shell=True)
            file = ''
            phrasenum = 0
            for x in range(0,13):
                line = ""
                for y in range(0,4):
                    line = line + v.passphraselist[phrasenum] + ' '
                    phrasenum = phrasenum + 1
                line = line + checksum(line)
                file = file + line + '\n'
            file = file + '\n \n' + v.pubdesc + '\n\n'
            SeedT = readFile(home+'/yeticold/templates/SeedTemplate.txt')
            for z in range(0, len(SeedT)):
                file = file + SeedT[i] + '\n'
            createOrPrepend(file, path+'/yetiseed'+str(i)+'.txt')
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

def checkSeeds(request, currentroute, nextroute, yeti="Cold"):
    if request.method == 'POST':
        if request.form['option'] == 'Skip':
            return redirect(nextroute)
        privkey = v.privkeylist[v.privkeycount]
        passphraselist = ConvertToPassphrase(privkey)
        passphraselisttoconfirm = []
        v.oldkeys = []
        if yeti == 'Warm':
            desctoconfirm = request.form['descriptor'].replace('\n','')
            if notdesctoconfirm == v.pubdesc:
                v.error = 'The descriptor contained in this seed file was found to be incorrect.'
                return redirect(currentroute)
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