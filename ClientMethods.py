from tkinter import filedialog, END

FORMAT = 'utf-8'
SEPARATOR = '<SEPARATOR>'
BUFFERSIZE = 2048


class ClientMethod:
    def __init__(self, ui, client_socket, client_names, name):
        self.ui = ui
        self.client_socket = client_socket
        self.client_names = client_names
        self.name = name

    def receive_msg(self, client_socket, name):
        client_socket.send(f'{"0"}{SEPARATOR}{"everyone"}{SEPARATOR}{name}{SEPARATOR}{name}'.encode())
        while True:
            try:
                #  Receive the message and decode.
                msg_recv = client_socket.recv(BUFFERSIZE).decode(FORMAT)
                split_message = msg_recv.split(SEPARATOR)

                #  See if the message is from server or another user
                if msg_recv.find(SEPARATOR) > -1:
                    if split_message[0] == '0':  # If text bit, write to client
                        self.accept_msg_from_client(split_message)
                    elif split_message[0] == '1':  # If file bit, ask user to save as and write to file.
                        self.read_write_file(split_message)
                else:
                    self.ui.display_message.insert(END, msg_recv)
            except OSError:
                break

    def accept_msg_from_client(self, text_message):
        print(text_message)
        #  All incoming message format {text_file bit}:{to}:{from}:{message}
        from_client = text_message[2]
        message = text_message[3]
        self.handle_client_names(from_client, self.client_names)
        self.ui.display_message.insert(END,
                                       '{}: {}'.format(from_client, message))

    def handle_client_names(self, client_name, client_names):
        if client_name not in client_names:
            client_names.append(client_name)
        self.ui.listbox.delete(0, END)
        for clients in client_names:
            self.ui.listbox.insert(END, clients)
        self.ui.listbox.select_set(0)
        self.ui.listbox.event_generate('<<ListboxSelect>>')

    def send_message(self):
        message = self.ui.msg.get()
        self.ui.msg.set('')
        recipient = self.ui.listbox.curselection()
        print(recipient)
        # if message != name:
        if recipient[0] != 0:
            self.ui.display_message.insert(END,
                                           '{}->PM->{}: {}'.format(self.name, self.ui.listbox.get(recipient[0]),
                                                                   message))
        else:
            self.ui.display_message.insert(END,
                                           '{}: {}'.format(self.name, message))
        for i in recipient:
            #  All incoming message format {text_file bit}:{to}:{from}:{message}
            message = f'{"0"}{SEPARATOR}{self.ui.listbox.get(i)}{SEPARATOR}{self.name}{SEPARATOR}{message}'
            self.client_socket.send(message.encode(FORMAT))

    def browse_files(self):
        filename = filedialog.askopenfilename(
            initialdir="/Users/jkom8/Desktop/final - chatting additions - kominsky",
            title="Select a File",
            filetypes=(("Text files",
                        "*.txt*"),
                       ("all files",
                        "*.*")))

        if not filename:
            return

        self.ui.file_search_button.configure(text="File Sent")
        self.send_file(filename)

    def send_file(self, filename):
        f = open(filename,
                 'r')
        data = f.read(BUFFERSIZE)
        print(data)

        recipient = self.ui.listbox.curselection()
        for i in recipient:
            while data:
                #  All incoming message format {text_file bit}:{to}:{from}:{message}
                message = f'{"1"}{SEPARATOR}{self.ui.listbox.get(i)}{SEPARATOR}{self.name}{SEPARATOR}{data}'
                self.client_socket.send(message.encode(FORMAT))
                data = f.read(BUFFERSIZE)
        self.ui.display_message.insert(END,
                                       'File sending completed.')

    def read_write_file(self, message):
        message = message[3]

        save_file = filedialog.asksaveasfilename(
            initialdir="/Users/jkom8/Desktop/final - chatting additions - kominsky",
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
        self.ui.display_message.insert(END,
                                       'The file has been saved.')
