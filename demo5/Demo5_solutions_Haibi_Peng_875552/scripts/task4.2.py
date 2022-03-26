import requests
from requests.auth import HTTPBasicAuth
import json

url = "http://127.0.0.1:8181/onos/v1/flows/"

device_id = "of:0000f29dc116ea40"

myResponse = requests.get(url, auth=HTTPBasicAuth('onos','rocks'))
print('Flows:')
print ("    flow_id         application_id          device_id                      instructions")
if myResponse.status_code == 200:
    flows = myResponse.json()['flows']
    for i in range(len(flows)):
        flow = flows[i]
        flow_id = flow['id']
        application_id = flow['appId']
        device_id = flow['deviceId']
        instructions = flow['treatment']['instructions']
        print('{}  {}  {}  {}'.format(flow_id, application_id, device_id, instructions))