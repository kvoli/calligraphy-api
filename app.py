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
    return json.dumps(instance_storage[package][id])


@app.route('/packages/<package>')
def get_package(package=None):
    return json.dumps(instance_storage[package])


# @app.route('/packages', methods = ['GET', 'POST'])
# def get_data():
    # if request.method == 'GET':
    #   return json.dumps(arr)
    # else:
    #
    #   # generate a unique id
    #   uid = str(uuid.uuid4())
    #   # generate image url
    #   path = './static/' + uid + '.jpg'
    #   # decode and save the image
    #   url = 'https://graffite-api.herokuapp.com/static/' + uid + '.jpg'
    #
    #   imageData = request.get_data()
    #
    #   imgdata = base64.b64decode(imageData)
    #   with open(path, 'wb') as f:
    #       f.write(imgdata)
    #
      # create the json object from the post paramaters
      # artObject = {uid: {
      #   "id":uid,
      #   "name":request.args['name'],
      #   "latitude":request.args['latitude'],
      #   "longitude":request.args['longitude'],
      #   "description":request.args['description'],
      #   "time_created":int(time.time()),
      #   "rating":7,
      #   "image_url":url
      # }}

    #
    #   arr.append(artObject)
    #
    #   return json.dumps(json.dumps(artObject))


if __name__ == '__main__': app.run(debug=True)