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


# jeff@catapulthealth.customer.cmsafe.com Quantum1!
# jeff2@catapulthealth.customer.cmsafe.com Quantum1!
# direct messaging API URL is https://directbeta.datamotion.com/SecureMessagingApi

class DataMotion:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.get_config()

    def get_config(self):
        with open(self.config_file) as config_file:
            config = json.load(config_file)
        return config

    def get_a_session_key(self):
        headers = {
            'Content-Type': 'application/json'
        }
        body = {
            "UserIdOrEmail" :self.config["username"],
            "Password": self.config["password"]
        }
        url = self.config["baseurl"]  + "/Account/Logon"

        r = requests.post(url=url, json=body, headers=headers)
        print("The sessionKey obtained was:", r.text)
        # {"SessionKey": "7B93178BBEBD45588CCE4FD3052F974F"}
        return r.text

    def get_account_details(self, session_key):
        url = self.config["baseurl"] + "/Account/Details"

        headers = {
            'Content-Type': 'application/json',
            'X-Session-Key': session_key
        }

        r = requests.get(url=url, json={}, headers=headers)
        print(r.text)
        """
        {
          "EmailAddress": "jeff@catapulthealth.customer.cmsafe.com",
          "FirstName": "Jeff",
          "LastName": "Smith",
          "Statistics": {
            "AccountSize": 256000,
            "AvailableAccountSize": 256000,
            "DateCreated": "3\/21\/2018 5:20:00 PM (UTC-04:00)",
            "DateOfLastNotice": "1\/1\/1900 1:00:00 AM (UTC-04:00)",
            "DateOfLastVisit": "4\/24\/2018 12:58:00 PM (UTC-04:00)",
            "DatePasswordExpires": "1\/1\/1900 1:00:00 AM (UTC-04:00)",
            "TotalMessagesInInbox": 0,
            "TotalMessagesInOutbox": 0,
            "TotalMessagesReceived": 0,
            "TotalMessagesSent": 0,
            "TotalUnreadMessagesInInbox": 0,
            "TotalVisits": 12,
            "UsedAccountSize": 0
          }
        }
        """

    def send_a_message(self, session_key):
        url = self.config["baseurl"] + "/Message/"

        headers = {
            'Content-Type': 'application/json',
            'X-Session-Key': session_key
        }

        body = {
            "To": ["jeff2@catapulthealth.customer.cmsafe.com"],
            "From": "jeff@catapulthealth.customer.cmsafe.com",
            "Cc": ["kbhattarai@quantumiot.com"],
            "Bcc": ["krishnamani.bhattarai@mavs.uta.edu"],
            "Subject": "This is a test for direct messaging api",
            "CreateTime": "11:51 AM",

            "HtmlBody": "<!DOCTYPE html><html><body>This document contains some sensitive information</body></html>",
            "TextBody": "Patient's Blood Pressure: 120/80"
        }

        r = requests.post(url=url, json=body, headers=headers)
        if r.status_code == 200:
            print("Message successfully sent", r.status_code)
            print("The message id of the message sent was: ", r.text)
            #The message id of the message sent was:  {"MessageId":12077}
        pass

    def get_inbox_message_ids(self, session_key):
        url = self.config["baseurl"] + "/Message/GetInboxMessageIds"

        headers = {
            'Content-Type': 'application/json',
            'X-Session-Key': session_key
        }
        body = {}

        r = requests.post(url=url, json=body, headers=headers)
        if r.status_code == 200:
            print("Request successfully completed", r.status_code)
            # print("The message ids are: ", r.text)
            #The message id of the message sent was:  {"MessageId":12077}
            return r.json()["MessageIds"]
        return []

    def get_a_message_by_id(self, session_key, MessageId):
        url = self.config["baseurl"] + "/Message/" + str(MessageId)

        headers = {
            'Content-Type': 'application/json',
            'X-Session-Key': session_key
        }
        body = {}
        r = requests.get(url=url, json=body, headers=headers)
        if r.status_code == 200:
            print("Request successfully completed", r.status_code)
            # print(r.text)
            return r.json()
            # {
            #     "To": [
            #         "\"jeff2@catapulthealth.customer.cmsafe.com\" <jeff2@catapulthealth.customer.cmsafe.com>"
            #     ],
            #     "From": "\"jeff@catapulthealth.customer.cmsafe.com\" <jeff@catapulthealth.customer.cmsafe.com>",
            #     "Cc": [
            #         "\"kbhattarai@quantumiot.com\" <kbhattarai@quantumiot.com>"
            #     ],
            #     "Bcc": [],
            #     "Subject": "This is a test for direct messaging api",
            #     "CreateTime": "4/24/2018 1:13:54 PM (UTC-04:00)",
            #     "Attachments": [],
            #     "HtmlBody": "<!DOCTYPE html><html><body>This document contains some sensitive information</body></html>",
            #     "TextBody": "Patient's Blood Pressure: 120/80"
            # }
        pass

    def load_json(self, json_file):
        with open(json_file) as json_file:
            data = json.load(json_file)
        return data






def main():

    #### First Send A Message
    # datamotion_config_file1 = "./config/config1.json"
    # my_data_motion_instance1 = DataMotion(datamotion_config_file1)
    # SessionKey = json.loads(my_data_motion_instance1.get_a_session_key())["SessionKey"]
    # my_data_motion_instance.get_account_details(SessionKey)
    # my_data_motion_instance1.send_a_message(SessionKey)


    #### Second Retrieve a Message
    datamotion_config_file2 = "./config/config2.json"
    my_data_motion_instance2 = DataMotion(datamotion_config_file2)
    SessionKey = json.loads(my_data_motion_instance2.get_a_session_key())["SessionKey"]
    message_ids_array = my_data_motion_instance2.get_inbox_message_ids(SessionKey)
    for id in message_ids_array:
        message_details = my_data_motion_instance2.get_a_message_by_id(SessionKey,id)
        print(json.dumps(message_details))
    pass


if __name__ == "__main__":
    main()


