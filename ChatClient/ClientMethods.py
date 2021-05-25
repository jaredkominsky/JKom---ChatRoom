from tkinter import filedialog, END

FORMAT = 'utf-8'
SEPARATOR = '<SEPARATOR>'
BUFFERSIZE = 2048


def receive_msg(client_socket, client_names, name, display, listbox):
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
    print(text_message)
    #  All incoming message format {text_file bit}:{to}:{from}:{message}
    from_client = text_message[2]
    message = text_message[3]
    handle_client_names(from_client, client_names, listbox)
    display.insert(END,
                   '{}: {}'.format(from_client, message))


def handle_client_names(client_name, client_names, listbox):
    if client_name not in client_names:
        client_names.append(client_name)
    listbox.delete(0, END)
    for clients in client_names:
        listbox.insert(END, clients)
    listbox.select_set(0)
    listbox.event_generate('<<ListboxSelect>>')


def send_message(msg, listbox, display, name, client_socket):
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
    filename = filedialog.askopenfilename(
        #  initialdir="/Users/jkom8/Desktop/final - chatting additions - kominsky",
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
    message = message[3]

    save_file = filedialog.asksaveasfilename(
        #  initialdir="/Users/jkom8/Desktop/final - chatting additions - kominsky",
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
