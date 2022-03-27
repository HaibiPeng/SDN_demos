import requests
from requests.auth import HTTPBasicAuth

device_url = "http://127.0.0.1:8181/onos/v1/devices/"
flow_url = "http://127.0.0.1:8181/onos/v1/flows/"

deviceResponse = requests.get(device_url, auth=HTTPBasicAuth('onos','rocks'))
if deviceResponse.status_code == 200:
    # first get the device id
    devices = deviceResponse.json()['devices']
    for i in range(len(devices)):
        available = devices[i]['available']
        # if the device is available
        if available:
            # get the flows of each device
            # print('Device id: {} '.format(devices[i]['id']))
            flowResponse = requests.get(flow_url + devices[i]['id'], auth=HTTPBasicAuth('onos','rocks'))
            flows = flowResponse.json()["flows"]
            print('Flow rules of Device id {}'.format(devices[i]['id']))
            print(flows)
            print("------------------------------------------------------------------")