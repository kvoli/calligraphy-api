from flask import request
import json
import uuid

# class Image:

# 	Images = defaultdict()

# 	def __init__(self, id, url, name):
# 	self.id = id
# 	self.url = url
# 	self.name = name
# 	Images.append(self)

def lettersToJson():
	letters = []

	uid = str(uuid.uuid4())


     letter = {uid: {
        "id":uid,
        "name":request.args['name'],
        "url":url
     }}
    

     letters.append(letter)

     return json.dumps(json.dumps(letter))
