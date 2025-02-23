# reliqua2.0

## What is new in this version?

the locked timer and date feature never really worked. also isnt that secure \
so i scrapted it and its working on a code system \
it makes it easier (on my end) and more userfriendly

## How to use

```sh
tibthink@reliqua:~/reliqua2.0$ ./reliqua.py --help
Usage: reliqua.py [OPTIONS]

Options:
  -m, --message TEXT    Sets your message
  -p, --port INTEGER    Sets the port you want the server to run on
  -k, --keygen INTEGER  how many combinations do you want your message to have
  -c, --code TEXT       Set the code to unlock the message
  -s, --server          Runs the server in the backgroud and starts
                        automaticly even if the computer shuts down (Linux
                        only)
  -z, --zip             (optional) Will zip the client directory so it can be
                        shared
  -C, --clean           Reverts back to a clean slate (THIS WILL REMOVE
                        EVERYTHING THAT ISNT ALREADY IN THE REPO)
  -L, --local           Sets the config ip to your local address (Good for
                        testing before using)
  -V, --version         Current version: 2.1.6
  --help                Show this message and exit.

```

## Installing 

Ive made a script to do all the heavy lifiting. \
To use it type in the following command into the shell.
```sh
sudo ./setup.sh
```
Simple as that. if there are any errors please make a issue ticket and i will \
try to respond to it as soon as possible