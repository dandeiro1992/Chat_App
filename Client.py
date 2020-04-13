from threading import Thread
from globals import *


class Client(User):
    list_of_all_users = []
    list_of_threads = []
    clients_server = socket.socket()
    requests_core = ""
    message_tmp={}

    ########### Creating Client - firstly creating server for Client ########
    def __init__(self, login, password, users_server_port):
        self.initialise_list_of_all_users()
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

    def clients_server_listen_for_other_users(self):
        ################ Listening for connections #################
        while True:
            user_socket, user_address = self.clients_server.accept()
            user = User(ip_address=user_address[0], port_1=user_address[1])
            self.message_tmp=get_frame_from_user(user_socket, self.list_of_all_users, user, self.login)
        ################ Listening for connections #################

    def initialise_list_of_all_users(self):
        json_file = open("Users.json", "r", encoding='utf-8')
        list_from_json = json.load(json_file)
        json_file.close()
        for i in list_from_json["Users"]:
            user = User(i["login"], i["password"], i["users_server_ip_address"], i["users_server_port"], False)
            self.list_of_all_users.append(user)
