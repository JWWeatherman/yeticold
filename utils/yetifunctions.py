from imports import *
from btcrpcfunctions import *
import variables as v
home = os.getenv("HOME")

def createOrPrepend(text, path):
    if (os.path.exists(path)):
        f = open(path,'r')
        temp = f.read()
        f.close()
        f = open(path, 'w')
        f.write(text)
        f.write(temp)
        f.close()
    else:
	    subprocess.call('echo "'+text+'" >> '+path, shell=True)

def erase():
    pw = str(random.getrandbits(256))
    file = "This is the first command:\n"
    file = file + "sudo hdparm -I /dev/sda\n"
    file = file + " \n"
    file = file + "This is the second command:\n"
    file = file + "sudo hdparm --user-master u --security-set-pass "+pw+" /dev/sda\n"
    file = file + " \n"
    file = file + "This is the third command:\n"
    file = file + "sudo time hdparm --user-master u --security-erase-enhanced "+pw+" /dev/sda\n"
    createOrPrepend(file, home+'/Documents/erase.txt')

def readFile(path):
    f = open(path,'r')
    temp = f.read()
    f.close()
    temp = temp.split('\n')
    result = []
    for i in range(0,len(temp)):
        result.append(temp[i])
    return result

def getPrunBlockheightByDate(date):
    fmt = '%Y-%m-%d %H:%M:%S'
    today = str(datetime.today()).split('.')[0]
    d1 = datetime.strptime(date + ' 12:0:0', fmt)
    d2 = datetime.strptime(today, fmt)
    d1_ts = time.mktime(d1.timetuple())
    d2_ts = time.mktime(d2.timetuple())
    diff = (int(d2_ts - d1_ts) / 60) / 10
    add = diff / 10
    blockheight = diff + add + 550
    print(blockheight)
    blockheight = int(blockheight)
    if blockheight < 25000:
        blockheight = 25000
    return blockheight

def generatePrivKeys(genbinary=False):
    handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetiwalletgen"')
    privkeylisttemp = []
    for i in range(1,8):
        if genbinary:
            newbinary = str('1') * 256
        else:
            newbinary = request.form['binary' + str(i)]
        adr = handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletgen getnewaddress')
        newprivkey =  handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletgen dumpprivkey '+adr)
        binary = bin(decode58(newprivkey))[	2:][8:-40]
        WIF = ConvertToWIF(xor(binary,newbinary))
        privkeylisttemp.append(WIF)
    handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli unloadwallet "yetiwalletgen"')
    return privkeylisttemp

def getxprivs(privkeylist):  
    handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetiwalletrec"')
    v.xpublist = []
    v.xprivlist = []
    for i in range(0,len(privkeylist)):
        xpriv = BIP32.from_seed(b58decode(privkeylist[i])[1:33]).get_master_xpriv()
        v.xprivlist.append(xpriv)
        response = handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwalletrec getdescriptorinfo "pk('+xpriv+')"')
        xpub = response.split('(')[1].split(')')[0]
        v.xpublist.append(xpub) 
    handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli unloadwallet "yetiwalletrec"')
    return (v.xpublist, v.xprivlist)

def createDumpWallet():
	v.dumpwalletindex = v.dumpwalletindex + 1
	return '"yetixprivwallet'+str(v.dumpwalletindex)+'"'

def checksum(fourwords):
    fourwords = fourwords.split(' ')
    fourwords.pop()
    WIFlist = PassphraseListToWIF(fourwords)
    sume = 0
    for char in WIFlist:
        decodenum = decode58(char)
        sume = sume + decodenum
    mod = sume % 58
    char = BASE58_ALPHABET[mod]
    char = ConvertToPassphrase(char)[0]
    return char


def handleResponse(func, returnJsonResponse=False, decode=True):
    response = subprocess.Popen(func, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print(response, "response for function: " + func)
    if response[1] != b'':
        raise werkzeug.exceptions.InternalServerError(response[1].decode("utf-8") + ". response for function: " + func)
    else:
        if returnJsonResponse:
            return json.loads(response[0].decode("utf-8").replace('\n',''))
        elif (decode):
            return response[0].decode("utf-8").replace('\n','')
        else:
            return response[0]