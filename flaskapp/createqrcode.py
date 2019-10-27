from qrtools.qrtools import QR
from pyzbar.pyzbar import decode
from PIL import Image
import os
import qrcode
data = input("input data ")
name = input("name to save ")
qr = qrcode.QRCode(
       version=1,
       error_correction=qrcode.constants.ERROR_CORRECT_L,
       box_size=10,
       border=4,
)
qr.add_data(data)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
home = os.getenv("HOME")
img.save(home + '/Desktop/' + name + '.png')