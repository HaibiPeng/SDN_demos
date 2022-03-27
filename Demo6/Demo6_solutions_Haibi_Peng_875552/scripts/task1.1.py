import requests
from requests.auth import HTTPBasicAuth
import json

# specify the device id, which is connected to blue and green
# the selectors specify the traffic from red to blue
# and the instructions include two destination ip and port, which are blue and green
flow_string = '''
{
  "flows": [
    {
      "priority": 40000,
      "timeout": 0,
      "isPermanent": true,
      "deviceId": "of:0000c61d89cfdd4c",
      "treatment": {
        "instructions": [
            {
                "type": "OUTPUT",
                "port": "4"
            },
            {
                "type":"L3MODIFICATION",
                "subtype":"IPV4_DST",
                "ip":"10.0.0.4"
            },
            {
                "type": "OUTPUT",
                "port": "3"
            },
            {
                "type":"L3MODIFICATION",
                "subtype":"IPV4_DST",
                "ip":"10.0.0.3"
            }
        ]
      },
      "selector": {
        "criteria": [
            {
                "type":"ETH_TYPE",
                "ethType":"0x0800"
            },
            {
                "type":"IPV4_SRC",
                "ip":"10.0.0.2/32"
            },
            {
                "type":"IPV4_DST",
                "ip":"10.0.0.3/32"
            }
        ]
      }
    }
  ]
}
'''

# device id is the id of switch connected to red
app_id = "org.onosproject.fwd"
url = "http://127.0.0.1:8181/onos/v1/flows?appId=" + app_id
data = json.loads(flow_string)

myResponse = requests.post(url, data=json.dumps(data), auth=HTTPBasicAuth('onos','rocks'))
print(myResponse.status_code)