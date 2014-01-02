"""
    Spamchat spams your Snapchat friends!
    Utilizes API outlined in http://gibsonsec.org/snapchat/fulldisclosure/

    Usage: python spamchat.py [images_folder]
"""

import os
import sys
import time
import getpass
import hashlib
from Crypto.Cipher import AES
import requests

HOST = "https://feelinsonice.appspot.com"
STATIC_TOKEN = "m198sOkJEn37DjqZ32lpRu76xmw288xSQ9"
ENCRYPTION_KEY = "M02cnQ51Ji97vwT4"

def ecb_encrypt(data, key):
    length = 16 - (len(data) % 16)
    data += chr(length) * length
    crypt = AES.new(key, AES.MODE_ECB)
    return crypt.encrypt(data)

def request_token(auth_token, timestamp):
    secret = "iEk21fuwZApXlz93750dmW22pw389dPwOk"
    pattern = "0001110111101110001111010101111011010001001110011000110001000110"
    first = hashlib.sha256(secret + auth_token).hexdigest()
    second = hashlib.sha256(str(timestamp) + secret).hexdigest()
    bits = [first[i] if c == "0" else second[i] for i, c in enumerate(pattern)]
    return "".join(bits)

if __name__ == "__main__":
    """
        python spamchat.py [images_folder]
    """

    try:
        IMAGE_FOLDER = sys.argv[1]
    except:
        print "Usage: python spamchat.py [images_folder]"
        sys.exit(0)

    FILES = [os.path.join(IMAGE_FOLDER, file_name)\
             for file_name in os.listdir(IMAGE_FOLDER)\
            if file_name != ".DS_Store"]
    TIMESTAMP = str(int(time.time() * 100))

    USERNAME = raw_input("Your Snapchat Username: ")
    PASSWORD = getpass.getpass("Your Snapchat Password: ")

    recipients_comma = raw_input("Enter comma-separated list of usernames as recipients: ")
    RECIPIENTS = [name.strip() for name in recipients_comma.split(",")] 

    # get a connection
    params = {"username" : USERNAME, "password" : PASSWORD, "timestamp": TIMESTAMP\
            , "req_token" : request_token(STATIC_TOKEN, TIMESTAMP)}
    TOKEN = requests.post(HOST+"/bq/login" , params).json()["auth_token"]

    for file_name in FILES:
        with open(file_name) as f:
            data = f.read()
        
        # upload image
        media_id = USERNAME + TIMESTAMP
        data = ecb_encrypt(data, ENCRYPTION_KEY)
        params = {"username" : USERNAME, "timestamp": TIMESTAMP\
                , "media_id" : media_id, "type" : 0\
                ,"req_token" : request_token(TOKEN, TIMESTAMP)}
        files = {'data' : ('file', data)}
        requests.post(HOST+"/bq/upload", params, files = files)

        # send snapchat
        params = {"username" : USERNAME, "timestamp": TIMESTAMP\
                , "media_id" : media_id, "type" : 0\
                , "country_code" : "US", "recipient" : ",".join(RECIPIENTS)\
                , "time" : 5, "req_token" : request_token(TOKEN, TIMESTAMP)}
        requests.post(HOST+"/bq/send" , params)

