class User:
    login = ""
    password = "damek"
    users_server_ip_address = ""  # ip address of user's server
    users_server_port = 0
    connected = False

    def __init__(self, login=None, password=None, ip_address=None, port_1=None, connected=False):
        self.login = login
        self.password = password
        self.users_server_ip_address = ip_address
        self.users_server_port = port_1
        self.connected = connected

    def toString(self):
        return f'login {self.login}, \npassword {self.password}, \nip address {self.users_server_ip_address}, ' \
               f'\n, \nuser\'s server\'' \
               f's port {self.users_server_port}, is_connected? {self.connected} '
