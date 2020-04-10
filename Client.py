from threading import Thread
from globals import *


class Client(User):
    list_of_all_users = []
    list_of_threads = []
    clients_server = socket.socket()
    requests_core = ""

    ########### Creating Client - firstly creating server for Client ########
    def __init__(self, login, password, users_server_port):
        clients_server_ip_address = socket.gethostbyname(socket.gethostname())
        try:
            super().__init__(login, password, clients_server_ip_address, users_server_port, False)
            self.clients_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.clients_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.clients_server.bind((self.users_server_ip_address, self.users_server_port))
            self.clients_server.listen(NUMBER_OF_USERS)
            self.requests_core = "@" + self.login + "@" + self.password + "@" + self.users_server_ip_address + "@" + str(
                self.users_server_port) + "@"
        except ConnectionRefusedError:
            print("Client's server not established")

    ###### Connectiong to MAIN SERVER ##################
    def send_requests_to_Main_Server(self, request):
        try:
            connect_to_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connect_to_server_socket.connect((MAIN_SERVER_IP, SERVER_PORT))
            return talk_with_Main_Server(connect_to_server_socket, request)
        except ConnectionRefusedError:
            print("No connection to Main Server established)")


if __name__ == "__main__":
    good_clients_server_flag = False
    ########### Tworzę Clienta - automatycznie tworzy się server klienta ####
    while not good_clients_server_flag:
        try:
            port = input("Wprowadź numer portu na którym będzie słuchał server znajdujący się u klienta i inne dane "
                         "oddzielone @\nlogin@password@number_of_port\n")
            tmp = port.split("@")
            print(tmp)
            client = Client(tmp[0], tmp[1], tmp[2])
            good_clients_server_flag = True
        except OSError:
            print("Wprowadź numer portu ponownie")

    ############## tworze wątek do obsługi serwera na kliencie #########
    try:
        clients_server = Thread(target=client.clients_server_listen_for_other_users, args=())
        clients_server.start()
    except:
        print("Error when waiting for new connectiom")

