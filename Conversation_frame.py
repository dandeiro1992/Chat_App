from functools import partial
from tkinter import *


class Conversation_frame:

    def __init__(self, name):
        window = Tk()
        window.title("Chat with " + name)
        window.geometry("700x700")
        window.resizable(width=True, height=True)
        window.update()
        frame_1 = Frame(window, width=window.winfo_width() - 20,
                        height=2 * window.winfo_height() / 3 - 20, bg="red")
        frame_1.pack(padx=10, pady=10)
        frame_2 = Frame(window, width=window.winfo_width() - 20, height=window.winfo_height() / 3 - 20,
                        bg="green")
        frame_2.pack(padx=10, pady=10)
        text_box_1 = Text(frame_1, bg="pink")
        text_box_1.pack(side=LEFT, fill=BOTH, padx=10, pady=10)
        text_box_2 = Text(frame_2, bg="grey")
        text_box_2.pack(side=LEFT, fill=BOTH, padx=10, pady=10)
        scrollbar_1 = Scrollbar(frame_1, command=text_box_1.yview)
        scrollbar_1.pack(side=RIGHT, fill=Y)
        text_box_1.config(yscrollcommand=scrollbar_1.set)

        scrollbar_2 = Scrollbar(frame_2, command=text_box_2.yview)
        scrollbar_2.pack(side=RIGHT, fill=Y)
        text_box_2.config(yscrollcommand=scrollbar_2.set)
        button = Button(frame_2, text="wyslij wiadomosc",
                        command=partial(print,partial(text_box_2.get,("1.0",END))))
        button.pack()
        window.mainloop()

    def send_message_to_user(self, text):
        print("klik")
        print(text)


if __name__ == "__main__":
    frame = Conversation_frame("Damian")


# from functools import partial
# from tkinter import *
#
#
# class Conversation_frame:
#
#     def __init__(self, name):
#         self.window = Tk()
#         self.window.title("Chat with " + name)
#         self.window.geometry("700x700")
#         self.window.resizable(width=True, height=True)
#         self.window.update()
#         self.frame_1 = Frame(self.window, width=self.window.winfo_width() - 20,
#                         height=2 * self.window.winfo_height() / 3 - 20, bg="red")
#         self.frame_1.pack(padx=10, pady=10)
#         self.frame_2 = Frame(self.window, width=self.window.winfo_width() - 20, height=self.window.winfo_height() / 3 - 20,
#                         bg="green")
#         self.frame_2.pack(padx=10, pady=10)
#         self.text_box_1 = Text(self.frame_1, bg="pink")
#         self.text_box_1.pack(side=LEFT, fill=BOTH, padx=10, pady=10)
#         self.text_box_2 = Text(self.frame_2, bg="grey")
#         self.text_box_2.pack(side=LEFT, fill=BOTH, padx=10, pady=10)
#         self.scrollbar_1 = Scrollbar(self.frame_1, command=self.text_box_1.yview)
#         self.scrollbar_1.pack(side=RIGHT, fill=Y)
#         self.text_box_1.config(yscrollcommand=self.scrollbar_1.set)
#
#         self.scrollbar_2 = Scrollbar(self.frame_2, command=self.text_box_2.yview)
#         self.scrollbar_2.pack(side=RIGHT, fill=Y)
#         self.text_box_2.config(yscrollcommand=self.scrollbar_2.set)
#         self.button = Button(self.frame_2, text="wyslij wiadomosc",
#                         command=self.send_message_to_user)# "text_box_2.get(, END)))"))
#         self.button.pack()
#         self.window.mainloop()
#
#     def send_message_to_user(self):
#         print("klik")
#         print(self.text_box_2.get("1.0",END))
#         self.text_box_2.delete("1.0",END)
#
#
# if __name__ == "__main__":
#     frame = Conversation_frame("Damian")
