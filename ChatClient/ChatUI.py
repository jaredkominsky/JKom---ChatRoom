"""This class creates the UI for each individual client.

The UI is designed and created once the class is instantiated. Each instance then connected the buttons
with methods in ClientMethods.py to run the functionalities that are required.
"""

from threading import Thread
import tkinter as tk
import tkinter.font as tk_font

from ClientMethods import *


# class ChatUI:
#     """Class that creates and starts the UI
#
#     Class inherits methods from ClientMethods.py. The UI is created,
#     bound to ClientMethod.py methods.
#     """

#     def __init__(self, client_socket, name, client_names):
#         """Constructor for ChatUI.
#
#         Sets up and runs the UI.
#
#         :param self: self object
#         :param client_socket: user's individual sockets
#         :param name: user's name
#         :param client_names: list of all users in the chat
#         """
#
#         self.root = tk.Tk()
#         self.root.title("Chat Client")
#
#         self.display_window = tk.Frame(self.root)
#
#         self.scrollbar = tk.Scrollbar(self.display_window)
#         self.display_message = tk.Listbox(self.display_window,
#                                           height=15,
#                                           width=100,
#                                           yscrollcommand=self.scrollbar.set)
#         self.scrollbar.pack(side=tk.RIGHT,
#                             fill=tk.Y)
#         self.display_message.pack(side=tk.LEFT,
#                                   fill=tk.BOTH)
#         self.display_message.pack()
#         self.display_window.pack()
#
#         self.msg = tk.StringVar()
#         self.msg.set("Type your messages here.")
#
#         self.listbox = tk.Listbox(self.root, exportselection=False)
#         self.listbox.pack(side=tk.LEFT)
#         self.listbox.insert(END,
#                             'everyone')
#         self.listbox.select_set(0)
#         self.listbox.event_generate('<<ListboxSelect>>')
#
#         self.input_field = tk.Entry(self.root,
#                                     textvariable=self.msg)
#         self.input_field.bind(lambda: send_message(self.msg,
#                                                    self.listbox,
#                                                    self.display_message,
#                                                    name,
#                                                    client_socket))
#         self.input_field.pack()
#
#         self.send_button = tk.Button(self.root,
#                                      text="Send",
#                                      command=lambda: send_message(self.msg,
#                                                                   self.listbox,
#                                                                   self.display_message,
#                                                                   name,
#                                                                   client_socket))
#         self.send_button.pack()
#
#         self.file_search_button = tk.Button(self.root,
#                                             text='Select a File',
#                                             command=lambda: browse_files(self.listbox,
#                                                                          self.display_message,
#                                                                          client_socket,
#                                                                          name))
#         self.file_search_button.pack()
#
#         Thread(target=lambda: receive_msg(client_socket,
#                                           client_names,
#                                           name,
#                                           self.display_message,
#                                           self.listbox)).start()
#
#         tk.mainloop()


class ChatUI:
    """Class that creates and starts the UI

    Class inherits methods from ClientMethods.py. The UI is created,
    bound to ClientMethod.py methods.
    """

    def __init__(self, client_socket, name, client_names):
        """Constructor for ChatUI.

            Sets up and runs the UI.

            :param self: self object
            :param client_socket: user's individual sockets
            :param name: user's name
            :param client_names: list of all users in the chat
            """

        self.root = tk.Tk()
        self.root.title("Chat Client")
        self.root.geometry("88x20")
        self.root.resizable(width=False, height=False)

        self.scrollbar = tk.Scrollbar(self.root)
        self.display_message = tk.Listbox(self.root,
                                          yscrollcommand=self.scrollbar.set)
        self.display_message["borderwidth"] = "1px"
        ft = tk_font.Font(family='Times', size=10)
        self.display_message["font"] = ft
        self.display_message["fg"] = "#333333"
        self.display_message["justify"] = "center"
        self.display_message.place(x=0, y=0, width=450, height=320)
        self.display_message["setgrid"] = "True"

        self.participant_listbox = tk.Listbox(self.root)
        self.participant_listbox["borderwidth"] = "1px"
        ft = tk_font.Font(family='Times', size=10)
        self.participant_listbox["font"] = ft
        self.participant_listbox["fg"] = "#333333"
        self.participant_listbox["justify"] = "center"
        self.participant_listbox.place(x=450, y=0, width=150, height=350)
        self.participant_listbox.insert(END,
                                        'everyone')
        self.participant_listbox.select_set(0)
        self.participant_listbox.event_generate('<<ListboxSelect>>')

        self.msg = tk.StringVar()
        self.msg.set("Type your messages here.")

        self.input_field = tk.Entry(self.root,
                                    textvariable=self.msg)
        self.input_field["borderwidth"] = "1px"
        ft = tk_font.Font(family='Times', size=10)
        self.input_field["font"] = ft
        self.input_field["fg"] = "#333333"
        self.input_field["justify"] = "center"
        self.input_field.place(x=130, y=320, width=240, height=30)

        self.send_button = tk.Button(self.root)
        self.send_button["bg"] = "#efefef"
        ft = tk_font.Font(family='Times', size=10)
        self.send_button["font"] = ft
        self.send_button["fg"] = "#000000"
        self.send_button["justify"] = "center"
        self.send_button["text"] = "Send"
        self.send_button.place(x=370, y=320, width=80, height=30)
        self.send_button["command"] = lambda: send_message(self.msg.get(),
                                                           self.participant_listbox,
                                                           self.display_message,
                                                           name,
                                                           client_socket)

        self.file_search_button = tk.Button(self.root)
        self.file_search_button["bg"] = "#efefef"
        ft = tk_font.Font(family='Times', size=10)
        self.file_search_button["font"] = ft
        self.file_search_button["fg"] = "#000000"
        self.file_search_button["justify"] = "center"
        self.file_search_button["text"] = "Search for File"
        self.file_search_button.place(x=0, y=320, width=128, height=30)
        self.file_search_button["command"] = lambda: browse_files(self.participant_listbox,
                                                                  self.display_message,
                                                                  client_socket,
                                                                  name)

        Thread(target=lambda: receive_msg(client_socket,
                                          client_names,
                                          name,
                                          self.display_message,
                                          self.participant_listbox)).start()

        tk.mainloop()

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = ChatUI(root)
#     root.mainloop()
