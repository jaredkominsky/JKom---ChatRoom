from threading import Thread
from tkinter import *

from ClientMethods import ClientMethod


class ChatUI:

    def __init__(self, client_socket, name, client_names):
        handler = ClientMethod(self, client_socket, client_names, name)
        self.root = Tk()
        self.root.title("Chat Client")

        self.display_window = Frame(self.root)
        self.msg = StringVar()
        self.msg.set("Type your messages here.")
        self.scrollbar = Scrollbar(self.display_window)
        self.display_message = Listbox(self.display_window,
                                       height=15,
                                       width=100,
                                       yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=RIGHT,
                            fill=Y)
        self.display_message.pack(side=LEFT,
                                  fill=BOTH)
        self.display_message.pack()
        self.display_window.pack()

        self.input_field = Entry(self.root,
                                 textvariable=self.msg)
        self.input_field.bind(handler.send_message())
        self.input_field.pack()
        self.send_button = Button(self.root,
                                  text="Send",
                                  command=handler.send_message())
        self.send_button.pack()

        self.listbox = Listbox(self.root, exportselection=False)
        self.listbox.pack(side=LEFT)
        self.listbox.insert(END,
                            'everyone')
        self.listbox.select_set(0)
        self.listbox.event_generate('<<ListboxSelect>>')

        self.file_search_button = Button(self.root,
                                         text='Select a File',
                                         command=handler.browse_files())
        self.file_search_button.pack()

        Thread(target=handler.receive_msg(name, client_names)).start()

        mainloop()
