import requests, json
secondsThreshold = 120
APIKEY = "secret"
url = "https://maps.googleapis.com/maps/api/directions/json?origin=Disneyland&destination=Universal+Studios+Hollywood&key=" + APIKEY

# Using API Request
#response = requests.get(url)
#r = json.loads(response.text)

# Using Dummy Data
with open("./exampleResponse.json") as json_file:
    response = json.load(json_file)
r = response

steps = r["routes"][0]["legs"][0]["steps"]
stepBounds = []
for a in range(len(steps)):
    if steps[a]["duration"]["value"] > secondsThreshold:
        stepBounds.append([(steps[a]["start_location"]["lat"], steps[a]["start_location"]["lng"]) , (steps[a]["end_location"]["lat"], steps[a]["end_location"]["lng"])])

print (stepBounds)