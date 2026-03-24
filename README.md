# Reliqua2.0

## What is new in this version?

The locked timer and date feature never really worked. Also, it isn't that secure, \
so I scrapped it, and it's now working on a code system. \
It makes it easier (on my end) and more user-friendly. 

## Features
* Message supports multi-line messages
* Converts messages from 5 different encodings
* The code word is encrypted by a hash
* The hint is also encoded with the same key as the message
* Zips all the required files into a file (if wanted)
* For testing, you can change the link IP to local

## How to use

```sh
tibthink@reliqua:~/reliqua2.0$ ./reliqua.py --help
Usage: reliqua.py [OPTIONS]

Options:
  -m, --message TEXT    Sets your message
  -p, --port INTEGER    Sets the port you want the server to run on
  -k, --keygen INTEGER  how many combinations do you want your message to have
  -c, --code TEXT       Set the code to unlock the message
  -H, --hint TEXT       Sets a hint for what the code might be
  -z, --zip             (optional) Will zip the client directory so it can be
                        shared
  -C, --clean           Reverts back to a clean slate (THIS WILL REMOVE
                        EVERYTHING THAT ISNT ALREADY IN THE REPO)
  -L, --local           Sets the config ip to your local address (Good for
                        testing before using)
  -V, --version         Current version: 2.2.1
  --help                Show this message and exit.
```

## Installing Linux

I've made a script to do all the heavy lifting. \
To use it, type the following command into the shell:
```sh
sudo ./setup.sh
```
Simple as that. If there are any errors, please make an issue ticket and I will \
try to respond to it as soon as possible.

## Installing Windows (Beta)
0. For some god-known reason, making a script to set up this program on Windows just doesn’t seem to work,
so here are the instructions on how to install the required dependencies: 

1. Download [Python3](https://www.python.org/ftp/python/3.13.5/python-3.13.5-amd64.exe)

2. In the folder that you were given, run the following command:
```cmd
C:\Users\tibthink\reliqua2.0> python3 -m pip install -r .\requirements.txt
```
If everything goes right, you should be able to continue to step...

## Usage
1. In a new Command Prompt (unless Python3 was already installed), run this command to run the main program. \
Regardless of OS, the command is the same:

```cmd
C:\Users\tibthink\reliqua2.0> python3 reliqua.py -m "hello world" -p 8080 -k 8 -c "goodbye" -H "opposite of hello" -z
```
2. Make sure that you port forward your IP with the correct port. \
If you don't know how, there are [many](https://www.noip.com/support/knowledgebase/general-port-forwarding-guide) resources to find out how to.