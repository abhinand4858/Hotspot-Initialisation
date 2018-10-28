#!/usr/bin/python3

import datetime
import sys
import json

import requests
from urllib2 import urlopen
from subprocess import Popen, PIPE


file_path = "/opt/attendance/"
base_url = "https://amfoss.in/api/"


def check_internet_connection():
    try:
        status_code = urlopen('http://foss.amrita.ac.in').getcode()
        if status_code == 200:
            return True
    except:
        print("Internet error")
        return False
    return False

def get_auth_token():
    token = ''
    try:
        with open('/opt/attendance/.token', 'r') as file:
            token = file.readline()
    except EnvironmentError:
        print("Token error, run 'python3 get_and_save_auth_token.py'")
    return token


def fetch_latest_ssid():
    # curl -H "Authorization: JWT <your_token>" https://amfoss.in/api/ssid-name/

    url = base_url + "ssid-name/"

    headers = {"Authorization": "JWT " + get_auth_token()}
    response = requests.get(url=url, headers=headers)
    try:
        data = json.loads(response.text)
    except Exception as e:
        print(e)
        sys.exit()
        
    if 'name' not in data.keys():
        print("Authentication token error")
        print(data)
        sys.exit()

    ssid = data['name']
    return ssid.strip().lower()



if __name__ == '__main__':

    # check internet connection
    if not check_internet_connection():
        sys.exit()


    # get new ssid from server
    fetched_ssid = fetch_latest_ssid()
    
    if not fetched_ssid:
        sys.exit()

    print(fetched_ssid)
