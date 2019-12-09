import socket
import requests
import json
import os
import errno


class Client:
    def __init__(self, HOST, PORT):
        self.host = HOST
        self.port = PORT

    def sendMSG(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall('Hello, world'.encode('ascii'))
            data = s.recv(1024)
            print('Received', repr(data))
            data = s.recv(1024)
            print('response from boomi',repr(data))

    def print_config(self):
        print('Host: ' + str(self.host)+'\n')
        print('Port: ' + str(self.port)+'\n')


class Server:
    msg = None

    def __init__(self, HOST, PORT):
        self.host = HOST
        self.port = PORT

    @classmethod
    def postMSG(cls, URL, MSG):
        post_data = {'message': MSG}
        http_request = requests.post(url=URL, data=post_data)
        print('boomi server health',http_request)
        response = http_request.text
        return response

    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            while True:
                s.listen()
                conn, addr = s.accept()
                with conn:
                    try:
                        print('connected by:', addr)

                        self.msg = conn.recv(1024)
                        if self.msg is None:
                            received = 'no message data recieved'
                        else:
                            received= 'recieved'
                        client_msg = self.msg.decode()
                        print('sending message:'+client_msg+'\n')
                        print('message sent by client',client_msg)
                        # this is a response to the client socket
                        conn.sendall(received.encode('ascii'))
                        # now I need to post the data into Boomi using http
                        # using the class method postMSG
                        # need to get the post url from the config json
                        # read file and parse it
                        with open(os.path.dirname(__file__) + '/../config.json', 'r') as config_file:
                        
                            config_data = config_file.read()
                            json_obj = json.loads(config_data)

                            url = json_obj['URLs']['LocalHost']
                            print("post url: "+url)
                            response=Server.postMSG(URL=url, MSG=client_msg)
                            print('returning boomi response message: ',response)
                            
                            conn.sendall(response.encode('ascii'))

                    except IOError as e:
                        if e.errno == errno.EPIPE:
                            print("pipe error occured")
                            continue
