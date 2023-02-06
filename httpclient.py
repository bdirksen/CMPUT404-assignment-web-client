#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        code = data.split(' ')[1]
        if (code == "400" or code == "403"):
            print("------------------------------\nresponse: " + data)
        return int(data.split(' ')[1])

    def get_headers(self,data):
        return None

    def get_body(self, data):
        #print("------------------------------\nresponse: " + data)
        body = data.split('\r')[-1]
        #print("------------------------------\nbody: " + body)
        return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        # Parse the URL and get the host, port and path
        parsed = urllib.parse.urlparse(url)
        host = parsed.hostname
        port = parsed.port
        path = parsed.path
        if (path == ""):
            path = "/"
        if (port == None):
            port = 80
        # Connect to the server
        self.connect(host, port)
        host = host + ":" + str(port)
        request = "GET %s HTTP/1.1\n" % path + "Host: %s\n" % host + "Connection: close\n\n"
        request = "GET %s HTTP/1.1\n" % path + "Host: %s\n" % host + "Connection: close\n\n" 
        self.sendall(request)

        # Receive the response and return it 
        response = self.recvall(self.socket)
        self.close()
        return HTTPResponse(self.get_code(response), self.get_body(response))


    def POST(self, url, args=None):

        # Parse the URL
        parsed = urllib.parse.urlparse(url)
        host = parsed.hostname
        port = parsed.port
        path = parsed.path
        # Connect to the server
        self.connect(host, port)
        # Send the request
        if (args != None):
            # body is given
            body = urllib.parse.urlencode(args)
            request = "POST %s HTTP/1.1\n" % path + "Host: %s\n" % host + "Content-Type: application/x-www-form-urlencoded\n" + "Content-Length: %d\n" % len(body) + "Connection: close\n\n" + body
        else:
            # no body
            request = "POST %s HTTP/1.1\n" % path + "Host: %s\n" % host + "Content-Type: application/x-www-form-urlencoded\n" + "Content-Length: 0\n" + "Connection: close\n\n"
        self.sendall(request)
        # Receive the response
        response = self.recvall(self.socket)
        # Close the connection
        self.close()
        # Return the response
        return HTTPResponse(self.get_code(response), self.get_body(response))
    

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))