"""
April 23, 2018
Krishna Bhattarai
QuantumIOT
A project to explore datamotion API
"""

import json
import requests
import base64

"""
http://developers.datamotion.com/docs
https://kb.datamotion.com/?ht_kb=what-are-the-pop3smtp-settings-for-direct
In order to use the DataMotion SecureMail APIs, you must have an active SecureMail account on our system. If you do not have an account and would like to integrate SecureMail into your workflows, please contact DataMotion.
# jeff@catapulthealth.customer.cmsafe.com Quantum1!
# jeff2@catapulthealth.customer.cmsafe.com Quantum1!
# direct messaging API URL is https://directbeta.datamotion.com/SecureMessagingApi
"""


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
        # This is an example of what the session key looks like
        #  {"SessionKey": "7B93178BBEBD45588CCE4FD3052F974F"}
        # print(json.loads(r.text), type(json.loads(r.text)))
        return json.loads(r.text)["SessionKey"]


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
        encoded_string = self.encode_to_base_64("./docs/adamEverymanB2.xml").decode("utf-8")

        url = self.config["baseurl"] + "/Message/"

        headers = {
            'Content-Type': 'application/json',
            'X-Session-Key': session_key
        }

        body = {
            "To": ["jeff2@catapulthealth.customer.cmsafe.com"],
            "From": "jeff@catapulthealth.customer.cmsafe.com",
            "Cc": [],
            "Bcc": [],
            "Subject": "This is another test email for direct messaging api",
            "CreateTime": "11:51 AM",
            "Attachments": [{
                "AttachmentBase64": str(encoded_string),
                "ContentType": "application/xml",
                "FileName": "adamEverymanB2.xml"
            }],

            "HtmlBody": "<!DOCTYPE html><html><body>This document contains sensitive information in C-CDA XML format</body></html>",
            "TextBody": "Another Sample Email Message"
        }

        r = requests.post(url=url, json=body, headers=headers)

        if r.status_code == 200:
            print("Message successfully sent", r.status_code)
            print("The message id of the message sent was: ", r.text)
            #The message id of the message sent was:  {"MessageId":12077}
            #The message id of the message sent was:  {"MessageId":12080}
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
            # The message id of the message sent was:  {"MessageId":12077}
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
            print(r.json())
            return r.json()

    def load_json(self, json_file):
        with open(json_file) as json_file:
            data = json.load(json_file)
        return data

    def encode_to_base_64(self, filename):
        fp = open(filename, "rb")
        bytes = fp.read()
        encoded_string = base64.b64encode(bytes )
        return encoded_string

    def decode_base_64(self, some_encoded_string):
        return base64.b64decode(some_encoded_string).decode("utf-8")




def send_a_message_with_CCDA_XML_Payload():
    ################## First Send A Message With C-CDA XML Payload ############################

    # define a configuration file for the first account
    datamotion_config_file1 = "./config/config1.json"

    # Create an instance of the datamotion class using this configuration file
    my_data_motion_instance1 = DataMotion(datamotion_config_file1)

    # Get a Session Key that is required to make various other calls using this account
    SessionKey = my_data_motion_instance1.get_a_session_key()

    # To view the account details
    my_data_motion_instance1.get_account_details(SessionKey)

    # To Send a Message with a C-CDA XML as a payload
    my_data_motion_instance1.send_a_message(SessionKey)

    ################## End of Sending Message With C-CDA XML Payload ##########################

def retrieve_a_message_with_CCDA_XML_Payload():
    ################## Second Retrieve A Message With C-CDA XML Payload ############################

    # define a configuratino file for the second account
    datamotion_config_file2 = "./config/config2.json"

    # Create an instance of the datamotion class using this configuration file
    my_data_motion_instance2 = DataMotion(datamotion_config_file2)

    # Get a Session Key that is required to make various other calls using this account
    SessionKey = my_data_motion_instance2.get_a_session_key()

    # Retrieve all the message ids in the inbox in an array
    message_ids_array = my_data_motion_instance2.get_inbox_message_ids(SessionKey)

    # Iterate through all the message ids in the message ids array
    for id in message_ids_array:
        # retrieve each message
        my_retrieved_json = my_data_motion_instance2.get_a_message_by_id(SessionKey, id)

        # check to see if message has attachments
        if my_retrieved_json["Attachments"]:
            # retrieve the base 64 encoded payload of the C-CDA XML
            base64encoded_message = my_retrieved_json["Attachments"][0]["AttachmentBase64"]
            print("Base 64 encoded message:\n", base64encoded_message)

            # decode the encoded message to get back the original C-CDA XML Payload
            decoded_message = my_data_motion_instance2.decode_base_64(base64encoded_message)
            print("Decoded message (C-CDA XML Payload)):\n", decoded_message)

            ################## End of retrieving a Message With C-CDA XML Payload ############################


def main():
    send_a_message_with_CCDA_XML_Payload()
    retrieve_a_message_with_CCDA_XML_Payload()

if __name__ == "__main__":
    main()


