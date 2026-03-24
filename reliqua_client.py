#!/usr/bin/python3
import hashlib
import requests
import json
import base64
from time import sleep
import sys
import random
import os

def get_resource_path(filename):
    # Prefer explicit file in current working directory
    if os.path.exists(filename):
        return os.path.abspath(filename)

    # If running as a bundled/frozen executable, try executable directory
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable) or os.path.dirname(os.path.abspath(sys.argv[0]))
        candidate = os.path.join(exe_dir, filename)
        if os.path.exists(candidate):
            return candidate

        # Also try the directory of argv[0]
        argv_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        candidate = os.path.join(argv_dir, filename)
        if os.path.exists(candidate):
            return candidate

    # Fall back to the script directory
    script_dir = os.path.dirname(__file__)
    candidate = os.path.join(script_dir, filename)
    if os.path.exists(candidate):
        return candidate

    # Not found; return original name so open() raises FileNotFoundError
    return filename

try:
    with open(get_resource_path("config.json"), "r") as cfg_file:
        config = json.load(cfg_file)
except FileNotFoundError:
    exit("Error: config.json not found. Make sure it's bundled or present next to the executable.")


def fetch_data():
    try:
        # Replace with your URL
        response = requests.get("http://" + config["ip"] + ":" + str(config["port"]) + "/data.json")
        response.raise_for_status()  # Will raise HTTPError for bad responses
        return response.json()
    except ConnectionError as e:
        exit("""Error Code: Connection refused.
             Please make sure that you port forward.""")
    except requests.exceptions.RequestException as e:
        exit("Error Code: An error occurred.")
    except Exception as e:
        exit("Error Code: Unexpected error.")

def print_ascii_art():
    ascii_art = [
r" /$$$$$$$            /$$ /$$                              ",
r"| $$__  $$          | $$|__/                              ",
r"| $$  \ $$  /$$$$$$ | $$ /$$  /$$$$$$  /$$   /$$  /$$$$$$ ",
r"| $$$$$$$/ /$$__  $$| $$| $$ /$$__  $$| $$  | $$ |____  $$",
r"| $$__  $$| $$$$$$$$| $$| $$| $$  \ $$| $$  | $$  /$$$$$$$",
r"| $$  \ $$| $$_____/| $$| $$| $$  | $$| $$  | $$ /$$__  $$",
r"| $$  | $$|  $$$$$$$| $$| $$|  $$$$$$$|  $$$$$$/|  $$$$$$$",
r"|__/  |__/ \_______/|__/|__/ \____  $$ \______/  \_______/",
r"                                  | $$                    ",
r"                                  | $$                    ",
r"                                  |__/                    ",
r"                                                          ",
]
    for line in ascii_art:
        print(line)
        sleep(0.2)

# Function to print a progress bar with spinning animation
def progress_bar_with_spinner(total=100):
    spinner = ['|', '/', '-', '\\']
    for i in range(total + 1):
        bar = 'Loading: [' + '#' * (i // 4) + ' ' * ((100 - i) // 4) + ']'
        sys.stdout.write(f'\r{bar} {i}% {spinner[i % 4]}')
        sys.stdout.flush()
        sleep(0.01)


import base64

class uconvert:
    @staticmethod
    def remove_p(string):
        # Assuming remove_p is meant to clean up the string; adjust as necessary
        return string.strip()  # Example: just strips whitespace, modify if needed.

    @staticmethod
    def b64(string):
        string = uconvert.remove_p(string)
        try:
            return base64.b64decode(string).decode('utf-8')
        except (UnicodeDecodeError, base64.binascii.Error) as e:
            print(f"Base64 decoding error: {e}")
            return None  # Or handle the error as needed

    @staticmethod
    def binary(string):
        string = uconvert.remove_p(string)
        binary = string.split()
        asciiString = ""
        for i in binary:
            asInt = int(i, 2)
            asciiCharacter = chr(asInt)
            asciiString += asciiCharacter
        return asciiString

    @staticmethod
    def ascii(string):
        string = uconvert.remove_p(string)
        li = list(string.split(" "))
        ascii_out = [chr(int(i)) for i in li]
        return "".join(ascii_out)

    @staticmethod
    def hex(string):
        try:
            return bytes.fromhex(string).decode("utf-8")
        except UnicodeDecodeError as e:
            print(f"Hex decoding error: {e}")
            return None  # Or handle the error as needed
    
    @staticmethod
    def octal(string):
    # Split the input string into individual octal values
        # print(string)
        octal_values = string.split()
        
        # Convert each octal value to its corresponding character
        characters = [chr(int(oct_value, 8)) for oct_value in octal_values]
        
        # Join the characters to form the original text
        return ''.join(characters)

    @staticmethod
    def key(key):
        key_out = [int(i) for i in key]
        return list(reversed(key_out))

    @staticmethod
    def translate(list, message):
        for i in range(len(list)):
            if list[i] == 1:
                message = uconvert.b64(message)
            elif list[i] == 2:
                message = uconvert.ascii(message)
            elif list[i] == 3:
                message = uconvert.binary(message)
            elif list[i] == 4:
                message = uconvert.hex(message)
            elif list[i] == 5:
                message = uconvert.octal(message)
            else:
                print("ERROR: Key out of range")
                return None
        return message


# http://pioxy.ddns.net:3000/tibthink/minecraft-server/src/branch/main/init-server.py#L35
def remove_p(string):
    punctuation = '''"'''
    remove_punct = """"""
    for character in string:
        if character not in punctuation:
            remove_punct = remove_punct + character
    return remove_punct
def dump(object):
    ip = remove_p(config["ip"])
    response = requests.get("http://" + ip + ":" + str(config["port"]) + "/data.json")
    output = response.json()
    # data = json.dumps(output[object])
    return output[object]

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

def check_password(hashed_code, unhashed_code_input):
    while True:  # Start an infinite loop
        # Hash the user's input (encode to bytes) and compare hex digests
        input_hash = hashlib.sha256(unhashed_code_input.encode()).hexdigest()
        if input_hash == hashed_code:
            print("Access granted!")
            break
        else:
            print("Incorrect password, please try again.\n")
            # unhashed_code_input = input("Enter the code: ")

def get_resource_path(filename):
        if getattr(sys, 'frozen', False):
            # Running as compiled binary
            base_path = os.path.dirname(sys.executable)
        else:
            # Running as normal Python
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, filename)

if __name__ == '__main__':
    print("\n")
    fetch_data()
    print_ascii_art()
    
    progress_bar_with_spinner()
    print("\n")
    try:
        # Getting the hashed code directly from the dump function
        print("Hint: " + uconvert.translate(uconvert.key(config['key']), dump("hint")))
        code_to_check = remove_p(dump("code"))
        unhashed_code_input = input("Enter the code: ")
        check_password(code_to_check, unhashed_code_input)  # Use the fetched code for checking
        print("\n") 
        message = uconvert.translate(uconvert.key(config['key']), dump("message"))
        writing_effect(message)
        print("\n")
        sleep(1)
        print("Press ctrl + C to exit")
        sleep(9999)
        exit("damn you left this open for 2.7 hours, must be a really interesting message")

    except KeyboardInterrupt:
        print("\nGoodbye")