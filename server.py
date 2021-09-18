#  coding: utf-8 
import socketserver
from os import path

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        
        client_request = self.data.decode('utf-8').split(" ")
        print("This is the client request: ", client_request)
        
        #TODO: handle requests other then GET here
        
        filepath = client_request[1]
        
        print("This is the filepath: \"" + filepath + "\"")
        
        status_line = self.get_status_line(filepath)
            
        self.request.sendall(bytearray(status_line,'utf-8'))
        
    def get_status_line(self, filepath):
        found = self.check_valid(filepath)
        
        if not found:
            #check if this can be fixed with a 301 redirect
            pass
            #if it can't, then throw a 404 error here
            status = "404 Not Found"
        else:
            #handle properly
            status = "200 OK"
            
        return "HTTP/1.1 " + status
    
        
    def get_file(self, filepath):
        filedata = None
        f = open("./www/" + filepath, "r")
        filedata = f.read()
        return str(filedata)
    
    def check_valid(self, filepath):
        if path.exists("./" + filepath):
            return True
        else:
            return False 

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
