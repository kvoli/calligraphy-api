import requests, base64, json

url = "https://frozen-badlands-62690.herokuapp.com/packages/chinese.json"

with open("./static/cc/bu.png", "rb") as f:
    data = f.read()
    encoded_string = base64.b64encode(data)

r = requests.post(url=url, data={"name": "test", "img": encoded_string})
