import time
from User import *
import socket
import json
import pickle

MAIN_SERVER_IP = "127.0.0.1"
SERVER_PORT = 1234
NUMBER_OF_USERS = 5
FRAME_SIZE = 5
HEADER_SIZE = 3
SEPARATOR = "@"


def receive_frame(socket):
    full_msg = b''
    new_msg = True
    while True:
        msg = socket.recv(FRAME_SIZE)
        # if len(msg) < HEADER_SIZE and new_msg == True:
        #     break
        if new_msg:
            msg_len = int(msg[:HEADER_SIZE])
            new_msg = False
            full_msg += msg[HEADER_SIZE:]
        else:
            full_msg += msg
        if len(full_msg) == msg_len:
            d = pickle.loads(full_msg)
            return d


def send_frame(socket, msg):
    msg = pickle.dumps(msg)
    msg = bytes(f'{len(msg):<{HEADER_SIZE}}', 'utf-8') + msg
    socket.send(msg)
    return len(msg)


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
                        Main_Server_connect_to_Client_and_send_msg(client_socket,
                                                                   msg_to_source)
                    else:
                        pass  # here will be password verification frame sent
        else:  # what should be done if no such login is found?
            ### adding new user ###
            user = User(login, password, users_server_ip_address, users_server_port, True)
            # and this user should be appended to all users list
            list_of_all_users.append(user)
            msg_to_source = "13"  # it says that MS added user
            Main_Server_connect_to_Client_and_send_msg(client_socket, msg_to_source)
    elif state == '2':  # I want to connect to some destination login, and need its data
        destination_login = data[5]
        ip_address, port = search_for_user_data(destination_login, list_of_all_users)
        print("******************")
        print(ip_address)
        print(str(port))
        if len(ip_address) < 5:
            msg_to_source = "16"  # sending to user that the destination is not connected
            Main_Server_connect_to_Client_and_send_msg(client_socket, msg_to_source)
        else:
            msg_to_source = "15@" + destination_login + "@" + ip_address + "@" + str(port)  # M_S found the ip
            # address and port and sends it back to user
            Main_Server_connect_to_Client_and_send_msg(client_socket, msg_to_source)
    elif state == '3':  # sending a message that user becomes disdandeiro@damian@1235connected
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


def Main_Server_connect_to_Client_and_send_msg(sockets, msg):
    send_frame(sockets, msg)
    sockets.close()


def client_connect_to_and_send_msg(ip_address, port, msg):
    sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockets.connect((ip_address, int(port)))
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
    destination_login = ""
    destination_ip = ""
    destination_port = 0
    data = prepare_data(request)
    status = data[0]
    ## every time client has to push the request to the server
    send_frame(server_socket, request)
    ##but accordingly to the request status, handling server responses differs
    if status == '1':
        msg = receive_frame(server_socket)
        if msg not in ['12', '13']:
            server_socket.close()
            return destination_login, destination_ip, destination_port, False
        else:
            return destination_login, destination_ip, destination_port, True
    elif status == '2':
        msg = receive_frame(server_socket)
        if msg == '16':
            server_socket.close()
            return destination_login, destination_ip, destination_port, False
        else:
            response_data = prepare_data(msg)
            if response_data[0] == '15':
                destination_login = response_data[1]
                destination_ip = response_data[2]
                destination_port = response_data[3]
                server_socket.close()
                return destination_login, destination_ip, destination_port, True
            else:
                server_socket.close()
                return destination_login, destination_ip, destination_port, True


def get_frame_from_user(socket, list_of_all_users, user, login):
    msg = receive_frame(socket)#json.loads(receive_frame(socket))
    file = open(login + "/" + msg["sender_login"] + ".json", "r", encoding='utf-8')
    temp = json.load(file)
    file.close()
    temp["Messages"].append(msg)
    file = open(login + "/" + msg["sender_login"] + ".json", "w", encoding='utf-8')
    json.dump(temp, file, ensure_ascii=False)
    file.close()
    socket.close()
    user.login = msg["sender_login"]
    user.users_server_ip_address = msg["sender_ip"]
    user.users_server_port = msg["sender_port"]
    if user.login in [i.login for i in list_of_all_users]:
        for i in list_of_all_users:
            if i.login == user.login:
                i.users_server_ip_address = user.users_server_ip_address
                i.users_server_port = user.users_server_port
                i.connected = True
    else:
        list_of_all_users.append(user)
    print("Otrzymałem: "+str(msg))
    return msg


def send_frame_to_user(client, msg, login, ip_address, port):
    sender_login = client.login
    sender_ip = client.users_server_ip_address
    sender_port = client.users_server_port
    receiver_login = login
    receiver_ip = ip_address
    receiver_port = port
    added = "false"
    json_frame = "{" + f'"sender_login" : "{sender_login}","sender_ip" : "{sender_ip}","sender_port" : {str(sender_port)},"receiver_login" : "{receiver_login}","receiver_ip" : "{receiver_ip}","receiver_port" : {receiver_port},"added" : {added},"msg" : "' + msg + '"}'
    print("json_frame=" + json_frame)
    print(client.login + "/" + login + ".json")
    file = open(client.login + "/" + login + ".json", "r", encoding='utf-8')
    temp = json.load(file)
    file.close()
    json_frame_object = json.loads(json_frame, encoding='utf-8')
    client_connect_to_and_send_msg(ip_address, port, json_frame_object)
    temp["Messages"].append(json_frame_object)
    file = open(client.login + "/" + login + ".json", "w", encoding='utf-8')
    json.dump(temp, file, ensure_ascii=False)
    file.close()
    return json_frame_object
