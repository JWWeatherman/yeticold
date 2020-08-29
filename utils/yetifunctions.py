from imports import *
import variables as v
from btcrpcfunctions import *
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

def getPrunBlockheightByDate(request):
    fmt = '%Y-%m-%d %H:%M:%S'
    today = str(datetime.today()).split('.')[0]
    d1 = datetime.strptime(request.form['date'] + ' 12:0:0', fmt)
    d2 = datetime.strptime(today, fmt)
    d1_ts = time.mktime(d1.timetuple())
    d2_ts = time.mktime(d2.timetuple())
    diff = (int(d2_ts - d1_ts) / 60) / 10
    add = diff / 10
    blockheight = diff + add + 550
    blockheight = int(blockheight)

def generatePrivKeys(newbinary):
    privkeylisttemp = []
    for i in range(1,8):
        rpc = RPC()
        adr = rpc.getnewaddress()
        newprivkey = rpc.dumpprivkey(adr)
        binary = bin(decode58(newprivkey))[	2:][8:-40]
        WIF = ConvertToWIF(xor(binary,newbinary))
        privkeylisttemp.append(WIF)
    return privkeylisttemp

def getxprivs(privkeylist):  
    v.xpublist = []
    v.xprivlist = []
    for i in range(0,len(privkeylist)):
        handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli createwallet "yetixprivwallet'+str(i)+'"')
        handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetixprivwallet'+str(i)+' sethdseed true "'+v.privkeylist[i]+'"')
        handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetixprivwallet'+str(i)+' dumpwallet "yetixprivwallet'+str(i)+'"')
        wallet = open(home + '/yetixprivwallet' + str(i),'r')
        wallet.readline()
        wallet.readline()
        wallet.readline()
        wallet.readline()
        wallet.readline()
        v.xprivlist.append(wallet.readline().split(" ")[4][:-1])
        response = handleResponse('~/yeticold/bitcoin/bin/bitcoin-cli -rpcwallet=yetiwallet getdescriptorinfo "pk('+v.xprivlist[i]+')"')
        xpub = response.split('(')[1].split(')')[0]
        v.xpublist.append(xpub)  
    return (v.xpublist, v.xprivlist)

def makeQrCode(data, path=None, minipath=None):
    if path == None:
        randomnum = str(random.randrange(0,1000000))
        path = home+'/yeticold/static/qrcode'+randomnum+'.png'
        minipath = 'qrcode'+randomnum+'.png'
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(path)
    if minipath != None:
        return url_for('static', filename=minipath)

def handleResponse(func, returnJsonResponse=False):
    response = subprocess.Popen(func, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print(response, "response for function: " + func)
    if response[1] != b'':
        raise werkzeug.exceptions.InternalServerError(response[1].decode("utf-8") + ". response for function: " + func)
    else:
        if returnJsonResponse:
            return json.loads(response[0].decode("utf-8"))
        else:
            return response[0].decode("utf-8")