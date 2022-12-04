from tkinter import *

import threading

import time

class App(threading.Thread):
    # TODO: Create send method and received method for the chat. This will be called from the client
    BG_GRAY = "#ABB2B9"
    BG_COLOR = "#17202A"
    TEXT_COLOR = "#EAECEE"

    FONT = "Helvetica 14"
    FONT_BOLD = "Helvetica 13 bold"


    def __init__(self):
        self.user_created = False
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def send_message(self):
        msg = self.e.get()
        if self.user_created is False and msg:
            print('Entra')
            self.user_created = True
            self.username = self.e.get()
            self.message.set('')
            self.txt.insert(END, f"Welcome {self.username}! \n"
                                  "If you want to exit and delete your node enter exitbye. \n"
                                  "If you want to clear the screen enter clearmsg.\n")
        elif msg == 'exitbye':
            self.root.destroy()

        elif msg == 'clearmsg':
            self.txt.delete(1.0, END)
            self.message.set('')

        else:
            send = f"[{self.username}] "  + self.e.get()
            self.txt.insert(END, "\n" + send)
            self.message.set('')


    def welcome_process(self):
        self.txt.insert(END, "Welcome to the decentralized chat!\n"
                             "Please, enter your nickname and press Enter.\n\n")

    def press_enter(self, e):
        self.send_message()

    def run(self):
        self.root = Tk()
        self.root.title("P2P Chat")
        # Creating text frame
        
        lable1 = Label(self.root, bg=self.BG_COLOR, fg=self.TEXT_COLOR, text="Welcome", font=self.FONT_BOLD, pady=10, width=20, height=1).grid(row=0)
        
        self.txt = Text(self.root, bg=self.BG_COLOR, fg=self.TEXT_COLOR, font=self.FONT, width=60)
        self.txt.grid(row=1, column=0, columnspan=2)
        
        scrollbar = Scrollbar(self.txt)
        scrollbar.place(relheight=1, relx=0.974)
        
        self.message = StringVar()
        self.e = Entry(self.root, textvariable=self.message, bg="#2C3E50", fg=self.TEXT_COLOR, font=self.FONT, width=55)
        self.e.grid(row=2, column=0)
        
        send = Button(self.root, text="Send", font=self.FONT_BOLD, bg=self.BG_GRAY, command=self.send_message).grid(row=2, column=1)
        self.root.bind('<Return>', self.press_enter)

        self.welcome_process()
        self.root.mainloop()



if __name__ == '__main__':
    gui = App() 
