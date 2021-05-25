# ChatRoom

This application extends a chatting project by adding additional features.
The user can select an individual to chat privately with, rather than chatting
with all users. The user can also select to send a txt file to an individual or the
whole group.

The application is run with Python through the Command Terminal. There are no special
arguments required.

Server:

To start the server, direct your command prompt to the location of file "ChatServer.py"
Type 'python ChatServer.py' in command prompt and hit enter. The server should connect and display
"Chat session suiccessfully connected on: "

Client:
To start the client, direct your command prompt to the location of file "ChatHandling.py"
Enter 'python ChatHandling.py' in command prompt and hit enter. The client program will
ask for your name to login. A UI will be displayed that welcomes you to the chat with your
name on display. Type your first message and hit send to start talking to others!

In order to login, you must input your name on the terminal. The client will send
your name to the server and connect you to the chat.

Once other users send messages in the chatroom, their names will start to be logged
on the client. After this point, the user can send private messages to other users.

The bottom left field allows for the selection of receiving individuals. As new connections
are made, the application adds new users to be selected. The user can select 'everyone'
or select a single user.

The file selection button will open file explorer. This application allows the transfer of
.txt files. Once sent, the other clients will have a file explorer window pop up on their
side asking for a location and name of the file. The file will then be written to that location
and saved name.


ToDo:

Increase file transfer size using multiple packets sent through the sockets. 

Have more fluid design of listing current users.

Track when users have left the chat and update list. 

Possible: Addition to create private chat rooms when sending messages to individuals. 

If server disconnects, sends message to all clients and no longer accepts messages. 

Error detections!!!

Add database to store user conversations.
