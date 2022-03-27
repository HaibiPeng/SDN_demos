import requests
from requests.auth import HTTPBasicAuth

flow_url = "http://127.0.0.1:8181/onos/v1/flows/"

device_id = "of:00006600ea3e3f41"
flow_id = "47850748951191811"

deleteResponse = requests.delete(flow_url + device_id + "/" + flow_id, auth=HTTPBasicAuth('onos','rocks'))
print(deleteResponse)
