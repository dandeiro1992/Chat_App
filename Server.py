from threading import Thread, active_count
from globals import *
import code

class Server:
    list_of_all_users = []
    server_socket = socket.socket()
    Main_Server_ip_address = ""
    Main_Server_port_number = 0
    list_of_threads = []

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.Main_Server_ip_address = MAIN_SERVER_IP
        self.Main_Server_port_number = SERVER_PORT
        self.server_socket.bind((self.Main_Server_ip_address, self.Main_Server_port_number))
        self.server_socket.listen(NUMBER_OF_USERS)

    def talk_with_client(self, client_socket):
        # #### I use the synchronous calls, Client always begins the conversation, because server accomplishes
        # requests and informs ###########
        # while True:  # receiving a request from Client
        frame = receive_frame(client_socket)
        data = prepare_data(frame)
        Main_Server_serve_client(data, client_socket, self.list_of_all_users)

    def start_listening_to_connections(self):
        ################ updating list of connected users every 5 seconds #######
        # checking_connections = Thread(name="checking_connections", target=Main_Server_check_connections,
        #                               args=(self.list_of_all_users, self.list_of_connected_users,))
        ################ updating list of connected users every 5 seconds #######
        ################ Listening for connections #################
        while True:
            client_socket, client_address = self.server_socket.accept()
            ################ Listening for connections #################
            ## When connection is established, server can talk to user with client_socket in separate thread ##
            talking_with_client_thread = Thread(name=str(client_address[0]) + ":" + str(client_address[1]),
                                                target=self.talk_with_client, args=(client_socket,))
            # self.list_of_threads.append(talking_with_client_thread)
            talking_with_client_thread.start()


def show(servers):
    while True:
        print("Working threads:")
        print("liczba aktywnych wątków "+str(active_count()))
        for i in servers.list_of_threads:
            print(i.name + "\n")
        for i in servers.list_of_all_users:
            print(i.toString())
        time.sleep(0.5)

# code.interact(local=locals())

server = Server()
################ checking threads #############
showing_thread = Thread(target=show, args=(server,))
showing_thread.start()
################ checking threads #############
server.start_listening_to_connections()
