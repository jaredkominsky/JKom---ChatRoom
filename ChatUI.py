from threading import Thread
from tkinter import *
from tkinter import filedialog

import ClientMethods


class ChatUI:

    def __init__(self, name, client_names):
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
        self.input_field.bind(ClientMethods.send_message())
        self.input_field.pack()
        self.send_button = Button(self.root,
                                  text="Send",
                                  command=ClientMethods.send_message())
        self.send_button.pack()

        self.listbox = Listbox(self.root, exportselection=False)
        self.listbox.pack(side=LEFT)
        self.listbox.insert(END,
                            'everyone')
        self.listbox.select_set(0)
        self.listbox.event_generate('<<ListboxSelect>>')

        self.file_search_button = Button(self.root,
                                         text='Select a File',
                                         command=ClientMethods.browse_files())
        self.file_search_button.pack()

        Thread(target=ClientMethods.receive_msg(name, client_names)).start()

        mainloop()
