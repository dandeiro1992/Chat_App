This Chat application is written in python and was basically used for:
-learning multithreading
-learning some GUI in tkinter
-solving some programming stuff
-learning json
-learning sockets connected with pickle

Applicaation runs as follows:
The server:
	- listens to new connections, and everytime it gets a new frame, it checks whether the user is in server's base. If not, adds him.
	-gets a frame from connected user, who wants to connect to sb else, and sends him the most recent credentials, so that he could start a p2p connection.
	-shows in it's console the active Threads.

The client:
	-makes communication with server (sending closing frame is not yet done)
	-makes its own server for getting connections from another Chat users.
	-initialises list of "contacts" from json file Users.json
	-has list of incoming messages - that is responsible for holding messages until the appropriate Chat Box is opened.

The client_app.py:
	-initialises the main window with contacts.
	-creates Chat windows when appropriate contact is double-clicked (when another user is not connectes, Chat window will not open)


When initialising Clients in console, separate them with "@" because that is the original separator.

Example is in Pictures/
