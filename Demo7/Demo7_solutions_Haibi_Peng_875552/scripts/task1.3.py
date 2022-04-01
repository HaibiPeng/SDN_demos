import requests
from requests.auth import HTTPBasicAuth
import json

intent_string = '''
{
  "type": "HostToHostIntent",
  "appId": "org.onosproject.fwd",
  "priority": 55,
  "one": "06:F9:EA:86:BE:EB/None",
  "two": "4E:34:A5:A4:EA:D3/None"
}
'''

url = "http://127.0.0.1:8181/onos/v1/intents/"
data = json.loads(intent_string)

myResponse = requests.post(url, data=json.dumps(data), auth=HTTPBasicAuth('onos','rocks'))
print(myResponse.status_code)
