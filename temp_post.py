import requests
from requests.auth import HTTPBasicAuth
import json
import datetime

URL='http://ec2-52-208-203-88.eu-west-1.compute.amazonaws.com/api/v1.0/readings'
USER='dawsonm'
PASSWORD='Lf0oTS4M'

def main():
     r=post_temp('77')
     print r
     print r.text

def post_temp(temp):
    '''Post temperature data to ec2'''
    payload={}
    payload['dlog']=str(datetime.datetime.now())
    payload['temp']=temp
    myjson=json.dumps(payload)

    r=requests.post(URL, json=myjson, auth=(USER, PASSWORD))
    return r
 
if __name__ == '__main__':
    main()
