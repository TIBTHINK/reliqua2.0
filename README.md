# reliqua2.0

## What is new in this version?

the locked timer and date feature never really worked. also isnt that secure \
so i scrapted it and its working on a code system \
it makes it easier (on my end) and more userfriendly

## How to use

```sh
tibthink@reliqua:~/reliqua2.0$ python3 reliqua.py --help
Usage: reliqua.py [OPTIONS]

Options:
  -m, --message TEXT    Sets your message
  -p, --port INTEGER    Sets the port you want the server to run on
  -k, --keygen INTEGER  how many combinations do you want your message to have
  -c, --code TEXT       Set the code to unlock the message
  -s, --server TEXT     Runs the server in the backgroud and starts
                        automaticly even if the computer shuts down (Linux
                        only)
  -C, --clean           Reverts back to a clean slate (THIS WILL REMOVE
                        EVERYTHING THAT ISNT ALREADY IN THE REPO)
  -V, --version         Current version: 2.0.1
  --help                Show this message and exit.

```