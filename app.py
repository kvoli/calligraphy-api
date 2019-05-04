from flask import Flask, render_template, request, redirect, url_for
from collections import defaultdict
import os, json, boto3
import uuid
import base64
import time
from flask_request_params import bind_request_params
# import the necessary packages
from skimage.measure import compare_ssim
import argparse
import imutils
import cv2
import random

app = Flask(__name__, static_folder='static')


instance_storage = defaultdict(list)

path_to_packages = './packages/'

for file in os.listdir(path_to_packages):
    file_path = "%s/%s" % (path_to_packages, file)
    with open(file_path, 'r') as jsonfile:
        file_data = json.loads(jsonfile.read())
        instance_storage[file] = file_data


def imageSimilarity(ref1, ref2):
    # load the two input images
    imageA = cv2.imread(ref2, cv2.IMREAD_UNCHANGED)
    imageB = cv2.imread(ref1, cv2.IMREAD_UNCHANGED)

    width = 450
    height = 450
    dim = (width, height)

    # resize image
    imageA = cv2.resize(imageA, dim, interpolation=cv2.INTER_AREA)
    imageB = cv2.resize(imageB, dim, interpolation=cv2.INTER_AREA)

    # resize

    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    return {"sim": str(score)}


def lettersToJson(name, url):
    curl = "./static/cc/"
    res = curl + "cu/" + url + ".png"

    letter = {id: {
        "id": str(len(instance_storage)),
        "name": str(name),
        "static": str(res),
        "gif": "N/A"
     }}

    return letter


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/packages/<package>/<id>')
def get_package_object(package=None, id=None):
    return json.dumps(instance_storage[package][int(id)])


@app.route('/packages/<package>')
def get_package(package=None):
    return json.dumps(instance_storage[package])


@app.route('/up', methods=['GET', 'POST'])
def get_data():
    if request.method == 'GET':
        return json.dumps(instance_storage)
    else:
        # generate a unique id
        uid = str(uuid.uuid4())
        # generate image url
        path = './static/' + uid + '.png'
        # decode and save the image
        url = 'https://frozen-badlands-62690.herokuapp.com/static/' + uid + '.png'

        # {"package": "<insert-package>", "id": "<insert-id>", "b64": "<b64encoded>"}
        data = request.get_data()
        imageData = data["b64"]
        path = instance_storage[data["package"]][0][data["id"]]["path"] + '.png'
        imgdata = base64.b64decode(imageData)
        with open(path, 'wb') as f:
            f.write(imgdata)

        print(url)

        return json.dumps(imageSimilarity(url, path))


@app.route('/put', methods=['GET', 'POST'])
def up_data():
    if request.method == 'GET':
        return json.dumps(instance_storage)
    else:
        # generate a unique id
        uid = str(uuid.uuid4())
        # generate image url
        path = './static/' + uid + '.png'
        # decode and save the image
        url = 'https://frozen-badlands-62690.herokuapp.com/static/' + uid + '.png'

        imageData = request.get_data()

        imgdata = base64.b64decode(imageData)
        with open(path, 'wb') as f:
            f.write(imgdata)

        res = lettersToJson("name", url)

        instance_storage["chinese.json"].append(res)

        print(url)

        return json.dumps({"url": str(url)})


@app.route('/sim')
def get_sim():
    return str(random.random()*40+60)


if __name__ == '__main__': app.run(debug=True)