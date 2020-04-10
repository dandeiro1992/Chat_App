import time
from User import *
import socket

MAIN_SERVER_IP = "127.0.0.1"
SERVER_PORT = 1234
NUMBER_OF_USERS = 5
FRAME_SIZE = 5
HEADER_SIZE = 3
SEPARATOR = "@"


def receive_frame(socket):
    msg_len = 0
    full_msg = ""
    new_msg = True
    while True:
        msg = socket.recv(FRAME_SIZE)
        msg = msg.decode('utf-8')
        if len(msg) < HEADER_SIZE and new_msg == True:
            break
        if new_msg:
            msg_len = int(msg[:HEADER_SIZE])
            new_msg = False
            full_msg += msg[HEADER_SIZE:]
        else:
            full_msg += msg
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


# def Main_Server_serve_client_tmp(data, client_socket, list_of_all_users, list_of_connected_users):
#     print(data)
#     if data[0] == "1":  # add or update data in list_of_all users / list_of_connected_users on Main Server
#         name = data[1]
#         login = data[2]
#         password = data[3]
#         users_server_port = data[4]
#         ######## update ########
#         for i in list_of_all_users:
#             if i.login == login:
#                 if i.password == password:
#                     i.users_server_port = int(users_server_port)
#                     list_of_connected_users.append(i)
#                     send_frame(client_socket, "12")  # state "12"  says: "you were in a base, I updated your profile"
#                     print("12")
#                     # client_socket.close()
#                     break
#         ####### add user #######
#         for i in list_of_all_users:
#             if i.users_socket_for_server_connection == client_socket:
#                 i.name = name
#                 i.login = login
#                 i.password = password
#                 i.users_server_port = int(users_server_port)
#                 list_of_connected_users.append(i)
#                 send_frame(client_socket, "13")  # state "13" says: "I added you to the base"
#                 print("13")
#                 # client_socket.close()
#                 break
#     if data[0] == "2":  # Client says to server: I want you (Server) to connect me to somebody
#         destination_login = data[1]
#         my_login = data[2]
#         ip_address = data[3]
#         port = data[4]  # for example - I want to connect to Ola who has login ola, I send a frame
#         # 2@ola@my_login@my_ip_address@my_listening_port
#         # then, the Main Server checks if ola is connected and sends her and me info
#         if destination_login in [i.login for i in list_of_connected_users]:
#             msg = "14@" + my_login + "@" + ip_address + "@" + port  # Please connect to ...., he wants to talk to you
#             print(msg)
#             send_frame(find_socket_by_login(list_of_connected_users, destination_login), msg)
#             send_frame(client_socket, "15")  # sending confirmation of sending request to ola
#             print("15")
#             counter_of_people_connected = 2
#             # client_socket.close()
#         else:
#             send_frame(client_socket, "16")  # sending that ola is not connected
#             print("16")
#             # client_socket.close()
#             counter_of_people_connected = 1
#         ### finally terminate connection and (in comments)delete users from list of connected users ##
#         # counter_of_deleted_users = 0
#         # for i in list_of_connected_users:
#         #     if i.login == my_login or i.login == destination_login:
#         #         list_of_connected_users.remove(i)
#         #         counter_of_deleted_users += 1
#         #         i.users_socket_for_server_connection.close()
#         #         if counter_of_deleted_users == counter_of_people_connected:
#         #             print("deleted users from list_of_connected users")
#         #             break
#     if data[0] == "3":  # sending a message to the server that the user is not longer available and should be removed from connected users list
#         login = data[0]
#         for i in list_of_connected_users:
#             if i.login == login:
#                 list_of_connected_users.remove(i)
#                 client_socket.close()

def Main_Server_serve_client(data, client_socket, list_of_all_users):
    state = data[0]
    login = data[1]
    password = data[2]
    users_server_ip_address = data[3]
    users_server_port = data[4]
    if state == '1':
        ###### adding a user who claims that is connected or updating ######
        ### firstly updating ####
        if login in [i.login for i in list_of_all_users]:
            for j in list_of_all_users:
                if login == j.login:
                    if password == j.password:
                        j.users_server_ip_address = users_server_ip_address
                        j.users_server_port = users_server_port
                        j.connected = True
                        msg_to_source = "12"  # it says that server updated data
                        Main_Server_connect_to_Client_and_send_msg(users_server_ip_address, users_server_port,
                                                                   msg_to_source)
                    else:
                        pass  # here will be password verification frame sent
        else:  # what should be done if no such login is found?
            ### adding new user ###
            user = User(login, password, users_server_ip_address, users_server_port, True)
            # and this user should be appended to all users list
            list_of_all_users.append(user)
            msg_to_source = "13"  # it says that MS added user
            Main_Server_connect_to_Client_and_send_msg(users_server_ip_address, users_server_port, msg_to_source)
    elif state == '2':  # I want to connect to some destination login, and need its data
        destination_login = data[5]
        ip_address, port = search_for_user_data(destination_login, list_of_all_users)
        if ip_address == "":
            msg_to_source = "16"  # sending to user that the destination is not connected
            Main_Server_connect_to_Client_and_send_msg(users_server_ip_address, users_server_port, msg_to_source)
        else:
            msg_to_source = "15@" + destination_login + "@" + ip_address + "@" + str(port)  # M_S found the ip
            # address and port and sends it back to user
            Main_Server_connect_to_Client_and_send_msg(users_server_ip_address, users_server_port, msg_to_source)
    elif state == '3':  # sending a message that user becomes disconnected
        if login in [i.login for i in list_of_all_users]:
            for j in list_of_all_users:
                if login == j.login:
                    j.connected = False
    client_socket.close()


def search_for_user_data(login, list_of_all_users):
    if login in [i.login for i in list_of_all_users]:
        for i in list_of_all_users:
            if i.login == login:
                return i.users_server_ip_address, i.users_server_port
    else:
        return "", 0


def Main_Server_connect_to_Client_and_send_msg(ip_address, port, msg):
    sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockets.connect((ip_address, port))
    send_frame(sockets, msg)
    sockets.close()


def client_connect_to_Main_Server_and_send_msg(ip_address, port, msg):
    sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockets.connect((ip_address, port))
    send_frame(sockets, msg)
    sockets.close()


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
def talk_with_Main_Server(server_socket, request):
    data = prepare_data(request)
    status = data[0]
    ## every time client has to push the request to the server
    send_frame(server_socket, request)
    ##but accordingly to the request status, handling server responses differs
    if status == '1':
        msg = receive_frame(server_socket)
        if msg not in ['12', '13']:
            server_socket.close(0)
            raise Exception
    elif status == '2':
        msg = receive_frame(server_socket)
        if msg == '16':
            print("destination login is not connected")
            server_socket.close()
        else:
            msg = receive_frame(server_socket)
            response_data = prepare_data(msg)
            if response_data[0] == '15':
                destination_login = data[1]
                destination_ip = data[2]
                destination_port = data[3]
                server_socket.close(0)
                return destination_login, destination_ip, destination_port
            else:
                server_socket.close(0)
                raise Exception
