from User import *
from globals import *
import time


class Server:
    list_of_connected_users = []
    #list_of_threads = []
    #list_of_sockets = []
    server_socket = socket.socket()
    ip_address = ""
    port_number = 0

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ip_address = MAIN_SERVER_IP
        self.port_number = SERVER_PORT
        self.server_socket.bind((self.ip_address, self.port_number))
        self.server_socket.listen(NUMBER_OF_USERS)

    def start_listening_to_connections(self):
        ################ Listening for connections #################
        while True:
            client_socket, client_address = self.server_socket.accept()
            user = User(client_socket, client_address[0], client_address[1])
            self.list_of_connected_users.append(user)
            #self.list_of_sockets.append(client_socket)
        ################ Listening for connections #################


def show(servers):
    while True:
        array_of_names=[]
        for i in servers.list_of_connected_users:
            if i.name != "":
                array_of_names.append(i.name)
        for i in servers.list_of_connected_users:
            if i.adresat in array_of_names:
                i.user_socket.send(bytes("Connect to "+i.adresat,'utf-8'))
        print("Working threads:")

        for i in servers.list_of_connected_users:
            print(i.toString())
        time.sleep(5)


server = Server()

################ checking threads #############
showing_thread = Thread(target=show, args=(server,))
showing_thread.start()
################ checking threads #############

server.start_listening_to_connections()