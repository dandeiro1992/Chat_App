import socket
from threading import *
import time


class User:
    name = ""
    login = ""
    password = ""
    ip_address = ""
    port = 0
    user_socket = socket.socket()
    thread = Thread()

    def talk(self, socket):
        print(self.thread.name)
        while True:
            msg = socket.recv(1024)

            print(msg.decode('utf-8'))
            msg = "damian" + str(msg)
            socket.send(bytes(msg, 'utf-8'))
            time.sleep(3)

    def __init__(self, socket, ip_address, port):
        self.user_socket = socket
        self.ip_address = ip_address
        self.port = port
        self.thread = Thread(target=self.talk, args=(self.user_socket,))
        self.thread.name = ip_address + ":" + str(port)
        self.thread.start()

    def toString(self):
        return f'name {self.name}, login {self.login}, password {self.password}, ip address {self.ip_address}, port {self.port}, thread {self.thread.getName()}'
