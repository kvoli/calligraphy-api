import requests

url = "https://frozen-badlands-62690.herokuapp.com/packages/upload"
file = "static/cc/bu.png"


with open(file, 'rb') as f:
    requests.post(url, data=f)


