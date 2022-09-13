import requests
from requests.auth import HTTPBasicAuth
import json

url = "http://127.0.0.1:8181/onos/v1/hosts/"

myResponse = requests.get(url, auth=HTTPBasicAuth('onos','rocks'))
if myResponse.status_code == 200:
    hosts = myResponse.json()['hosts']
    for i in range(len(hosts)):
        host = {
            "id": hosts[i]['id'],
            "Mac address": hosts[i]['mac'],
            "IP addresses": hosts[i]['ipAddresses'],
        }
        print('Host {}: {}'.format(i + 1, host))