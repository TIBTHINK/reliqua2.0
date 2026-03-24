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
import zipfile
import base64
import subprocess

ip = rs.get_ip()
pwd = os.getcwd()
system = platform.system()
version = "2.3.0"

if system == "Windows":
    type_of_os = "windows"
elif system == "darwin":
    type_of_os = "darwin"
else:
    type_of_os = "unix"



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
            elif list[i] == 5:
                message = convert.octal(message)
                count += 1    
            else:
                return print("ERROR: Key out of range")
        return message
    
class compile:
    def get_resource_path(filename):
        if getattr(sys, 'frozen', False):
            # Running as compiled binary
            base_path = os.path.dirname(sys.executable)
        else:
            # Running as normal Python
            base_path = os.path.dirname(__file__)

        return os.path.join(base_path, filename)

    def compile_client():
        print("Compiling reliqua_client.py with Nuitka...")

        try:
            subprocess.run([
                sys.executable, "-m", "nuitka",
                "--onefile",
                "--standalone",
                "--follow-imports",
                "--include-data-files=config.json=config.json",
                "reliqua_client.py"
            ], check=True)

            print("Compilation successful!")

        except subprocess.CalledProcessError:
            print("Compilation failed")
    
def hashed(password):
    # Create a hash using SHA-256
    hash_obj = hashlib.sha256(password.encode())
    hashed_password = hash_obj.hexdigest()
    return hashed_password

def zip_folder(folder_path, output_filename):
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)



@click.command()
@click.option("-m", "--message", help="Sets your message")
@click.option("-p", "--port", default=8080, help="Sets the port you want the server to run on")
@click.option("-k", "--keygen", default=8, help="how many combinations do you want your message to have")
@click.option("-c", "--code", help="Set the code to unlock the message")
@click.option("-H", "--hint", default="No hint was provided", help="Sets a hint for what the code might be")
# @click.option("-s", "--server", is_flag=True, flag_value=True, help="Runs the server in the backgroud and starts automaticly even if the computer shuts down (Linux only)")
@click.option("--compile", is_flag=True, flag_value=True, help="(optional) Compiles the client into a binary using Nuitka")
@click.option("-z", "--zip", is_flag=True, flag_value=True, help="(optional) Will zip the client directory so it can be shared")
@click.option("-C", "--clean", is_flag=True, flag_value=True, help="Reverts back to a clean slate (THIS WILL REMOVE EVERYTHING THAT ISNT ALREADY IN THE REPO)")
@click.option("-L", "--local", is_flag=True, flag_value=True, help="Sets the config ip to your local address (Good for testing before using)")
@click.option("-D", "--ddns", help="(optional) use a domain name instead of an ip (Advanced users only)")
@click.option("-V", "--version", is_flag=True, flag_value = version, help="Current version: " + str(version), )

def main(message, port, keygen, clean, version, code, hint, local, zip , ddns, compile):

    if hint is None:
        hint = "No hint was provided"
        
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
        digit = str(random.randint(1, 5))
        key += digit
        print(digit, end="")
    
    print("\r")

    converted = convert.translate(convert.key(key), message)
    hint_encoded = convert.translate(convert.key(key), hint)
    hashed_code = hashed(code)
    if ddns:
        ip = ddns
        print("Using ddns: " + str(ddns) + " instead of ip")
        
    data = {
        'message': converted,
        'code': hashed_code,
        'hint': hint_encoded
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
    compile.compile_client_with_config()

    with open(compile.get_resource_path('config.json'), "r") as f:
        config = json.load(f)

    
# http://pioxy.ddns.net:3000/tibthink/minecraft-server/src/branch/main/init-server.py#L222
    folder_check = os.path.exists(pwd + "/client") 
    if not folder_check:
        path = os.path.join(pwd, "client")
        os.mkdir(path)


    if not compile:
        shutil.copy2('reliqua_client.py', pwd + '/client', follow_symlinks=True)
        shutil.copy2('config.json', pwd + '/client', follow_symlinks=True)
        shutil.copy2("INSTRUCTIONS.html", pwd + '/client', follow_symlinks=True)
        shutil.copy2("setup.sh", pwd + '/client' ,follow_symlinks=True)
    else:
        exe_name = "reliqua_client.exe" if os.name == "nt" else "reliqua_client"
        if os.path.exists(exe_name):
            shutil.move(exe_name, os.path.join("client", exe_name))
    # shutil.copy2("setup.bat", pwd + '/client' ,follow_symlinks=True)

    
    if zip:
        print("zipping folder")
        zip_folder("./client", "client.zip")
        print("folder zipped and ready to ship")
        shutil.copy2("client.zip", pwd + '/client' , follow_symlinks=True)
    else:
        print("Send the client folder in your directory to the target") 
    
    print("Remember to port forward port " + str(port)+ " on " + rs.get_ip(local))
    rs.http_server(port, local)
#     
if __name__ == '__main__':
    main()