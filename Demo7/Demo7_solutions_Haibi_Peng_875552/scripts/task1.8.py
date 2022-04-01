import requests
from requests.auth import HTTPBasicAuth
import json

intent_string = '''
{
  "type": "SinglePointToMultiPointIntent",
  "appId": "org.onosproject.fwd",
  "priority": 55,
  "selector": {
    "criteria": [
        {
            "type":"ETH_TYPE",
            "ethType":"0x0800"
        },
        {
            "type": "TCP_DST",
            "tcpPort": 4009
        },
        {
            "type": "IP_PROTO",
            "protocol": 6
        }
    ]
  },
  "ingressPoint": {
    "port": "4",
    "device": "of:00009ed62bc8b14b"
  },
  "egressPoint": [
    {
        "port": "3",
        "device": "of:0000527da71fda4f"
    },
    {
        "port": "2",
        "device": "of:000096b38f961446"
    },
    {
        "port": "4",
        "device": "of:00000a8618536343"
    }
  ]
}
'''

url = "http://127.0.0.1:8181/onos/v1/intents/"
data = json.loads(intent_string)

myResponse = requests.post(url, data=json.dumps(data), auth=HTTPBasicAuth('onos','rocks'))
print(myResponse.status_code)