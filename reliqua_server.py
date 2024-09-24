import random
import http.server
import socketserver
import requests    
import socket
import json



def dump(file, object):
    output = json.load(open(file))
    data = json.dumps(output[object])
    return data

def get_ip(local=False):
    if not local:
        endpoint = 'https://ipinfo.io/json'
        response = requests.get(endpoint, verify = True)

        if response.status_code != 200:
            return 'Status:', response.status_code, 'ERROR. Exiting.'
            
        data = response.json()

        return data['ip']

    else:
        # https://thewebdev.info/2022/04/07/how-to-find-local-ip-addresses-using-python/
        # Its used to give your actually ip and you would be able to connect to the server outside your network but 
        # its refusing to connect to the server outside
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

def http_server(port):
    handling_it_like_its_1924 = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer((get_ip(True), int(port)), handling_it_like_its_1924) as httpd:
        print("serving on: " + get_ip(True) + ":" + str(port))
        httpd.serve_forever()


if __name__ == '__main__':
    http_server(dump('config.json', 'port'))
