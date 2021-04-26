import cv2
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from PIL import Image
import pytesseract
import base64
import time
import numpy as np
import os

app = FastAPI()


class Item(BaseModel):
    base64: str
    lang: str


@app.get('/')
def hello_world():
    return 'Hello World !'


@app.post('/getImage')
def getImage(item: Item):
    print(item.lang)
    timestamp = str(time.time() * 1000)
    print("create tmp file from base64")
    fh = open("tmp\\imageToSave_" + timestamp + ".png", "wb")
    fh.write(base64.b64decode(item.base64))
    fh.close()

    # load the example image and convert it to grayscale
    print("compress picture to adapt")

    image = Image.open('tmp\\imageToSave_' + timestamp + '.png')
    image.save('tmp\\imageToSave_' + timestamp + '.png', quality=70)
    image = cv2.imread('tmp\\imageToSave_' + timestamp + '.png')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.medianBlur(image, 5)
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    image = deskew(image)
    cv2.imwrite('tmp\\output_' + timestamp + '.png', image, [int(cv2.IMWRITE_PNG_COMPRESSION), 6])

    # TAKE THESE 2 COMMENTS OUT IF YOU WANT TO TEST ON YOUR LOCAL MACHINE
    #tessconfig = r'--tessdata-dir "' + os.path.abspath(os.getcwd()) + r'\env" --oem 1 --psm 1'
    print("read content ...")
    #text = pytesseract.image_to_string(Image.open("tmp\\output_" + timestamp + ".png"), lang=item.lang, config=tessconfig)
    text = pytesseract.image_to_string(Image.open("tmp\\output_" + timestamp + ".png"), lang=item.lang, config="--oem 1 --psm 1")

    # text = pytesseract.image_to_string(Image.open('output.png'), lang="deu")
    print("remove tmp files")
    os.remove("tmp\\output_" + timestamp + ".png")
    os.remove("tmp\\imageToSave_" + timestamp + ".png")
    return text


def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
