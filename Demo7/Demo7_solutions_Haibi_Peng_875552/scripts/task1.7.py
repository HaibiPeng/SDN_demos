import requests
from requests.auth import HTTPBasicAuth
import json

hosts_mac = ["06:F9:EA:86:BE:EB", "5A:B6:94:09:64:25", "D6:B3:89:DF:3F:32", "4E:34:A5:A4:EA:D3", "06:37:D5:AE:25:BB"]

intent_string = '''
{{
  "type": "HostToHostIntent",
  "appId": "org.onosproject.fwd",
  "priority": 55,
  "one": "{}/None",
  "two": "{}/None"
}}
'''

url = "http://127.0.0.1:8181/onos/v1/intents/"

for i in range(len(hosts_mac) - 1):
  for j in range(i + 1, len(hosts_mac)):
    data = json.loads(intent_string.format(hosts_mac[i], hosts_mac[j]))
    myResponse = requests.post(url, data=json.dumps(data), auth=HTTPBasicAuth('onos','rocks'))
    print("Intent between {} and {}:".format(hosts_mac[i], hosts_mac[j]), myResponse.status_code)