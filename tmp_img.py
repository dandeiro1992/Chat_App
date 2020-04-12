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
import os
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


import json

json_file = open("Users.json", "r", encoding='utf-8')
txt = json.load(json_file)
json_file.close()
print(txt["Users"])

file_2 = open("Heniek.json", "w", encoding='utf-8')
json.dump(txt, file_2, ensure_ascii=False)
file_2.close()

with open("Damian/Ola.json", "rb+") as file:
    file.seek(-3, os.SEEK_END)
    file.truncate()
    file.write("damian".encode('utf-8'))
