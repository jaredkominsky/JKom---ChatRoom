from threading import *

FORMAT = "utf-8"
BUFFERSIZE = 2048
SEPARATOR = '<SEPARATOR>'


def broadcast_message(message, conn, clients):
    for client in clients:
        if client != conn:
            client.send(message.encode(FORMAT))


def handle_client(conn, names, clients):
    conn_open = True

    while conn_open:
        msg_recv = conn.recv(BUFFERSIZE).decode(FORMAT)

        #  Check if message is sent to everyone or an individual
        #  All incoming message format {text_file bit}:{to}:{from}:{message}
        split_message = msg_recv.split(SEPARATOR)
        text_file = split_message[0]
        to_client = split_message[1]
        from_client = split_message[2]
        message = split_message[3]
        if to_client != 'everyone':
            message = message
            individual_client_index = names.index(to_client) - 1  # must account for the server in names 'everyone'
            individual_client_conn = clients[individual_client_index]
            message_to_send = f'{text_file}{SEPARATOR}{to_client}{SEPARATOR}{from_client}{SEPARATOR}[{message}]'
            individual_client_conn.send(message_to_send.encode(FORMAT))
        else:
            broadcast_message(msg_recv, conn, clients)

    conn.close()


# def handle_file_share(file_data):


def start_server(server_address, server, names, clients):
    print('Chat session successfully connected on: ' + server_address[0])

    server.listen()
    while True:
        connection, client_address = server.accept()

        name = connection.recv(BUFFERSIZE).decode(FORMAT).split(SEPARATOR)[3]

        names.append(name)

        print('New connection with {}'.format(name))
        clients.append(connection)

        broadcast_message(('{} has joined the chat.\r\n'.format(name)), connection, clients)

        connection.send('Welcome to the chat!\r\n'.encode(FORMAT))
        connection.send('Remember to select who you want the message to be sent to! '.encode(FORMAT))
        # connection.send('If the message is in "[]", than you received a private message!'.encode(FORMAT))

        client_thread = Thread(target=handle_client, args=(connection, names, clients))
        client_thread.start()
