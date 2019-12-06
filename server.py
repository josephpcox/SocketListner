from classes.network import Server
import json
# read file and parse it
with open('config.json','r') as config_file:
    config_data = config_file.read()
    json_obj = json.loads(config_data)

# show values
print("host: " + str(json_obj['routing']['HOST']))
print("port: " + str(json_obj['routing']['PORT']))
HOST = str(json_obj['routing']['HOST'])
PORT = int(json_obj['routing']['PORT'])
print('/................................./\n')
socket_server = Server(HOST,PORT)
socket_server.listen()
