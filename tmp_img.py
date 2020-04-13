# import tkinter as tk
# from threading import Thread
#
# class DisplayWindow(object):
#
#     def __init__(self):
#         self.running = False
#
#     def start(self):
#         self.running = True
#         self.thread = Thread(target = self.run)
#         self.thread.start()
#
#     def callback(self):
#         self.running = False
#         self.root.destroy()
#
#     def run(self):
#         self.root = tk.Tk()
#         self.root.protocol('WM_DELETE_WINDOW', self.callback)
#         self.root.geometry('600x600')
#
#         tk.Label(self.root, text='Hello World').pack()
#
#         self.root.mainloop()
#
# win = DisplayWindow()
# win.start()
# dog=DisplayWindow()
# dog.start()
# import os
import sys

# from tkinter import *
# from tkinter import scrolledtext
# from wikipedia import *
#
#
# def search_wiki():
#     txt = text.get()  # Get what the user eneterd into the box
#     txt = wikipedia.page(txt)  # Search Wikipedia for results
#     txt = txt.summary  # Store the returned information
#     global textw
#     textw = scrolledtext.ScrolledText(main, width=70, height=30)
#     textw.grid(column=1, row=2, sticky=N + S + E + W)
#     textw.config(background="light grey", foreground="black",
#                  font='times 12 bold', wrap='word')
#     textw.insert(END, txt)
#
#
# main = Tk()
# main.title("Search Wikipedia")
# main.geometry('750x750')
# main.configure(background='ivory3')
#
# text = StringVar()
#
# lblSearch = Label(main, text='Search String:').grid(row=0, column=0)
# entSearch = Entry(main, textvariable=text, width=50).grid(row=0,
#                                                           column=1)
#
# btn = Button(main, text='Search', bg='ivory2', width=10,
#              command=search_wiki).grid(row=0, column=10)
#
# main.mainloop()


# import json
#
# json_file = open("Users.json", "r", encoding='utf-8')
# txt = json.load(json_file)
# json_file.close()
# print(txt["Users"])
#
# file_2 = open("Heniek.json", "w", encoding='utf-8')
# json.dump(txt, file_2, ensure_ascii=False)
# file_2.close()
#
# with open("Damian/Ola.json", "rb+") as file:
#     file.seek(-3, os.SEEK_END)
#     file.truncate()
#     file.write("damian".encode('utf-8'))

# FRAME_SIZE = 1024
# HEADER_SIZE = 10
# import pickle
#
#
# def receive_frame(wiadomosc):
#     full_msg = b''
#     new_msg = True
#     while True:
#         msg = wiadomosc
#         if new_msg:
#             msg_len = int(msg[:HEADER_SIZE])
#             new_msg = False
#             full_msg += msg[HEADER_SIZE:]
#         else:
#             full_msg += msg
#         if len(full_msg) == msg_len:
#             d = pickle.loads(full_msg)
#             print(d)
#
#
# def send_frame(msg):
#     msg = pickle.dumps(msg)
#     msg = bytes(f'{len(msg):<{HEADER_SIZE}}', 'utf-8') + msg
#     return msg
#
#
# msg = {"sender":"Damian","receiver":"Ola","port":1234}
# w=send_frame(msg)
# print(w)
# print("*****************")
#
#
# print(receive_frame(w))
from functools import partial

from tkinter import *


def create_first():
    okno = small_window("hej")


def create_second():
    okno = small_window("dupcia")


def show(name, text_box):
    print(name)
    print(text_box.get("1.0", "end-1c"))


class big_window:

    def __init__(self):
        window = Tk()
        window.title = ("big window")
        window.geometry("300x300")
        button_1 = Button(window, text="first", command=create_first)
        button_1.pack()
        button_2 = Button(window, text="second", command=create_second)
        button_2.pack()
        window.mainloop()


class small_window:

    def __init__(self, name):
        window = Tk()
        window.title = ("small window")
        window.geometry("200x200")
        self.text_box = Text(window, bg="grey")
        self.text_box.pack()
        button_1 = Button(window, text="first", command=partial(show,name, self.text_box))
        button_1.pack()
        window.mainloop()


if __name__ == '__main__':
    big = big_window()
