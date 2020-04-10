from tkinter import *

from Client import *


class Client_app:
    main_window = Tk()
    list_of_users = Listbox(main_window)

    def init_new_conversation_frame(self, name):
        window = Tk()
        window.title("Chat with " + name)
        window.geometry("500x700")
        window.resizable(width=True, height=True)
        window.update()
        frame_1 = Frame(window, width=window.winfo_width() - 20,
                        height=2 * window.winfo_height() / 3 - 20, bg="red")
        frame_1.pack(padx=10, pady=10)
        frame_2 = Frame(window, width=window.winfo_width() - 20, height=window.winfo_height() / 3 - 20,
                        bg="green")
        frame_2.pack(padx=10, pady=10)
        text_box_1 = Text(frame_1, bg="pink")
        text_box_1.pack(padx=10, pady=10)
        text_box_2 = Text(frame_2, bg="grey")
        text_box_2.pack(padx=10, pady=10)
        window.mainloop()

    def make_conversation(self, destination_login):
        #     create window for conversation
        request = "2@" + self.client.login + "@" + self.client.password + "@" + self.client.users_server_ip_address + "@" + str(
            self.client.users_server_port) + "@" + destination_login
        # main_server = Thread(name="Main Server Thread", target=client.send_requests_to_Main_Server, args=(request,))
        # client.list_of_threads.append(main_server)
        # main_server.start()
        destination_login, destination_ip, destination_port, flag = self.client.send_requests_to_Main_Server(request)
        if True:
            self.init_new_conversation_frame(destination_login)
        else:
            print("Returned false")

    def double_click(self, event):
        item = self.list_of_users.get('active')
        conversation = Thread(target=self.make_conversation, args=(str(item),))
        conversation.daemon = True
        conversation.start()

    def __init__(self, client):
        ## fiorst tell the server that I am connected
        request = "1@" + client.login + "@" + client.password + "@" + client.users_server_ip_address + "@" + str(
            client.users_server_port)
        self.client = client
        destination_login, destination_ip, destination_port, flag = self.client.send_requests_to_Main_Server(request)
        if not flag:
            print("NO connection to server estanlished")
        scrollbar = Scrollbar(self.main_window)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.list_of_users.config(yscrollcommand=scrollbar.set)
        self.list_of_users.insert(1, "Ola")
        self.list_of_users.insert(2, "Alina")
        self.list_of_users.insert(3, "Damian")
        self.list_of_users.pack(side=LEFT, fill=BOTH)
        scrollbar.config(command=self.list_of_users.yview())
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

    ############## tworze wątek do obsługi serwera na kliencie #########
    # try:
    # clients_server = Thread(target=client.clients_server_listen_for_other_users, args=())
    # clients_server.start()
    # except:
    #     print("Error when waiting for new connectiom")
    main_application = Client_app(client)
# main_application.main_window.mainloop()
