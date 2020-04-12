from functools import partial
from tkinter import *

from Client import *


class Client_app:
    main_window = Tk()
    list_of_users = Listbox(main_window)

    def init_new_conversation_frame(self, destination_login, destination_ip, destination_port):
        self.window = Tk()
        self.window.title("Chat with " + destination_login)
        self.window.geometry("700x700")
        self.window.resizable(width=True, height=True)
        self.window.update()
        self.frame_1 = Frame(self.window, width=self.window.winfo_width() - 20,
                             height=2 * self.window.winfo_height() / 3 - 20, bg="red")
        self.frame_1.pack(padx=10, pady=10)
        self.frame_2 = Frame(self.window, width=self.window.winfo_width() - 20,
                             height=self.window.winfo_height() / 3 - 20,
                             bg="green")
        self.frame_2.pack(padx=10, pady=10)
        self.text_box_1 = Text(self.frame_1, bg="pink")
        self.text_box_1.pack(side=LEFT, fill=BOTH, padx=10, pady=10)
        self.text_box_2 = Text(self.frame_2, bg="grey")
        self.text_box_2.pack(side=LEFT, fill=BOTH, padx=10, pady=10)
        self.scrollbar_1 = Scrollbar(self.frame_1, command=self.text_box_1.yview)
        self.scrollbar_1.pack(side=RIGHT, fill=Y)
        self.text_box_1.config(yscrollcommand=self.scrollbar_1.set)

        self.scrollbar_2 = Scrollbar(self.frame_2, command=self.text_box_2.yview)
        self.scrollbar_2.pack(side=RIGHT, fill=Y)
        self.text_box_2.config(yscrollcommand=self.scrollbar_2.set)
        self.button = Button(self.frame_2, text="wyslij wiadomosc",
                             command=partial(self.send_message_to_user,
                                             destination_login, destination_ip, destination_port))
        self.button.pack()
        self.window.mainloop()

    def make_conversation(self, destination_login):
        #     create window for conversation
        request = "2@" + self.client.login + "@" + self.client.password + "@" + self.client.users_server_ip_address + "@" + str(
            self.client.users_server_port) + "@" + destination_login
        # main_server = Thread(name="Main Server Thread", target=client.send_requests_to_Main_Server, args=(request,))
        # client.list_of_threads.append(main_server)
        # main_server.start()
        destination_login, destination_ip, destination_port, flag = self.client.send_requests_to_Main_Server(request)
        if flag:
            print("daestination login" + destination_login)
            self.init_new_conversation_frame(destination_login, destination_ip, destination_port)
        else:
            print("Returned false")

    def send_message_to_user(self,destination_login,destination_ip,destination_port):
        send_frame_to_user(self.client,self.text_box_2.get("1.0", "end-1c"),destination_login,destination_ip,destination_port)
        print(self.text_box_2.get("1.0", "end-1c")+str(destination_port)+destination_ip+destination_login)
        self.text_box_2.delete("1.0", END)
        # send_frame_to_user(self.client, msg, "Ola", "127.0.1.1", 1236)

    def double_click(self, event):
        item = self.list_of_users.get('active')
        print(item + "hejehejejehe")
        conversation = Thread(target=self.make_conversation, args=(str(item),))
        print(item)
        conversation.daemon = True
        conversation.start()

    def __init__(self, client):
        ## fiorst tell the server that I am connected
        request = "1@" + client.login + "@" + client.password + "@" + client.users_server_ip_address + "@" + str(
            client.users_server_port)
        self.client = client
        destination_login, destination_ip, destination_port, flag = self.client.send_requests_to_Main_Server(request)
        if not flag:
            print("NO connection to server established")
        scrollbar = Scrollbar(self.main_window)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.list_of_users.config(yscrollcommand=scrollbar.set)
        for i in range(len(client.list_of_all_users)):
            self.list_of_users.insert(i + 1, client.list_of_all_users[i].login)
            print(client.list_of_all_users[i].login)
        self.list_of_users.pack(side=LEFT, fill=BOTH)
        scrollbar.config(command=self.list_of_users.yview)
        self.list_of_users.bind('<Double-1>', self.double_click)
        self.main_window.mainloop()


if __name__ == '__main__':
    good_clients_server_flag = False
    ########### Tworzę Clienta - automatycznie tworzy się server klienta ####
    while not good_clients_server_flag:
        try:
            port = input("Wprowadź numer portu na którym będzie słuchał server znajdujący się u klienta i inne dane "
                         "oddzielone @\nlogin@password@number_of_port\n")
            tmp = port.split("@")
            print(tmp)
            client = Client(tmp[0], tmp[1], int(tmp[2]))
            good_clients_server_flag = True
        except OSError:
            print("Wprowadź numer portu ponownie")

    ############# tworze wątek do obsługi serwera na kliencie #########
    if good_clients_server_flag:
        try:
            clients_server = Thread(target=client.clients_server_listen_for_other_users, args=())
            clients_server.start()
        except:
            print("Error when waiting for new connection")

    main_application = Client_app(client)
# main_application.main_window.mainloop()
