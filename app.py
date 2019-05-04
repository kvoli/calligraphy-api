from flask import Flask, render_template, request, redirect, url_for
import os, json, boto3
import uuid
import base64
import time
from flask_request_params import bind_request_params

app = Flask(__name__, static_folder='static')

arr = []

with open('./graffite/streetart.json','r') as jsonfile:
    file_data = json.loads(jsonfile.read())
    arr = file_data

@app.route('/')
def index():
    return render_template('index.html')


# We're using the new route that allows us to read a date from the URL
@app.route('/street-art/<name>/<query>')
def get_data_specific(name=None, query=None):
    return json.dumps(arr[0][name][query])


@app.route('/street-art/<name>')
def get_data_name(name=None):
    return json.dumps(arr[0][name])


@app.route('/street-art', methods = ['GET', 'POST'])
def get_data():
    if request.method == 'GET':
      return json.dumps(arr)
    else:

      # generate a unique id
      uid = str(uuid.uuid4())
      # generate image url
      path = './static/' + uid + '.jpg'
      # decode and save the image
      url = 'https://graffite-api.herokuapp.com/static/' + uid + '.jpg'

      imageData = request.get_data()

      imgdata = base64.b64decode(imageData)
      with open(path, 'wb') as f:
          f.write(imgdata)

      # create the json object from the post paramaters
      artObject = {uid: {
        "id":uid,
        "name":request.args['name'],
        "latitude":request.args['latitude'],
        "longitude":request.args['longitude'],
        "description":request.args['description'],
        "time_created":int(time.time()),
        "rating":7,
        "image_url":url
      }}
    

      arr.append(artObject)

      return json.dumps(json.dumps(artObject))


if __name__ == '__main__': app.run(debug=True)