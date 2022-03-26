import requests
from requests.auth import HTTPBasicAuth
import json

url = "http://127.0.0.1:8181/onos/v1/hosts/"

host_ip = "10.0.0.130"

myResponse = requests.get(url, auth=HTTPBasicAuth('onos','rocks'))
print('Device id and the port used by the host having “10.0.0.130" as an IP address:')
if myResponse.status_code == 200:
    hosts = myResponse.json()['hosts']
    for i in range(len(hosts)):
        ip_addresses = hosts[i]['ipAddresses']
        if host_ip in ip_addresses:
            locations = hosts[i]['locations']
            for j in range(len(locations)):
                print('Device id {}: {}'.format(j + 1, locations[j]['elementId']))
                print('Port number {}: {}'.format(j + 1, locations[j]['port']))