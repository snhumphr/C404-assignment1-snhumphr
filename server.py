#  coding: utf-8 
import socketserver
import datetime
import pytz
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
        
        self.protocol = "HTTP/1.1 "
        
        self.crlf = "\r\n"          
        
        self.data = self.request.recv(1024).strip()
        #TODO: RECEIVE ALL THE REQUEST STUFF, UNTIL IT RETURNS A BLANK /r/l
        
        client_request = self.data.decode('utf-8').split(" ")
        
        method_type = client_request[0]
        
        filepath = client_request[1]
    
        if filepath[-1:] is "/":
            filepath = filepath + "index.html"        
        
        status_line, filepath = self.get_status_line(method_type, filepath)
            
        date = self.get_current_date()
        
        connection = self.get_connection()
        
        content = ""
        content_length = ""
        content_type = ""
        
        if "4" not in status_line: 
            content, content_length, content_type = self.get_file(filepath)
        
        response = self.consolidate_response(status_line, date, connection, content_length, content_type, content)

        self.request.sendall(bytearray(response,'utf-8'))
        
    def get_status_line(self, method_type, filepath):
        
        if "GET" not in method_type:
            return (self.protocol + "405 Method Not Allowed" + self.crlf, filepath)
        
        found = self.check_valid(filepath)
        new_filepath = filepath
        
        if found != 1:
            if found == 0:
                status = "404 Not Found"
            elif found == 2:
                status = "301 Moved Permanently"
                new_filepath = new_filepath + "/index.html"
        else:
            #handle properly
            status = "200 OK"
                    
        return (self.protocol + status + self.crlf, new_filepath)
    
    def get_current_date(self):
        date = datetime.datetime.now()
        date = date.astimezone(pytz.timezone("GMT"))
        date = date.strftime("%a, %d %b %Y %H:%M:%S")
        return "Date: " + date + " GMT" + self.crlf
    
    def get_connection(self):
        return "Connection: closed" + self.crlf
        
    def get_file(self, filepath):
        filedata = None
        f = open("./www" + filepath, "r")
        filedata = f.read()
        content = str(filedata)
        content_length = "Content-Length: " + str(len(content)) + self.crlf
        content_type = "Content-Type: " + "text/" + filepath.split(".")[-1:][0] + "; charset=utf-8" + self.crlf
        content = content + self.crlf
        #content_type = filepath.split(".")[-1:] + self.crlf
        #TODO: CHECK IF THE CONTENT LENGTH INCLUDES STUFF LIKE /r
        return (content, content_length, content_type)
    
    def check_valid(self, filepath):
        
        if path.exists("./www/" + filepath):
            norm_filepath = path.normpath("./www/" + filepath)
            if norm_filepath.split("/")[0] != "www":
                return 0
            if filepath[:-1] != "/" and "." not in filepath:
                if path.exists("./www/" + filepath + "/index.html"):
                    return 2
                else:
                    return 0
            else:
                return 1
        else:
            return 0
        
    def consolidate_response(self, status_line, date, connection, content_type, content_length, content):
        response = status_line + date + connection
        response = response + content_type + content_length
        response = response + self.crlf + content + self.crlf
        return response

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
