from imports import *
import variables as v
from yetifunctions import *
from btcrpcfunctions import *
from formating import *
home = os.getenv("HOME")

def blockChain(request, nextroute):
    if request.method == 'GET':
        if (os.path.exists(home + "/.bitcoin")):
            createOrPrepend('\nserver=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword='+v.rpcpsw+'\n',home+'/.bitcoin/bitcoin.conf')
            return redirect(nextroute)
    if request.method == 'POST':
        subprocess.call('mkdir ~/.bitcoin',shell=True)
        if request.form['date'] == '':
            createOrPrepend('\nserver=1\nrpcport=8332\nrpcuser=rpcuser\nrpcpassword='+v.rpcpsw+'\n',home+'/.bitcoin/bitcoin.conf')
            return redirect(nextroute)
        createOrPrepend('server=1\nrpcport=8332\nrpcuser=rpcuser\nprune='+str(getPrunBlockheightByDate(request))+'\nrpcpassword='+v.rpcpsw+'',home+'/.bitcoin/bitcoin.conf')
        return redirect(nextroute)

def openBitcoin(request, currentroute, nextroute, loadwallet=False, offline=False, yeti='warm'):
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
                if yeti == 'cold' and not offline:
                    handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli loadwallet "yetiwalletpub"')
                elif yeti == 'hot':
                    handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli loadwallet "yetiwallethot"')
                else:
                    handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli loadwallet "yetiwalletpriv"')
            else:
                if yeti == 'cold' and not offline:
                    handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetiwalletpub" true true "" false true')     
                elif yeti == 'hot':
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
        subprocess.call('rm -r '+path+'/yetiseed*', shell=True)
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

# def displaywallet(request, nextroute):
#     if request.method == 'GET':
#         v.addresses = []
#         v.totalwalletbal = 0
#         subprocess.call(['rm -r ~/yeticold/static/qrcode*'],shell=True)
#         adrlist = handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwallet deriveaddresses "'+v.pubdesc+'" "[0,999]"', True)
#         rpc = RPC("yetiwallet")
#         for i in range(0, len(adrlist)):
#             adr = adrlist[i]
#             randomnum = str(random.randrange(0,1000000))
#             route = url_for('static', filename='qrcode'+adr+''+randomnum+'.png')
#             response = rpc.listunspent(0, 9999999, [adr])
#             if response == []:
#                 rpc.importaddress(adrlist[i], "", False)
#                 totalbal = rpc.getreceivedbyaddress(adrlist[i])
#                 if totalbal:
#                     status = 3
#                 else:
#                     status = 0
#                 address = {}
#                 address['txid'] = ''
#                 address['address'] = adr
#                 address['balance'] = "0.00000000"
#                 address['numbal'] = 0
#                 address['status'] = status
#                 address['route'] = route
#                 v.addresses.append(address)
#             else:
#                 for x in range(0, len(response)):
#                     utxo = response[x]
#                     txid = utxo['txid']
#                     vout = utxo['vout']
#                     scriptPubKey = utxo['scriptPubKey']
#                     amount = "{:.8f}".format(float(utxo['amount']))
#                     numamount = float(amount)
#                     v.totalwalletbal = v.totalwalletbal + numamount
#                     confs = utxo['confirmations']
#                     totalbal = rpc.getreceivedbyaddress(adr)
#                     if numamount:
#                         if not confs:
#                             status = 1
#                         else:
#                             status = 2
#                     elif totalbal:
#                         status = 3
#                     else:
#                         status = 0
#                     address = {}
#                     address['txid'] = txid
#                     address['vout'] = vout 
#                     address['scriptPubKey'] = scriptPubKey
#                     address['address'] = adr
#                     address['balance'] = amount
#                     address['numbal'] = numamount
#                     address['status'] = status
#                     address['route'] = route
#                     v.addresses.append(address)
#         v.addresses.sort(key=lambda x: x['balance'], reverse=True)
#         for i in range(0, len(v.addresses)):
#             makeQrCode(v.addresses[i]['address'], home+'/yeticold/'+v.addresses[i]['route'])
#     if request.method == 'POST':
#         for i in range(0, len(v.addresses)):
#             if v.addresses[i]['txid'] == request.form['txid']:
#                 v.selectedutxo = v.addresses[i]
#         return redirect(nextroute)

# def scanrecipent(request, currentroute, nextroute):
#     if request.method == 'POST':
#         v.error = None
#         if request.form['option'] == 'scan':
#             v.receipentaddress = handleResponse('python3 ~/yeticold/utils/scanqrcode.py').replace('\n', '')
#             return redirect(currentroute)
#         else:
#             v.receipentaddress = request.form['option']
#         if (v.receipentaddress.split(':')[0] == 'bitcoin'):
#             v.receipentaddress = v.receipentaddress.split(':')[1].split('?')[0]
#         if (v.receipentaddress[:3] == 'bc1') or (v.receipentaddress[:1] == '3') or (v.receipentaddress[:1] == '1'):
#             if not (len(v.receipentaddress) >= 26) and (len(v.receipentaddress) <= 35):
#                 v.error = v.receipentaddress + ' is not a valid bitcoin address, address should have a length from 26 to 35 instead of ' + str(len(v.receipentaddress)) + '.'
#         else: 
#             v.error = v.receipentaddress + ' is not a valid bitcoin address, address should have started with bc1, 3 or 1 instead of ' + v.receipentaddress[:1] + ', or ' + v.receipentaddress[:3] + '.'
#         if v.error:
#             return redirect(currentroute)
#         return redirect(nextroute)

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

# def setFee(request, currentroute, nextroute):
#     if request.method == 'GET':
#         rpc = RPC("yetiwallet")
#         v.amount = "{:.8f}".format(float(v.selectedutxo['numbal']))
#         v.minerfee = float(rpc.estimatesmartfee(1)["feerate"])
#         kilobytespertrans = 0.200
#         v.minerfee = (v.minerfee * kilobytespertrans)
#         v.amo = "{:.8f}".format(float(v.selectedutxo['numbal']) - v.minerfee)
#     if request.method == 'POST':
#         v.minerfee = request.form['fee']
#         v.amo = "{:.8f}".format(float(v.selectedutxo['numbal']) - float(v.minerfee))
#         return redirect(nextroute)

# def sendTransaction(request, currentroute, nextroute):
#     if request.method == 'GET':
#         createTransactions()
#     if request.method == 'POST':
#         handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpriv sendrawtransaction '+v.transnum['hex']+'')
#         return redirect(nextroute)

# def createPSBT():
#     response = handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpriv createrawtransaction \'[{ "txid": "'+v.selectedutxo['txid']+'", "vout": '+str(v.selectedutxo['vout'])+'}]\' \'[{"'+v.receipentaddress+'" : '+str(v.amo)+'}]\'')
#     transhex = response[:-1]
#     psbt = handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpriv converttopsbt '+transhex)
#     response = handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpriv walletprocesspsbt '+psbt, True)
#     v.psbt = response['psbt']

# def signPSBT():
#     response = handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpriv walletprocesspsbt'+v.psbt, True)
#     if not response['complete']:
#         raise werkzeug.exceptions.InternalServerError(response['errors'][0]['error'])
#     v.psbt = response['psbt']
#     response = handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletpriv finalizepsbt'+v.psbt, True)
#     v.transhex = response['hex']




