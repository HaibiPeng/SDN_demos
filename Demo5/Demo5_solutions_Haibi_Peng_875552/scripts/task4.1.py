import requests
from requests.auth import HTTPBasicAuth
import json

url = "http://127.0.0.1:8181/onos/v1/links/"

myResponse = requests.get(url, auth=HTTPBasicAuth('onos','rocks'))
print('Active links:')
print ("   device_id_src    port_src   device_id_dst    port_dst")
if myResponse.status_code == 200:
    links = myResponse.json()['links']
    for i in range(len(links)):
        state = links[i]['state']
        if state:
            src = links[i]['src']
            dst = links[i]['dst']
            print('{}    {}    {}    {}'.format(src['device'],  src['port'], dst['device'],  dst['port']))