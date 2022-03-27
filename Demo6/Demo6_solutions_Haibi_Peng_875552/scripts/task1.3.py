import requests
from requests.auth import HTTPBasicAuth
import json

# specify the device id, which is connected to red
# leave the treatment blank so the selected packets will be dropped
flow_string = '''
{
  "flows": [
    {
      "priority": 40000,
      "timeout": 0,
      "isPermanent": true,
      "deviceId": "of:00006600ea3e3f41",
      "treatment": {
        "instructions": []
      },
      "selector": {
        "criteria": [
            {
                "type":"ETH_TYPE",
                "ethType":"0x0800"
            },
            {
                "type":"IPV4_DST",
                "ip":"10.0.0.2/32"
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