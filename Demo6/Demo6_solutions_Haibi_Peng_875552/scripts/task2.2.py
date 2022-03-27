import requests
from requests.auth import HTTPBasicAuth

url = "http://127.0.0.1:8181/onos/v1/flows/application/"

apps = ["org.onosproject.hostprovider","org.onosproject.mobility","org.onosproject.lldpprovider","org.onosproject.ofagent","org.onosproject.openflow.base",
"org.onosproject.openflow","org.onosproject.roadm","org.onosproject.proxyarp","org.onosproject.fwd","org.onosproject.core"]

for app in apps :
    myResponse = requests.get(url + app, auth=HTTPBasicAuth('onos','rocks'))
    if myResponse.status_code == 200:
        flows = myResponse.json()["flows"]
        print("Flow rule of application %s "%app)
        print(flows)
        print("----------------------------------------")