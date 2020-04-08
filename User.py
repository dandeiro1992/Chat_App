import socket


class User:
    name = ""
    login = ""
    password = ""
    ip_address = ""
    port_for_main_server_connection = 0
    users_server_port = 0
    users_socket_for_server_connection = socket.socket()

    def __init__(self, name=None, login=None, password=None, ip_address=None, port_1=None, port_2=None,
                 users_socket_for_server_connection=None):
        self.name = name
        self.login = login
        self.password = password
        self.users_socket_for_server_connection=users_socket_for_server_connection
        self.ip_address = ip_address
        self.port_for_main_server_connection = port_1
        self.clients_server_port = port_2


    def toString(self):
        return f'name {self.name} ,\n login {self.login}, \npassword {self.password}, \nip address {self.ip_address}, \nport ' \
               f'for main server communication {self.port_for_main_server_connection}, \nuser\'s server\'' \
               f's port {self.users_server_port} '
