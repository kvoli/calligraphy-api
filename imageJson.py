import os
import json


path = "./static/cc/"
path1 = "./static/stroke/"

curl = "https://frozen-badlands-62690.herokuapp.com/static/"

names = []


for file in os.listdir(path):
    names.append(file)

print(names)

letters = []


def lettersToJson(id, name, url1):

    u1 = curl + "cc/" + url1 + ".png"
    u2 = curl + "stroke/" + url1 + ".gif"

    letter = {id: {
        "id":id,
        "name":name,
        "static":u1,
        "gif":u2
     }}

    return letter


for i in range(len(names)):
    letters.append(lettersToJson(i,names[i].strip(".png"), names[i].strip(".png")))


with open('./packages/chinese.json', 'w') as f:
    json.dump(letters, f)


print(letters)