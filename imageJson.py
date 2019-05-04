import os
import json
import base64


path = "./static/cc/"
path1 = "./static/stroke/"

curl = "https://frozen-badlands-62690.herokuapp.com/static/"

names = []


for file in os.listdir(path):
    names.append(file)

print(names)

letters = []

# with open("./static/cc/bu.png", "rb") as f:
#     data = f.read()
#     encoded_string = base64.b64encode(data)
#
# print(encoded_string)



def lettersToJson(id, name, url1, p):

    u1 = curl + "cu/" + url1 + ".png"
    u2 = curl + "stroke/" + url1 + ".gif"
    pathu = p + name

    letter = {id: {
        "id":id,
        "name":name,
        "static":u1,
        "gif":u2,
        "path":pathu
     }}

    return letter


for i in range(len(names)):
    letters.append(lettersToJson(i, names[i].strip(".png"), names[i].strip(".png"), path))


with open('./packages/Flags.json', 'w') as f:
    json.dump(letters, f)


print(letters)