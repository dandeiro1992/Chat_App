from threading import Thread
from tkinter import *


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
        self.init_new_conversation_frame(destination_login)

    def double_click(self, event):
        item = self.list_of_users.get('active')
        conversation = Thread(target=self.make_conversation, args=(str(item),))
        conversation.daemon=True
        conversation.start()

    def __init__(self):
        scrollbar = Scrollbar(self.main_window)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.list_of_users.config(yscrollcommand=scrollbar.set)
        self.list_of_users.insert(1, "Ola")
        self.list_of_users.insert(2, "Alina")
        self.list_of_users.insert(3, "Damian")
        self. list_of_users.pack(side=LEFT, fill=BOTH)
        scrollbar.config(command=self.list_of_users.yview())
        self.list_of_users.bind('<Double-1>', self.double_click)
        self.main_window.mainloop()

    def start_conversation(self, event):
        print("Witaj swiecie")


if __name__ == '__main__':
    main_application = Client_app()
# main_application.main_window.mainloop()
