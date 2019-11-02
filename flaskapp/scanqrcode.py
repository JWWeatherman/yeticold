import cv2
from pyzbar.pyzbar import decode
from PIL import Image
cam = cv2.VideoCapture(0)
cv2.namedWindow("qrcodescaner")
while True:
    k = cv2.waitKey(1)
    ret, frame = cam.read()
    if not ret:
        break
    cv2.imshow("qrcodescaner", frame)
    img_name = "qrcodeimage.png"
    cv2.imwrite(img_name, frame)
    decodepng = decode(Image.open('qrcodeimage.png'))
    if decodepng:
        firstqrcode = decodepng[0].data
        break
cam.release()
cv2.destroyAllWindows()
print(firstqrcode.decode("utf-8"))
