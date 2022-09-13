import requests
from requests.auth import HTTPBasicAuth
import json

url = "http://127.0.0.1:8181/onos/v1/devices/"

myResponse = requests.get(url, auth=HTTPBasicAuth('onos','rocks'))
if myResponse.status_code == 200:
    devices = myResponse.json()['devices']
    for i in range(len(devices)):
        print('Device {} id: {} '.format(i + 1, devices[i]['id']))