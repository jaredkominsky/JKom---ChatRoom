"""Method file that holds all methods for the server."""

from threading import *

FORMAT = "utf-8"
BUFFERSIZE = 2048
SEPARATOR = '<SEPARATOR>'


def broadcast_data(message, conn, clients):
    """Takes received data and sends them to all clients listed
    in clients.

    :param message: Data that was received and to be sent.
    :param conn: Server socket
    :param clients: List of client sockets.
    """
    for client in clients:
        if client != conn:
            client.send(message.encode(FORMAT))


def handle_client(conn, names, clients):
    """Infinite while that continuously waits for incoming data and clients.

    Target of server thread. This loop infinitely waits for new messages
    to be received. The method then analyses if the message is meant as a
    private message or group and send the data out accordingly.

    :param conn: Server socket
    :param names: list of names that are related to the clients
    :param clients:  list of client sockets
    """
    conn_open = True

    while conn_open:
        msg_recv = conn.recv(BUFFERSIZE).decode(FORMAT)

        #  Check if message is sent to everyone or an individual
        #  All incoming message format {text_file bit}:{to}:{from}:{message}
        split_message = msg_recv.split(SEPARATOR)
        to_client = split_message[1]
        message = split_message[3]
        if to_client != 'everyone':
            message = message
            individual_client_index = names.index(to_client) - 1  # must account for the server in names 'everyone'
            individual_client_conn = clients[individual_client_index]
            text_file = split_message[0]
            from_client = split_message[2]
            message_to_send = f'{text_file}{SEPARATOR}{to_client}{SEPARATOR}{from_client}{SEPARATOR}[{message}]'
            individual_client_conn.send(message_to_send.encode(FORMAT))
        else:
            broadcast_data(msg_recv, conn, clients)

    conn.close()


# def handle_file_share(file_data):


def start_server(server_address, server, names, clients):
    """Starts the server connection and waits for new incoming clients.

    This method connects the socket to the server and starts an infinite
    loop that awaits incoming connection. Once a new connection is established,
    The server stores the socket and client name in their respective lists.
    A new thread is created for each client waiting for their incoming data.

    :param server_address: IP and port of server connection
    :param server: the server socket
    :param names: list of names relating to each socket
    :param clients: list of client sockets
    """
    print('Chat session successfully connected on: ' + server_address[0])

    server.listen()
    while True:
        connection, client_address = server.accept()

        name = connection.recv(BUFFERSIZE).decode(FORMAT).split(SEPARATOR)[3]

        names.append(name)

        print('New connection with {}'.format(name))
        clients.append(connection)

        broadcast_data(('{} has joined the chat.\r\n'.format(name)), connection, clients)

        connection.send('Welcome to the chat!\r\n'.encode(FORMAT))
        connection.send('Remember to select who you want the message to be sent to! '.encode(FORMAT))
        # connection.send('If the message is in "[]", than you received a private message!'.encode(FORMAT))

        client_thread = Thread(target=handle_client, args=(connection, names, clients))
        client_thread.start()
