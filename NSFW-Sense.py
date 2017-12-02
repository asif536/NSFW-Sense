from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import json
import requests

app = ClarifaiApp(api_key='ec6402c259dc42a5a0d8d48b1e121cad')

model = app.models.get('nsfw-v1.0')
image = ClImage(url='https://pbs.twimg.com/media/BFG-BCSCMAA7sF9.jpg')
response = model.predict([image])

concepts = response['outputs'][0]['data']['concepts']
for concept in concepts:
	if concept["name"] == "sfw":
		sfw_val = concept["value"]
	if concept["name"] == "nsfw":
		nsfw_val = concept["value"]
#print(concept['name'], concept['value'])
    
print("sfw: ", sfw_val)
print("nsfw: ", nsfw_val)
data = {
	"type": "bulk",
	"args": [
		{
			"type": "delete",
			"args": {
				"table": "clarifai_nsfw",
				"where": {}
			}
		},
		{
			"type": "insert",
			"args": {
				"table": "clarifai_nsfw",
				"objects": [
					{
						"sfw": sfw_val,
						"nsfw": nsfw_val
					}
				]
			}
		}
	]
}

request = requests.post("https://data.alliance84.hasura-app.io/v1/query", data=json.dumps(data))

print(request.json())

