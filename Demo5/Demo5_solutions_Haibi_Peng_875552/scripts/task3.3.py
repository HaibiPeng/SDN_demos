import requests
from requests.auth import HTTPBasicAuth
import json

url = "http://127.0.0.1:8181/onos/v1/hosts/"

host_id = "9E:BD:DF:85:20:25/None"

myResponse = requests.get(url + host_id, auth=HTTPBasicAuth('onos','rocks'))
if myResponse.status_code == 200:
    mac = myResponse.json()['mac']
    vlan = myResponse.json()['vlan']
    deleteResponse = requests.delete(url + mac + '/' + vlan, auth=HTTPBasicAuth('onos','rocks'))
    print(deleteResponse)
    myResponseAfterDelete = requests.get(url + host_id, auth=HTTPBasicAuth('onos','rocks'))
    print(myResponseAfterDelete.json())