import requests
from requests.auth import HTTPBasicAuth
import json

url = "http://127.0.0.1:8181/onos/v1/intents/"

intentsDetailsResponse = requests.get(url, auth=HTTPBasicAuth('onos','rocks'))
if intentsDetailsResponse.status_code == 200:
  intents = intentsDetailsResponse.json()['intents']
  print(intents)
  for i in range(len(intents)):
    intent = intents[i]
    intentsDeleteResponse = requests.delete(url + intent['appId'] + '/' + intent['key'], auth=HTTPBasicAuth('onos','rocks'))
    print(intentsDeleteResponse.status_code)