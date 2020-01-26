import requests, json, random
import pandas as pd

from geopy import distance

num_months = 47 # number of months in the dataset

US_Accidents_Dec19 = pd.read_csv("US_Accidents_Dec19.csv")
data = US_Accidents_Dec19[['Start_Time', 'End_Time', 'Start_Lat', 'Start_Lng', 'Street', 'Severity']]
    
def score_rectangle(pt1, pt2):
    """
    pt1: (lat1, lon1)
    pt2: (lat2, lon2)
    
    returns: number (float) of crashes per unit area within rectangle
             made by pt1 and pt2 at opposite corners
    """
    lat1, lon1 = pt1
    lat2, lon2 = pt2
    #rectangle_area = abs((lat1 - lat2) * (lon1 - lon2))
    
    bottomLat, topLat = (min(lat1, lat2), max(lat1, lat2))
    leftLon, rightLon = (min(lon1, lon2), max(lon1, lon2))
    
    xDistance = distance.distance((bottomLat, rightLon), (bottomLat, leftLon)).miles
    yDistance = distance.distance((topLat, leftLon), (bottomLat, leftLon)).miles
    rectangle_area = xDistance * yDistance
    
    crashes_in_rectangle = data[(data['Start_Lat'] >= bottomLat) & (data['Start_Lat'] <= topLat) & (data['Start_Lng'] >= leftLon) & (data['Start_Lng'] <= rightLon)]
    
    num_crashes = crashes_in_rectangle.shape[0]
    avg_severity = crashes_in_rectangle['Severity'].mean() / 4
    
    if rectangle_area == 0 or num_crashes == 0:
        return 0

    return num_crashes * avg_severity / rectangle_area / num_months


secondsThreshold = 120

options = {
    "origin": "400 Bizzell St TX",
    "destination": "Austin TX 78712",
    "key": "secret"
}
url = "https://maps.googleapis.com/maps/api/directions/json"

# Using API Request
response = requests.get(url, params=options)
r = json.loads(response.text)

steps = r["routes"][0]["legs"][0]["steps"]
stepBounds = []
for a in range(len(steps)):
    if steps[a]["duration"]["value"] > secondsThreshold:
        stepBounds.append([(steps[a]["start_location"]["lat"], steps[a]["start_location"]["lng"]) , (steps[a]["end_location"]["lat"], steps[a]["end_location"]["lng"])])

dangerScore = 0
for b in range(len(stepBounds)):
    dangerScore += score_rectangle(stepBounds[b][0], stepBounds[b][1])

print(dangerScore)
