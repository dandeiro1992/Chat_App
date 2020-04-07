from User import *
from globals import *
import os

class Client:
    #list_of_sockets = []
    list_of_connected_users = []
    receiving_socket = socket.socket()
    list_of_communication_sockets = []
    connect_to_server_socket = socket.socket()
    list_of_threads = []
    clients_server_port_number = 0
    clients_server = socket.socket()
    ip_address = ""

    ########### Creating Client - firstly creating server for Client ########
    def __init__(self, number_of_port):
        try:
            self.clients_server_port_number = number_of_port
            self.ip_address = socket.gethostname()
            self.clients_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.clients_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.clients_server.bind((self.ip_address, self.clients_server_port_number))
            self.clients_server.listen(NUMBER_OF_USERS)
        except ConnectionRefusedError:
            print("Client's server not established")

    def clients_server_listen_for_other_users(self):
        ################ Listening for connections #################
        while True:
            user_socket, user_address = self.clients_server.accept()
            user = User(user_socket, user_address[0], user_address[1])
            self.list_of_connected_users.append(user)
            #self.list_of_sockets.append(user_socket)
        ################ Listening for connections #################

    ###### Connectiong to MAIN SERVER ##################
    def connect_to_server(self):
        try:
            self.connect_to_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connect_to_server_socket.connect((MAIN_SERVER_IP, SERVER_PORT))
            self.talk_with_server()
        except ConnectionRefusedError:
            print("No connection to Main Server established)")

    def talk_with_server(self):
        i = 1
        while True:
            msg = str(i)
            self.connect_to_server_socket.send(bytes(msg, 'utf-8'))
            time.sleep(3)
            msg = self.connect_to_server_socket.recvfrom(1024)[0]
            print(msg.decode('utf-8'))
            i = i + 1


if __name__ == "__main__":
    good_clients_server_flag=False
    ########### Tworzę Clienta - automatycznie tworzy się server klienta ####
    while not good_clients_server_flag:
        try:
            port = input("Wprowadź numer portu na którym będzie słuchał server znajdujący się u klienta")
            client = Client(int(port))
            good_clients_server_flag=True
        except OSError:
            print("Wprowadź numer portu ponownie")
    ############## tworzę wątek do rozmowy z serwerem głównym ##########
    try:
        main_server = Thread(target=client.connect_to_server, args=())
        client.list_of_threads.append(main_server)
        main_server.start()
    except ConnectionRefusedError:
        print("Error creating thread talking to the main server")
    ############## tworze wątek do obsługi serwera na kliencie #########
    try:
        clients_server=Thread(target=client.clients_server_listen_for_other_users, args=())
        clients_server.start()
    except:
        print("Error when waiting for new connections")
