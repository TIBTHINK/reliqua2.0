#!/usr/bin/python3
import hashlib
import requests
import json
import base64
from time import sleep
import sys
import random

with open("config.json") as config:
    config = json.load(config)



class uconvert:
    def b64(string):
        string = remove_p(string)
        return base64.b64decode(string).decode('utf-8')

    def b32(string):
        string = remove_p(string)
        return base64.b32encode(bytearray(string, 'ascii')).decode('utf-8')

    def binary(string):
        string = remove_p(string)
        binary = string.split()
        asciiString = ""
        for i in binary:
            asInt = int(i, 2)
            asciiCharacter = chr(asInt)
            asciiString += asciiCharacter
        return asciiString

    def ascii(string):
        string = remove_p(string)
        li = list(string.split(" "))
        ascii_out = []
        for i in li:
            ascii_out.append(chr(int(i)))
        output = ""
        # convert to string
        return output.join(ascii_out)

    def key(key):
        key_out = []
        for i in key:
            key_out.append(int(i))
        return list(reversed(key_out))

    def translate(list, message):
        for i in range(len(list)):
            # print(i)
            # print(list[i])
            # if i == 0:
            if list[i] == 1:
                message = uconvert.b64(message)
                # print(message)
            elif list[i] == 2:
                message = uconvert.ascii(message)
                # print(message)
            elif list[i] == 3:
                message = uconvert.binary(message)
                # print(message)
            # elif list[i] == 4:
                # print("test")
            else:
                return print("ERROR: Key out of range")
        return(message)

# http://pioxy.ddns.net:3000/tibthink/minecraft-server/src/branch/main/init-server.py#L35
def remove_p(string):
    punctuation = '''"'''
    remove_punct = """"""
    for character in string:
        if character not in punctuation:
            remove_punct = remove_punct + character
    return remove_punct
def dump(object):
    response = requests.get("http://" + config["ip"] + ":" + str(config["port"]) + "/data.json")
    output = response.json()
    data = json.dumps(output[object])
    return data

# Type writting effect
# https://stackoverflow.com/a/59401383
def writing_effect(text):
    for i in text:
        print(i, end='')
        sys.stdout.flush()
        sleep(random.uniform(.01, .2))


def hashed(password):
    # Create a hash using SHA-256
    hash_obj = hashlib.sha256(password.encode())
    hashed_password = hash_obj.hexdigest()
    return hashed_password

try:
    code_check = input("Please enter the code: ")
    # Getting date and time and checking making sure it matches the json
    if remove_p(dump("code")) == hashed(code_check):
        print("\n")
        writing_effect(uconvert.translate(uconvert.key(config['key']), dump("message")))
        print("\n")
        sleep(1)
        print("Press ctrl + C to exit")
        sleep(9999)
        print("damn your left this open for 2.7 hours, really that interesting of a message")
    else:
        exit("Sorry the code given was incorrect, Please try again")
except KeyboardInterrupt:
    print("\nGoodbye")