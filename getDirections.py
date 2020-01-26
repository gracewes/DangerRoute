import requests, json, random

from geopy import distance

num_months = 47 # number of months in the dataset
    
def crash_per_area(pt1, pt2):
    """
    pt1: (lat1, lon1)
    pt2: (lat2, lon2)
    
    returns: number (float) of crashes per square mile within the
             rectangle made by pt1 and pt2 at opposite corners
    """
    lat1, lon1 = pt1
    lat2, lon2 = pt2
    
    bottomLat, topLat = (min(lat1, lat2), max(lat1, lat2))
    leftLon, rightLon = (min(lon1, lon2), max(lon1, lon2))
    
    xDistance = distance.distance((bottomLat, rightLon), (bottomLat, leftLon)).miles
    yDistance = distance.distance((topLat, leftLon), (bottomLat, leftLon)).miles
    rectangle_area = xDistance * yDistance
    
    data_in_rectangle = data[(data['Start_Lat'] >= bottomLat) & (data['Start_Lat'] <= topLat) & (data['Start_Lng'] >= leftLon) & (data['Start_Lng'] <= rightLon)]
    
    num_crashes = data_in_rectangle.shape[0]
    
    return num_crashes / rectangle_area / num_months


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
