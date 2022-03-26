import requests
from requests.auth import HTTPBasicAuth
import json

url = "http://127.0.0.1:8181/onos/v1/intents"

myResponse = requests.get(url + '?detail=false', auth=HTTPBasicAuth('onos','rocks'))
print('All intents:')
if myResponse.status_code == 200:
    intents = myResponse.json()['intents']
    for i in range(len(intents)):
        print('intents {}: {}'.format(i+1, intents[i]))