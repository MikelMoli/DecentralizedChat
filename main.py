import settings
import requests
from tkinter import *
from random import randint
from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol 

from uuid import uuid4
import threading

import time

class ChatApp(threading.Thread, DatagramProtocol):

    def __init__(self, host, port):
        self.user_created = False
        if host == "localhost":
            host = "127.0.0.1"

        self.host = host
        self.port = port
        print('NEW ADDRESS: ', host, port)
        self.address = host, port
        self.username = None
        self.address_list = []
        self.request_ips()
        self.id = host, port
        # self.address = None
        self.server = settings.CONNECTION['HOST']
        self.user = uuid4() # Sets a random id the client

        threading.Thread.__init__(self)
        self.start()

    def request_ips(self):
        server_address = f"{settings.CONNECTION['HOST']}/?p={self.port}"
        response = requests.get(server_address)
        if response.status_code == 200:
            for row in response.text.split("\n"):
                address = row.split(',')[0][2:-1]
                port = int(row.split(', ')[1][0:-1])
                full_address = address, port 
                if full_address not in self.address_list and full_address != self.address:
                    self.address_list.append(full_address)
            for add in self.address_list:
                print(add)

    # def startProtocol(self):
    #     self.transport.write("ready".encode("utf-8"), self.server)

    # datagram is the data we receive and address is the address that sends the data
    def datagramReceived(self, datagram: bytes, addr):
        datagram = datagram.decode("utf-8")
        print(addr)
        if addr not in self.address_list:
            self.address_list.append(addr)
            print(f"New address added: {addr}")
            self.txt.insert(END, "\n" + datagram)

        else:
            self.txt.insert(END, "\n" + datagram)


    def send_message(self, message):
        if self.username is not None:
            message = f'{message}'.encode('utf-8')
        else:
            message = f'{message}'.encode('utf-8')
        for address in self.address_list:
            print(f'Sending message to: {address}')
            self.transport.write(message, address)
                
    def callback(self):
        self.root.quit()

    def send_message_interface(self):
        msg = self.e.get()
        if self.user_created is False and msg:
            self.user_created = True
            self.username = self.e.get()
            self.message.set('')
            self.txt.insert(END, f"Welcome {self.username}! \n"
                                  "If you want to exit and delete your node enter exitbye. \n"
                                  "If you want to clear the screen enter clearmsg.\n")
        elif msg == 'exitbye':
            self.root.destroy()
            reactor.stop()

        elif msg == 'clearmsg':
            self.txt.delete(1.0, END)
            self.message.set('')

        else:
            send = f"[{self.username}] "  + self.e.get()
            self.txt.insert(END, "\n" + send)
            self.send_message(message=send)
            self.message.set('')
    


    def welcome_process(self):
        self.txt.insert(END, "Welcome to the decentralized chat!\n"
                             "Please, enter your nickname and press Enter.\n\n")

    def press_enter(self, e):
        self.send_message_interface()

    def run(self):
        self.root = Tk()
        self.root.title("P2P Chat")
        # Creating text frame
        
        lable1 = Label(self.root, bg=settings.BG_COLOR, fg=settings.TEXT_COLOR, text="Welcome", font=settings.FONT_BOLD, pady=10, width=20, height=1).grid(row=0)
        
        self.txt = Text(self.root, bg=settings.BG_COLOR, fg=settings.TEXT_COLOR, font=settings.FONT, width=60)
        self.txt.grid(row=1, column=0, columnspan=2)
        
        scrollbar = Scrollbar(self.txt)
        scrollbar.place(relheight=1, relx=0.974)
        
        self.message = StringVar()
        self.e = Entry(self.root, textvariable=self.message, bg="#2C3E50", fg=settings.TEXT_COLOR, font=settings.FONT, width=55)
        self.e.grid(row=2, column=0)
        
        send = Button(self.root, text="Send", font=settings.FONT_BOLD, bg=settings.BG_GRAY, command=self.send_message_interface).grid(row=2, column=1)
        self.root.bind('<Return>', self.press_enter)

        self.welcome_process()
        
        self.root.mainloop()



if __name__ == '__main__':
    port = randint(1000, 5000)
    port = 9998
    host = '127.0.0.1'
    reactor.listenUDP(port, ChatApp(host, port))
    reactor.run()
