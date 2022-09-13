import requests
from requests.auth import HTTPBasicAuth
import json

url = "http://127.0.0.1:8181/onos/v1/devices/"

device_id = "of:00000a3a67d42346"

myResponse = requests.get(url + device_id + '/ports', auth=HTTPBasicAuth('onos','rocks'))
if myResponse.status_code == 200:
    device_annotaions = myResponse.json()['annotations']
    print('IP management address: ' + device_annotaions['managementAddress'])
    print('OpenFlow version: ' + device_annotaions['protocol'])