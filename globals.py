import time
from User import *

MAIN_SERVER_IP = "127.0.0.1"
SERVER_PORT = 1234
NUMBER_OF_USERS = 5
FRAME_SIZE = 5
HEADER_SIZE = 3
SEPARATOR = "@"


def receive_frame(socket):
    print("*****************")
    msg_len = 0
    full_msg = ""
    new_msg = True
    while True:
        msg = socket.recv(FRAME_SIZE)
        msg = msg.decode('utf-8')
        if len(msg) < HEADER_SIZE and new_msg == True:
            break
        print(msg)
        if new_msg:
            print(f"lalalala : {msg[:HEADER_SIZE]}")
            msg_len = int(msg[:HEADER_SIZE])
            print(f"lalalala : {msg_len}")
            new_msg = False
            full_msg += msg[HEADER_SIZE:]
        else:
            full_msg += msg
        print("lenghth of full message" + str(len(full_msg)))
        if len(full_msg) == msg_len:
            return full_msg


def send_frame(socket, msg):
    msg = f'{len(msg):<{HEADER_SIZE}}' + msg
    print("-------------------\n")
    print(msg)
    socket.send(bytes(msg, 'utf-8'))
    return len(msg) + HEADER_SIZE


def prepare_data(frame):
    if frame == None:
        return None
    else:
        data = frame.split(SEPARATOR)
        return data


def find_socket_by_login(source, login):
    for i in source:
        if i.login == login:
            return i.users_socket_for_server_connection


def Main_Server_serve_client(data, client_socket, list_of_all_users, list_of_connected_users):
    print(data)
    if data[0] == "1":  # add or update data in list_of_all users / list_of_connected_users on Main Server
        name = data[1]
        login = data[2]
        password = data[3]
        users_server_port = data[4]
        ######## update ########
        for i in list_of_all_users:
            if i.login == login:
                if i.password == password:
                    i.users_server_port = int(users_server_port)
                    list_of_connected_users.append(i)
                    send_frame(client_socket, "12")  # state "12"  says: "you were in a base, I updated your profile"
                    print("12")
                    # client_socket.close()
                    break
        ####### add user #######
        for i in list_of_all_users:
            if i.users_socket_for_server_connection == client_socket:
                i.name = name
                i.login = login
                i.password = password
                i.users_server_port = int(users_server_port)
                list_of_connected_users.append(i)
                send_frame(client_socket, "13")  # state "13" says: "I added you to the base"
                print("13")
                # client_socket.close()
                break
    if data[0] == "2":  # Client says to server: I want you (Server) to connect me to somebody
        destination_login = data[1]
        my_login = data[2]
        ip_address = data[3]
        port = data[4]  # for example - I want to connect to Ola who has login ola, I send a frame
        # 2@ola@my_login@my_ip_address@my_listening_port
        # then, the Main Server checks if ola is connected and sends her and me info
        if destination_login in [i.login for i in list_of_connected_users]:
            msg = "14@" + my_login + "@" + ip_address + "@" + port  # Please connect to ...., he wants to talk to you
            print(msg)
            send_frame(find_socket_by_login(list_of_connected_users, destination_login), msg)
            send_frame(client_socket, "15")  # sending confirmation of sending request to ola
            print("15")
            counter_of_people_connected = 2
            # client_socket.close()
        else:
            send_frame(client_socket, "16")  # sending that ola is not connected
            print("16")
            # client_socket.close()
            counter_of_people_connected = 1
        ### finally terminate connection and (in comments)delete users from list of connected users ##
        # counter_of_deleted_users = 0
        # for i in list_of_connected_users:
        #     if i.login == my_login or i.login == destination_login:
        #         list_of_connected_users.remove(i)
        #         counter_of_deleted_users += 1
        #         i.users_socket_for_server_connection.close()
        #         if counter_of_deleted_users == counter_of_people_connected:
        #             print("deleted users from list_of_connected users")
        #             break
    if data[0] == "3":  # sending a message to the server that the user is not longer available and should be removed from connected users list
        login = data[0]
        for i in list_of_connected_users:
            if i.login == login:
                list_of_connected_users.remove(i)
                client_socket.close()


def Main_Server_check_connections(list_of_all_users, list_of_connected_users):
    while True:
        msg = "checking"
        for i in list_of_all_users:
            if send_frame(i.users_socket_for_server_connection, msg) > 0:
                list_of_connected_users.append(i)
            else:
                list_of_connected_users.remove(i)
        time.sleep(5)


######### states of Client when it comes to connection with Server #########
## 1 sends data - updating or creating Client user in Server - when done, Main Server knows that Client is connected ###
## 2 - Client sends request for talking with other user ##
## 3 - Client sends this, when leaving app - telling the Main Server, that it is not connected ##
def talk_with_Main_Server(server_socket):
    while True:
        action = input("jaka akcje chcesz wykonać :\n 1 - zalogowac sie do serwera \n 2 - polaczyc sie z innym "
                   "uzytkownikiem \n 3 - poinformowac Main Server o zakonczeniu polaczenia\n")
        if action == 1:
            msg = input("Przedstaw się: \n np. 1@name@login@password@port")
            send_frame(server_socket, msg)
            # server_socket.close()
        elif action == 2:
            msg = input("Chcę się połączyć z  \n np. 2@destination_login@my_login@ip_address@port")
            send_frame(server_socket, msg)
            server_socket.close()
        elif action == 3:
            msg = input("Koncze połaczenie \n 3@login")
            send_frame(server_socket, msg)
            server_socket.close()
        time.wait(20)
