import socket
from ChatUI import ChatUI

client_socket = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM)

SERVER_ADDRESS = ('localhost', 30000)
print('Connecting to %s port %s' % SERVER_ADDRESS)
client_socket.connect(SERVER_ADDRESS)

print('Connected to remote host. You can start sending messages.')

name = input('Name: ')

client_names = ['everyone']
text_file = 0  # Creating a bit to tell if incoming data is file or chat message

UI = ChatUI(client_socket, name, client_names)
