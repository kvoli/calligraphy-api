from flask import Flask, render_template, request, redirect, url_for
from collections import defaultdict
import os, json, boto3
import uuid
import base64
import time
from flask_request_params import bind_request_params

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


@app.route('/packages/<package>/', methods = ['GET', 'POST'])
def get_data(package=None):
    if request.method == 'GET':
        return json.dumps(instance_storage.values())
    else:
        # generate a unique id
        uid = str(uuid.uuid4())
        # generate image url
        path = './static/' + package + '/' + uid + '.jpg'
        # decode and save the image
        url = 'https://frozen-badlands-62690.herokuapp.com/static/' + uid + '.jpg'

        data = request.get_data()

        imageData = data["img"]
        name = data["name"]

        imgdata = base64.b64decode(imageData)
        with open(path, 'wb') as f:
            f.write(imgdata)

        # create the json object from the post paramaters
        new = {uid: {
            "id": uid,
            "name": name,
            "image_url": url
            }}

        instance_storage[package].append(new)

        return json.dumps(json.dumps(new))


if __name__ == '__main__': app.run(debug=True)