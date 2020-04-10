from tkinter import *


class Conversation_frame:


    def __init__(self, name):
        window = Toplevel()
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
        print(frame_1.winfo_width())
        text_box_1 = Text(frame_1, bg="pink")
        text_box_1.pack(padx=10, pady=10)
        text_box_2 = Text(frame_2, bg="grey")
        text_box_2.pack(padx=10, pady=10)
        window.mainloop()


