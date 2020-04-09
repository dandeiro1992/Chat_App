from User import User


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
            msg_to_source = "15@" + destination_login + "@" + ip_address + "@" + str(
                port)  # M_S found the ip address and port and sends it back to user
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
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.connect((ip_address, port))
    send_frame(socket, msg)
    socket.close()
