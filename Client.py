from threading import Thread
from User import *
from globals import *


class Client:
    name = ""
    login = ""
    password = ""
    list_of_connected_users = []
    list_of_threads = []
    connect_to_server_socket = socket.socket()
    clients_server_port_number = 0  # port on which client is listening on
    clients_server = socket.socket()
    ip_address = ""
    list_of_wanted_connections = []

    ########### Creating Client - firstly creating server for Client ########
    def __init__(self, name, login, password, number_of_port):
        try:
            self.name = name
            self.login = login
            self.password = password
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
        ################ Listening for connections #################

    ###### Connectiong to MAIN SERVER ##################
    def connect_to_Main_Server(self, action):
        try:
            self.connect_to_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connect_to_server_socket.connect((MAIN_SERVER_IP, SERVER_PORT))
            talk_with_Main_Server(action, self.connect_to_server_socket)
        except ConnectionRefusedError:
            print("No connection to Main Server established)")


if __name__ == "__main__":
    good_clients_server_flag = False
    ########### Tworzę Clienta - automatycznie tworzy się server klienta ####
    while not good_clients_server_flag:
        try:
            port = input("Wprowadź numer portu na którym będzie słuchał server znajdujący się u klienta i inne dane "
                         "oddzielone @\nname@login@password@number_of_port\n")
            tmp = port.split("@")
            print(tmp)
            client = Client(tmp[0], tmp[1], tmp[2], int(tmp[3]))
            good_clients_server_flag = True
        except OSError:
            print("Wprowadź numer portu ponownie")

    ############## tworze wątek do obsługi serwera na kliencie #########
    try:
        clients_server = Thread(target=client.clients_server_listen_for_other_users, args=())
        clients_server.start()
    except:
        print("Error when waiting for new connections")

    ############## tworzę wątek do rozmowy z serwerem głównym ##########
    while True:
        action = input("jaka akcje chcesz wykonać :\n 1 - zalogowac sie do serwera \n 2 - polaczyc sie z innym "
                       "uzytkownikiem \n 3 - poinformowac Main Server o zakonczeniu polaczenia\n")
        try:
            main_server = Thread(name="My Server Thread", target=client.connect_to_Main_Server, args=(int(action),))
            client.list_of_threads.append(main_server)
            main_server.start()
        except ConnectionRefusedError:
            print("Error creating thread talking to the main server")
