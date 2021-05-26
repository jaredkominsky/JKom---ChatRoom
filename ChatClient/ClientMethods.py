"""ClientMethods.py holds the methods the client requires.

UI imports methods from ClientMethods. Buttons on the UI
utilize these methods in order to facilitate message and
file transfers.
"""

from tkinter import filedialog, END

FORMAT = 'utf-8'
SEPARATOR = '<SEPARATOR>'
BUFFERSIZE = 2048


def receive_msg(client_socket, client_names, name, display, listbox):
    """Target of UI thread that continuously waits for incoming messages.

    Parameters
    ----------
    :param client_socket: Socket that holds client connection information.
    :param listbox: UI listbox that holds current chatroom user's information.
    :param display: UI display that will display the messages.
    :param name: Name of the user.
    :param client_names: Names of all users in the chatroom.
    """
    client_socket.send(f'{"0"}{SEPARATOR}{"everyone"}{SEPARATOR}{name}{SEPARATOR}{name}'.encode())
    while True:
        try:
            #  Receive the message and decode.
            msg_recv = client_socket.recv(BUFFERSIZE).decode(FORMAT)
            split_message = msg_recv.split(SEPARATOR)

            #  See if the message is from server or another user
            if msg_recv.find(SEPARATOR) > -1:
                if split_message[0] == '0':  # If text bit, write to client
                    accept_msg_from_client(split_message, client_names, display, listbox)
                elif split_message[0] == '1':  # If file bit, ask user to save as and write to file.
                    read_write_file(split_message, display)
            else:
                display.insert(END, msg_recv)
        except OSError:
            break


def accept_msg_from_client(text_message, client_names, display, listbox):
    """Receives and displays the messages from other users.

    :param listbox:
    :param display:
    :param client_names:
    :param text_message
    """
    print(text_message)
    #  All incoming message format {text_file bit}:{to}:{from}:{message}
    from_client = text_message[2]
    message = text_message[3]
    handle_client_names(from_client, client_names, listbox)
    display.insert(END,
                   '{}: {}'.format(from_client, message))


def handle_client_names(client_name, client_names, listbox):
    """Method to update listbox with users who are currently in chat.

    This method takes the name of the user who sent the most recent message.
    If the user is not already listed, user is added to the listbox.

    :param client_name: The user's name who sent the message
    :param client_names: Array that stores the users' names
    :param listbox: UI listbox that displays the user names
    """
    if client_name not in client_names:
        client_names.append(client_name)
    listbox.delete(0, END)
    for clients in client_names:
        listbox.insert(END, clients)
    listbox.select_set(0)
    listbox.event_generate('<<ListboxSelect>>')


def send_message(msg, listbox, display, name, client_socket):
    """Sends message to the server.

    Analyses if message is sent as private or group.
    If private, shows message as ->PM-> to portray Private Message.
    Else, prints the message normally in the display box.

    :param msg: the UI msg input box
    :param listbox: UI listbox that displays users' names
    :param display: UI display box that displays messages
    :param name:L user's name
    :param client_socket: user's individual socket
    """
    message = msg.get()
    msg.set('')
    recipient = listbox.curselection()
    print(recipient)
    # if message != name:
    if recipient[0] != 0:
        display.insert(END,
                       '{}->PM->{}: {}'.format(name, listbox.get(recipient[0]),
                                               message))
    else:
        display.insert(END,
                       '{}: {}'.format(name, message))
    for i in recipient:
        #  All incoming message format {text_file bit}:{to}:{from}:{message}
        message = f'{"0"}{SEPARATOR}{listbox.get(i)}{SEPARATOR}{name}{SEPARATOR}{message}'
        client_socket.send(message.encode(FORMAT))


def browse_files(listbox, display, client_socket, name):
    """Opens the file explorer for user to select what file to send.

    :param listbox: UI listbox that displays users' names
    :param display: UI display box that displays messages
    :param client_socket: user's individual socket
    :param name: user's names
    """
    filename = filedialog.askopenfilename(
        initialdir="/Users",
        title="Select a File",
        filetypes=(("Text files",
                    "*.txt*"),
                   ("all files",
                    "*.*")))

    if not filename:
        return

    send_file(filename,
              listbox,
              display,
              client_socket,
              name)


def send_file(filename, listbox, display, client_socket, name):
    """Sends the file to the server.

    :param filename: filedialogue file name
    :param listbox: UI listbox that displays users' names
    :param display: UI display box that displays messages
    :param client_socket: user's individual socket
    :param name: user's names
    """
    f = open(filename,
             'r')
    data = f.read(BUFFERSIZE)
    print(data)

    recipient = listbox.curselection()
    for i in recipient:
        while data:
            #  All incoming message format {text_file bit}:{to}:{from}:{message}
            message = f'{"1"}{SEPARATOR}{listbox.get(i)}{SEPARATOR}{name}{SEPARATOR}{data}'
            client_socket.send(message.encode(FORMAT))
            data = f.read(BUFFERSIZE)
    display.insert(END,
                   'File sending completed.')


def read_write_file(message, display):
    """This method takes data sent from the server and writes it to a new file.

    First, this method asks the user where they would like to save the incoming
    file. The file is then written and saved to the location.

    :param message: data of file
    :param display: UI display box that displays the message.
    """
    message = message[3]

    save_file = filedialog.asksaveasfilename(
        initialdir="/Users",
        title="Where would you like to save the file",
        filetypes=(("Text files",
                    "*.txt*"),
                   ("all files",
                    "*.*")))

    if not save_file:
        return

    f = open(save_file + '.txt',
             'w')
    f.write(message)
    display.insert(END,
                   'The file has been saved.')
