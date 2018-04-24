"""
April 23, 2018
Krishna Bhattarai
QuantumIOT
A project to explore datamotion API
"""

import json
import time
from datetime import datetime
import requests
import os
import sys
import wget


"""
http://developers.datamotion.com/docs
https://kb.datamotion.com/?ht_kb=what-are-the-pop3smtp-settings-for-direct


https://kb.datamotion.com/?ht_kb=datamotion-securemail-url-endpoints
Messaging
To access the Messaging API (REST/SOAP), use:

Production: https://ssl.datamotion.com/cmv4/cmv4.asmx
Testing: https://sandbox.datamotion.com/cmv4/cmv4.asmx
Administration
To access the Admin API (REST) use:

Production: https://ssl.datamotion.com/Remote
Testing: https://sandbox.datamotion.com/Remote
Provisioning
To access the Provisioning API (REST) use:

Production: https://provisioning.datamotion.com:8888/
In order to use the DataMotion SecureMail APIs, you must have an active SecureMail account on our system. If you do not have an account and would like to integrate SecureMail into your workflows, please contact DataMotion.
"""


# jeff2@catapulthealth.customer.cmsafe.com.

class DataMotion:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.get_config()

    def get_config(self):
        with open(self.config_file) as config_file:
            config = json.load(config_file)
        return config

    def make_request(self, url):
        print("\nMaking request for url:", url)
        r = requests.get(url=self.url, json=self.paylod, headers=self.headers)
        print("Status code of the request was:", r.status_code)

        if r.status_code == 200:
            # print(json.loads(r.text))
            # print("The response received was:\n", json.loads(r.text))
            # print(r.json)
            return json.loads(r.text)


    def load_json(self, json_file):
        with open(json_file) as json_file:
            data = json.load(json_file)
        return data




def main():
    print("Hello World!")
    pass


if __name__ == "__main__":
    main()


