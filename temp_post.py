import requests
from requests.auth import HTTPBasicAuth
import json
import datetime


url='http://localhost:5000/api/v1.0/readings'
payload={}
payload['dlog']=str(datetime.datetime.now())
payload['temp']='81'
json=json.dumps(payload)

r=requests.post(url, json=json, auth=('dawsonm','Lf0oTS4M'))

print r
