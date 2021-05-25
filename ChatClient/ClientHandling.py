"""ClientHandling.py starts each client.

This controls the start of the client program.
Each client runs this script which requests the login name
of the user. Once the user has put in their name, the
client sends the name to the server and starts the UI.
"""

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

UI = ChatUI(client_socket, name, client_names)
