from classes.network import Client
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

# client sends msg to server and then recieves msg
print('printing server object\n')
send = Client(HOST,PORT)
send.print_config()

toSend = input("send message (y/any key to quite): ")
while toSend == 'y':
    msg=str(input("please enter the message you want sent:"))
    send.sendMSG(msg)
    toSend = input("send message (y/any key to quite): ")

print('\nGood Bye')


