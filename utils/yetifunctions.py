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

def generatePrivKeys(genbinary=False):
    privkeylisttemp = []
    for i in range(1,8):
        if genbinary:
            newbinary = str('1') * 256
        else:
            newbinary = request.form['binary' + str(i)]
        adr = handleResponse('bitcoin-cli -rpcwallet= getnewaddress')
        print(adr)
        newprivkey =  handleResponse('bitcoin-cli -rpcwallet= dumpprivkey '+adr)
        print(newprivkey)
        binary = bin(decode58(newprivkey))[	2:][8:-40]
        WIF = ConvertToWIF(xor(binary,newbinary))
        privkeylisttemp.append(WIF)
    return privkeylisttemp

def getxprivs(privkeylist):  
    v.xpublist = []
    v.xprivlist = []
    for i in range(0,len(privkeylist)):
        xpriv = BIP32.from_seed(b58decode(privkeylist[i])[1:33]).get_master_xpriv()
        v.xprivlist.append(xpriv)
        response = handleResponse('bitcoin-cli -rpcwallet=yetiwallet getdescriptorinfo "pk('+xpriv+')"')
        xpub = response.split('(')[1].split(')')[0]
        v.xpublist.append(xpub)  
    return (v.xpublist, v.xprivlist)

def createDumpWallet():
	v.dumpwalletindex = v.dumpwalletindex + 1
	return '"yetixprivwallet'+str(v.dumpwalletindex)+'"'

def makeQrCode(data, path=None, name=None):
    if path == None:
        randomnum = str(random.randrange(0,1000000))
        path = home+'/yeticold/static/qrcode'+randomnum+'.png'
        name = 'qrcode'+randomnum+'.png'
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
    if name != None:
        return url_for('static', filename=name)

def handleResponse(func, returnJsonResponse=False, decode=True):
    response = subprocess.Popen(func, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print(response, "response for function: " + func)
    if response[1] != b'':
        raise werkzeug.exceptions.InternalServerError(response[1].decode("utf-8") + ". response for function: " + func)
    else:
        if returnJsonResponse:
            return json.loads(response[0].decode("utf-8"))
        elif (decode):
            return response[0].decode("utf-8")
        else:
            return response[0]