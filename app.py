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

app = Flask(__name__, static_folder='static')


instance_storage = defaultdict(list)

path_to_packages = './packages/'

for file in os.listdir(path_to_packages):
    file_path = "%s/%s" % (path_to_packages, file)
    with open(file_path, 'r') as jsonfile:
        file_data = json.loads(jsonfile.read())
        instance_storage[file] = file_data


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/packages/<package>/<id>')
def get_package_object(package=None, id=None):
    return json.dumps(instance_storage[package][int(id)])


@app.route('/packages/<package>')
def get_package(package=None):
    return json.dumps(instance_storage[package])


@app.route('/packages/', methods=['GET', 'POST'])
def get_data():
    if request.method == 'GET':
        return json.dumps(instance_storage.values())
    else:
        # generate a unique id
        uid = str(uuid.uuid4())
        # generate image url
        path = './static/' + uid + '.jpg'
        # decode and save the image
        url = 'https://frozen-badlands-62690.herokuapp.com/static/' + uid + '.jpg'

        # data = json.dumps(request.json)

        # image_data = data["img"]
        # name = data["name"]
        # package = data["package"]

        data = request.get_data()

        print(data)

        imgdata = base64.b64decode(data)
        with open(path, 'wb') as f:
            f.write(imgdata)

        # create the json object from the post paramaters
        # new = {uid: {
        #     "id": uid,
        #     "name": name,
        #     "image_url": url
        #     }}

        # instance_storage[package].append(new)

        # return json.dumps(json.dumps(new))
        return url


app.route("/upload", methods=['POST'])
def upload_file():
    def custom_stream_factory(total_content_length, filename, content_type, content_length=None):
        import tempfile
        tmpfile = tempfile.NamedTemporaryFile('wb+', prefix='flaskapp', suffix='.nc')
        app.logger.info("start receiving file ... filename => " + str(tmpfile.name))
        return tmpfile
    sim = 0
    import werkzeug, flask
    stream, form, files = werkzeug.formparser.parse_form_data(flask.request.environ, stream_factory=custom_stream_factory)
    for fil in files.values():
        app.logger.info(" ".join(["saved form name", fil.name, "submitted as", fil.filename, "to temporary file", fil.stream.name]))
        sim = imageSimilarity(fil.stream.name, "static/cc/bu.png")
    return sim


def imageSimilarity(ref1, ref2):
    # load the two input images
    imageA = cv2.imread(ref2, cv2.IMREAD_UNCHANGED)
    imageB = cv2.imread(ref1, cv2.IMREAD_UNCHANGED)

    width = 350
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
    return {"sim": str(score), "diff": str(diff)}


if __name__ == '__main__': app.run(debug=True)