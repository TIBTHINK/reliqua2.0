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
version = "2.1.3"

if system == "Windows":
    type_of_os = "windows"
else:
    type_of_os = "unix"

class convert:
    def b64(string):
        return base64.b64encode(bytearray(string, 'ascii')).decode('utf-8')

    def ascii(string):
        ascii_out = []
        for i in string:
            ascii_out.append(str(ord(i)))
        output = " "
        # convert to string
        return output.join(ascii_out)

    def binary(string):
        return ' '.join(format(ord(x), 'b') for x in string)

    def key(key):
        key_out = []
        for i in key:
            key_out.append(int(i))
        return key_out

    def translate(list, message):
        count = 0
        for i in range(len(list)):
            # print(list[i])
            if list[i] == 1:
                message = convert.b64(message)
                count = count + 1
            elif list[i] == 2:
                message = convert.ascii(message)
                count = count + 1
            elif list[i] == 3:
                message = convert.binary(message)
                count = count + 1
            else:
                return print("ERROR: Key out of range")
        return(message)
    
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
@click.option("-s", "--server", is_flag=False, flag_value=True, help="Runs the server in the backgroud and starts automaticly even if the computer shuts down (Linux only)")
@click.option("-C", "--clean", is_flag=True, flag_value=True, help="Reverts back to a clean slate (THIS WILL REMOVE EVERYTHING THAT ISNT ALREADY IN THE REPO)")
@click.option("-V", "--version", is_flag=True, flag_value = version, help="Current version: " + str(version), )

def main(message, port, keygen, server, clean, version, code):
    
    if version:
        print("Current version: ", str(version))
        exit()

    # http://pioxy.ddns.net:3000/tibthink/minecraft-server/src/branch/main/init-server.py#L77
    if clean:
        print("Warning: Using --clean will remove everything that is not whitelisted.")
        con = input("Are you sure you want to continue?[y/N]: ") or "n"
        con += " "
        if con[0].lower() == "n":
            exit("Goodbye")

        filenames = os.listdir("./")
        dont_remove_these_files = ["data.json", "config.json", "./client", "./__pycache__"]
        print("###Removing needed files from delete list###")
        for i in dont_remove_these_files:
            if i in filenames:
                filenames.remove(i)

        directory = next(os.walk("./"))[1]
        directory.remove(".git")
  
        try:
            for i in directory:
                print("Removing: " + i)
                shutil.rmtree(i)
            for i in filenames:
                print("Removing: " + i)
                os.remove(i)
        except OSError as e:
                print("Error: %s : %s" % (directory, e.strerror))

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
        digit = str(random.randint(1, 3))
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
        rs.http_server(port)

if __name__ == '__main__':
    main()