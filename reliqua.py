#!/usr/bin/python3

import json
import base64
import reliqua_server as rs
import click
import random
import os
import shutil
import platform
import hashlib
import sys

ip = rs.get_ip()
pwd = os.getcwd()
system = platform.system()
version = "2.1.6"

if system == "Windows":
    type_of_os = "windows"
elif system == "darwin":
    type_of_os = "darwin"
else:
    type_of_os = "unix"

import base64

def remove_p(string):
    punctuation = '''"'''
    remove_punct = """"""
    for character in string:
        if character not in punctuation:
            remove_punct = remove_punct + character
    return remove_punct

class convert:
    @staticmethod
    def b64(string):
        # Convert string to bytes and then to Base64
        return base64.b64encode(string.encode('utf-8')).decode('utf-8')

    @staticmethod
    def ascii(string):
        ascii_out = [str(ord(i)) for i in string]
        return " ".join(ascii_out)

    @staticmethod
    def binary(string):
        return remove_p(' '.join(format(ord(x), 'b') for x in string))

    @staticmethod
    def hex(string):
        # Convert string to hex
        hex_string = string.encode("utf-8").hex()
        # Add spaces every 2 characters
        spaced_hex_string = ' '.join(hex_string[i:i + 2] for i in range(0, len(hex_string), 2))
        return spaced_hex_string

    
    def octal(string):
        octal_values = [format(ord(char), 'o') for char in string]
        return ' '.join(octal_values)

    def key(key):
        key_out = []
        for i in key:
            key_out.append(int(i))
        return key_out


    @staticmethod
    def translate(list, message):
        count = 0
        for i in range(len(list)):
            if list[i] == 1:
                message = convert.b64(message)
                count += 1
            elif list[i] == 2:
                message = convert.ascii(message)
                count += 1
            elif list[i] == 3:
                message = convert.binary(message)
                count += 1
            elif list[i] == 4:
                message = convert.hex(message)
                count += 1
            # elif list[i] == 5:
            #     message = convert.octal(message)
            #     count += 1    
            else:
                return print("ERROR: Key out of range")
        return message

    
def hashed(password):
    # Create a hash using SHA-256
    hash_obj = hashlib.sha256(password.encode())
    hashed_password = hash_obj.hexdigest()
    return hashed_password

@click.command()
@click.option("-m", "--message", help="Sets your message")
@click.option("-p", "--port", default=8080, help="Sets the port you want the server to run on")
@click.option("-k", "--keygen", default=8, help="how many combinations do you want your message to have")
@click.option("-c", "--code", help="Set the code to unlock the message")
@click.option("-s", "--server", is_flag=True, flag_value=True, help="Runs the server in the backgroud and starts automaticly even if the computer shuts down (Linux only)")
@click.option("-z", "--zip", is_flag=True, flag_value=True, help="(optional) Will zip the client directory so it can be shared")
@click.option("-C", "--clean", is_flag=True, flag_value=True, help="Reverts back to a clean slate (THIS WILL REMOVE EVERYTHING THAT ISNT ALREADY IN THE REPO)")
@click.option("-L", "--local", is_flag=True, flag_value=True, help="Sets the config ip to your local address (Good for testing before using)")
@click.option("-V", "--version", is_flag=True, flag_value = version, help="Current version: " + str(version), )

def main(message, port, keygen, server, clean, version, code, local, zip):

    ip = rs.get_ip(local)

    if version:
        exit("Current version: ", str(version))
        

    # http://pioxy.ddns.net:3000/tibthink/minecraft-server/src/branch/main/init-server.py#L77
    if clean:
        print("Warning: Using --clean will remove everything that is not whitelisted.")
        con = input("Are you sure you want to continue?[y/N]: ") or "n"
        con += " "
        if con[0].lower() == "n":
            exit("Goodbye")

        item_list = [
            "config.json",
            "data.json",
            "__pycache__/",
            "client/",
            "client.zip"
        ]
        
        for item in item_list:
            try:
                if os.path.isfile(item):
                    os.remove(item)  # Remove file
                    print(f"File removed: {item}")
                elif os.path.isdir(item):
                    shutil.rmtree(item)  # Remove folder and its contents
                    print(f"Folder removed: {item}")
                else:
                    print(f"Path not found: {item}")
            except Exception as e:
                    print(f"Error while removing {item}: {e}")
        exit("All items have been completly obliterated")

    missing_arguments = []
    if message is None:
        missing_arguments.append('message')
    if port is None:
        missing_arguments.append('port')
    if keygen is None:
        missing_arguments.append('keygen')
    if code is None:
        missing_arguments.append('code')

    if missing_arguments:
        click.echo(f"Error: Missing argument(s): {', '.join(missing_arguments)}.")
        sys.exit(1)

    if keygen > 8:
        print("Warning: you are generating " + str(keygen) + " keys")
        print("It is highly suggested that you keep the key 8 digits or lower")
        con = input("Are you sure you want to continue with the conversion? [y/N] ") or "n"
        con += " "
        if con[0].lower() == "n":
            exit("Exiting reliqua")
    key = ""
    print("Generating key: ", end="")  # Print message without new line
    for i in range(keygen):
        digit = str(random.randint(1, 4))
        key += digit
        print(digit, end="")
    
    print("\r")

    converted = convert.translate(convert.key(key), message)
    hashed_code = hashed(code)
    
    data = {
        'message': converted,
        'code': hashed_code
    }

    config = {
        'ip': ip,
        'port': port,
        'key': key,
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)
# http://pioxy.ddns.net:3000/tibthink/minecraft-server/src/branch/main/init-server.py#L222
    folder_check = os.path.exists(pwd + "/client") 
    if not folder_check:
        path = os.path.join(pwd, "client")
        os.mkdir(path)

    shutil.copy2('reliqua_client.py', pwd + '/client', follow_symlinks=True)
    shutil.copy2('config.json', pwd + '/client', follow_symlinks=True)
    shutil.copy2("INSTRUCTIONS.md", pwd + '/client', follow_symlinks=True)
    
    if zip:
        print("zipping folder")
        shutil.make_archive("client/", 'zip', "client")
        print("folder zipped and ready to ship")
    else:
        print("Send the client folder in your directory to the target")    
    
    print("Remember to portforward port " + str(port)+ " on " + rs.get_ip(True))

    if server:
        if type_of_os == "windows":
            exit("Sorry, this feature is for linux based OS's")
        user = os.getlogin()
        open("reliqua.service", "w+").write("""[Unit]
Description=Reliqua server
After=network.target
[Service]
User=""" + user + """
Nice=1
KillMode=none
SuccessExitStatus=0 1
ProtectHome=true
ProtectSystem=full
PrivateDevices=true
NoNewPrivileges=true
WorkingDirectory=""" + pwd + """
ExecStart= /usr/bin/python3 """ + pwd +"""/reliqua_server.py
[Install]
WantedBy=multi-user.target
            """)
        shutil.copy2('reliqua.service', "/etc/systemd/system/", follow_symlinks=True)
        os.system("sudo systemctl daemon-reload")
        os.system("sudo systemctl start reliqua.service")
        os.system("sudo systemctl enable reliqua.service")
    else:
        rs.http_server(port, local)

if __name__ == '__main__':
    main()