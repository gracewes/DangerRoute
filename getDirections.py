import requests, json
APIKEY = "secret"
url = "https://maps.googleapis.com/maps/api/directions/json?origin=Disneyland&destination=Universal+Studios+Hollywood&key=" + APIKEY
response = requests.get(url)
r = json.loads(response.text)
print(r["legs"])