import requests
from requests.auth import HTTPBasicAuth
import json
import datetime

#URL='http://ec2-52-208-203-88.eu-west-1.compute.amazonaws.com/api/v1.0/readings'
URL='http://ec2-52-208-203-88.eu-west-1.compute.amazonaws.com/api/v1.0/weather'
#URL='http://localhost:5000/api/v1.0/weather'

USER='dawsonm'
PASSWORD='Lf0oTS4M'

def main():
     r=post_weather('923','24')
     print r.status_code
     print r.json()

def post_weather(pressure,temperature):
    '''Post weather data to ec2'''
    payload={}
    payload['datetime_logged']=str(datetime.datetime.now())
    payload['pressure']=pressure
    payload['temperature']=temperature
    myjson=json.dumps(payload)

    r=requests.post(URL, json=myjson, auth=(USER, PASSWORD))
    return r
 
if __name__ == '__main__':
    main()
