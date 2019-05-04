import requests, base64, json

url = "https://frozen-badlands-62690.herokuapp.com/packages/upload"
file = "static/cc/bu.png"


# with open("./static/cc/bu.png", "rb") as f:
#     data = f.read()
#     encoded_string = base64.b64encode(data)

with open(file, 'rb') as f:
    requests.post(url, data=f)


# r = requests.post(url=url, data=json.dumps({"name": "test", "img": encoded_string, "package": "chinese.json"}))

# r = requests.post(url=url, data=encoded_string)

# w = requests.get(url=url)

