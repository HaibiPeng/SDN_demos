import requests
from requests.auth import HTTPBasicAuth
import json

intent_string1 = '''
{
  "type": "PointToPointIntent",
  "appId": "org.onosproject.fwd",
  "treatment": {
    "instructions": [
      {
        "type": "OUTPUT",
        "port": "4"
      }
    ],
    "deferred": []
  },
  "priority": 55,
  "ingressPoint": {
    "port": "4",
    "device": "of:00009ed62bc8b14b"
  },
  "egressPoint": {
    "port": "4",
    "device": "of:00000a8618536343"
  }
}
'''

intent_string2 = '''
{
  "type": "PointToPointIntent",
  "appId": "org.onosproject.fwd",
  "treatment": {
    "instructions": [
      {
        "type": "OUTPUT",
        "port": "4"
      }
    ],
    "deferred": []
  },
  "priority": 55,
  "ingressPoint": {
    "port": "4",
    "device": "of:00000a8618536343"
  },
  "egressPoint": {
    "port": "4",
    "device": "of:00009ed62bc8b14b"
  }
}
'''

url = "http://127.0.0.1:8181/onos/v1/intents/"
data1 = json.loads(intent_string1)
data2 = json.loads(intent_string2)

myResponse1 = requests.post(url, data=json.dumps(data1), auth=HTTPBasicAuth('onos','rocks'))
print(myResponse1.status_code)

myResponse2 = requests.post(url, data=json.dumps(data2), auth=HTTPBasicAuth('onos','rocks'))
print(myResponse1.status_code)