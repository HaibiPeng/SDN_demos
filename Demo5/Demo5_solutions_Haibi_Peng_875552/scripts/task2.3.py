import requests
from requests.auth import HTTPBasicAuth
import json

url = "http://127.0.0.1:8181/onos/v1/devices/"

device_id = "of:00000a3a67d42346"

myResponse = requests.get(url + device_id + '/ports', auth=HTTPBasicAuth('onos','rocks'))
if myResponse.status_code == 200:
    device_ports = myResponse.json()['ports']
    print('Active ports:')
    for i in range(len(device_ports)):
        port = device_ports[i]['port']
        port_annotation = device_ports[i]['annotations']
        isEnabled = device_ports[i]['isEnabled']
        if isEnabled:
            print('Mac address of port {}: {}'.format(port, port_annotation['portMac']))
            print('Port name of port {}: {}'.format(port, port_annotation['portName']))