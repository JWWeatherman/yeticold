#from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
#
#wallet_template = "http://{rpc_username}:{rpc_password}@{rpc_host}:{rpc_port}/wallet/{wallet_name}"
#settings = {
#      "rpc_username": "rpcuser",
#    "rpc_password": "somesecretpassword",
#    "rpc_host": "127.0.0.1",
#    "rpc_port": 8332,
#    "address_chunk": 100
#}
#name = 'username'
#wallet_name = ''
#uri = wallet_template.format(**settings, wallet_name=wallet_name)
#rpc = AuthServiceProxy(uri, timeout=600)  # 1 minute timeout
#adr = rpc.getnewaddress()
#privkey = rpc.dumpprivkey(adr)
#print(privkey)



#pip install pypng
#pip install zbar
#pip install pillow
#pip install qrtools
#pip install qrcode
#pip install pyzbar
#brew install python3-opencv

# qr = qrcode.QRCode(
#    version=1,
#    error_correction=qrcode.constants.ERROR_CORRECT_L,
#    box_size=10,
#    border=4,
# )
# qr.add_data('Some data')
# qr.make(fit=True)

# img = qr.make_image(fill_color="black", back_color="white")
# img.save('test.jpg')
# decodepng = decode(Image.open('test.jpg'))
# print(decodepng[0].data)
# webcam = QR()
# print(webcam.decode_webcam())

# decodepng = decode(Image.open('filename.jpg'))
# print(decodepng[0].data)




# cv2.destroyAllWindows()

# import subprocess
# import os

# subprocess.Popen("ls", cwd=os.path.expanduser('~
import cv2
from qrtools.qrtools import QR
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode
global secondqrcode
import time
cam = cv2.VideoCapture(0)
cv2.namedWindow("qrcode2")
img_counter = 0
qrcode_counter = 0
pause = 0
while True:
    if qrcode_counter == 3:
        break
    k = cv2.waitKey(1)
    if k == 13:
        pause = 0
    if not pause == 1 :
        ret, frame = cam.read()
        cv2.imshow("qrcode2", frame)
        if not ret:
            break
        img_counter = img_counter + 1
        if img_counter >= 100:
            img_counter = 0
            img_name = "qrcodeimage.png"
            cv2.imwrite(img_name, frame)
            decodepng = decode(Image.open('qrcodeimage.png'))
            if decodepng:
                pause = 1
                qrcode_counter = qrcode_counter + 1
                if qrcode_counter == 1:
                    firstqrcode = decodepng[0].data
                elif qrcode_counter == 2:
                    secondqrcode = decodepng[0].data
                elif qrcode_counter == 3:
                    thirdqrcode = decodepng[0].data
                
cam.release()
cv2.destroyAllWindows()

######### RANDOM CODE STOP /\


#add multisig address as an watch only







#### LIST OF THINGS TO DO IN ORDER







