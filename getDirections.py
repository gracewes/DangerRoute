import requests, json, random

def crash_per_area(t1, t2):
    lat_1, lng_1 = t1
    lat_2, lng_2 = t2
    return random.random()

secondsThreshold = 120
APIKEY = "secret"
#url = "https://maps.googleapis.com/maps/api/directions/json?origin=Disneyland&destination=Universal+Studios+Hollywood&key=" + APIKEY
url = "https://maps.googleapis.com/maps/api/directions/json?origin=400+Bizzell+St+TX&destination=Austin+TX+78712&key=" + APIKEY

# Using API Request
response = requests.get(url)
r = json.loads(response.text)

# Using Dummy Data
#with open("./exampleResponse.json") as json_file:
#    response = json.load(json_file)
#r = response

steps = r["routes"][0]["legs"][0]["steps"]
stepBounds = []
for a in range(len(steps)):
    if steps[a]["duration"]["value"] > secondsThreshold:
        stepBounds.append([(steps[a]["start_location"]["lat"], steps[a]["start_location"]["lng"]) , (steps[a]["end_location"]["lat"], steps[a]["end_location"]["lng"])])

dangerScore = 0
for b in range(len(stepBounds)):
    dangerScore += crash_per_area(stepBounds[b][0], stepBounds[b][1])

print(dangerScore)