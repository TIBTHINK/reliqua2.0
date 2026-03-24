# How to use

## Windows(beta)
0. For some god known reason, making a script to setup this program in windows just doesnt seems to work \
so here are the instuctions on how to install the required dependencies

1. Download [python3](https://www.python.org/ftp/python/3.13.5/python-3.13.5-amd64.exe) and install it

2. in the folder that you were given run the following command
```cmd
C:\Users\tibthink\reliqua2.0\client\python3 -m pip install -r .\requirements.txt
```
if everything goes right you should be able to continue to step...

2. in a new command prompt(unless python3 was already installed) run this command to run the main program
```cmd
C:\Users\tibthink\reliqua2.0> python3 reliqua_client.py
```
3. the script should run after that, it will prompt you with a password, \
if you do not have the password, ask the person who sent you this and \
request the password.

## Linux/MacOS
1. open a terminal run the following command (you need sudo/root to run this)
```sh
tibthink@hal:~/reliqua2.0$ sudo ./setup.sh
```
2. after that has completed succesfully you are now ready too run the script \
by running the following command
```sh
tibthink@hal:~/reliqua2.0$ python3 reliqua_client.py
```
3. the script should run after that, it will prompt you with a password, \
if you do not have the password, ask the person who sent you this and \
request the password.