import tkinter as tk
from threading import Thread

class DisplayWindow(object):

    def __init__(self):
        self.running = False

    def start(self):
        self.running = True
        self.thread = Thread(target = self.run)
        self.thread.start()

    def callback(self):
        self.running = False
        self.root.destroy()

    def run(self):
        self.root = tk.Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.callback)
        self.root.geometry('600x600')

        tk.Label(self.root, text='Hello World').pack()

        self.root.mainloop()

win = DisplayWindow()
win.start()
dog=DisplayWindow()
dog.start()