import requests, base64, json
from urllib.request import urlopen

url = "https://frozen-badlands-62690.herokuapp.com/upload"
file = "static/fed.png"


import os
with open(file, 'rb') as f:
    t = f.read()
    # print(t)
    x = base64.b64encode(t)

    y = {"package": "chinese.json", "id": "0", "b64": x}
    print(y)
    out = requests.post('https://frozen-badlands-62690.herokuapp.com/put', data=y)

    print(out.status_code, out.text)


# print(out)
# image = open('deer.gif', 'rb')
# read = image.read()
# image_64_encode = base64.encodebytes(image_read)