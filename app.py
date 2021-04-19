from flask import Flask, request
from PIL import Image
import pytesseract
import base64
#import cv2
import os
import numpy as np
from skimage import io
from skimage.color import rgb2gray
from skimage.transform import rotate
from deskew import determine_skew
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World !'

@app.route('/getImage', methods=['POST'])
def getImage():
    fh = open("imageToSave.png", "wb")
    fh.write(base64.b64decode(request.get_data()))
    fh.close()
    # load the example image and convert it to grayscale

    image = io.imread('imageToSave.png')
    grayscale = rgb2gray(image)
    angle = determine_skew(grayscale)
    rotated = rotate(image, angle, resize=True) * 255
    io.imsave('output.png', rotated.astype(np.uint8))

    #image = cv2.imread('imageToSave.png')
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # check to see if we should apply thresholding to preprocess the
    # image
    pathname = os.path.abspath(os.getcwd()) + r"\env"

    #gray = cv2.threshold(gray, 0, 255,
     #                        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    #filename = "{}.png".format(os.getpid())
    #cv2.imwrite(filename, gray)
    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file#

    # TAKE THESE 2 COMMENTS OUT IF YOU WANT TO TEST ON YOUR LOCAL MACHINE
    #tessconfig = r'--tessdata-dir "' + os.path.abspath(os.getcwd()) + '\env"'
    #text = pytesseract.image_to_string(Image.open(filename), lang="deu", config=tessconfig)

    text = pytesseract.image_to_string(Image.open('output.png'), lang="deu")
    os.remove('output.png')
    print(text)
    return text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
