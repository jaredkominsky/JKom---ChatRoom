""" Main file for Server

ChatServer.py creates the socket to open the server. The server
is then connected to the port through ServerMethods.py.
"""

import socket

from ServerMethods import start_server

clients = []
names = ['everyone']


#  Create the server
server = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)
SERVER_ADDRESS = ('localhost',
                  30000)
server.bind(SERVER_ADDRESS)

start_server(SERVER_ADDRESS,
             server,
             names,
             clients)
