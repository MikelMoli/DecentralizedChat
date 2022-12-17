import settings
import requests
from kivy.app import App
from kivy.lang import builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol


class LoginLayout(Screen):
    pass

class ChatLayout(Screen):

    name = ObjectProperty(None)
    pizza = ObjectProperty(None)
    text_input = ObjectProperty(None)
    chat_label = ObjectProperty(None)
    chat_scroll = ObjectProperty(None)
    first_message = True

    def send_message(self):
        self.username = self.ids.username.text
        user_text = self.ids.text_input.text
        if user_text.strip() != '':
            # self.chat_history.text += f"\n{self.chat_username}: {user_text}"
            if self.first_message:
                message_text = f'[color=02a200][b][{self.username}][/b][/color] {user_text}'
                self.first_message = False
                # COLOR PARA LOS RECIVIDOS: c00000
            else:
                message_text = f'[color=c00000][b][{self.username}][/b][/color] {user_text}'
            self.ids.chat_label.text += f"\n{message_text}"
            # chat_label = Label(text=message_text)
            # self.ids.chat_scroll.add_widget(chat_label)
            self.ids.text_input.text = ''

class ChatApp(App, DatagramProtocol):

    def __init__(self, host, port):
        # super().__init__(**kwargs)
        super().__init__()
        self.host = host
        self.port = port
        self.address = host, port
        self.username = None
        self.address_list = []
        self.request_ips()
        self.id = host, port
        # self.address = None
        self.server = settings.CONNECTION['HOST']

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

    def prueba(self, message):
        # Comprobar los exitbye, clearmsg y esas mierdas
        chat_message = f"[color=02a200][b][{self.username}][/b][/color] {message}"
        channel_message = f"[color=c00000][b][{self.username}][/b][/color] {message}"
        channel_message = channel_message.encode('utf-8')
        self.chat_label.text += f"\n{chat_message}"

        for address in self.address_list:
            print(f'Sending message to: {address}')
            self.transport.write(channel_message, address)

    def datagramReceived(self, datagram: bytes, addr):
        # Aquí tengo que cambiarlo por el label. Importante el tema del color!
        datagram = datagram.decode("utf-8")
        print(addr)
        if addr not in self.address_list:
            self.address_list.append(addr)
            print(f"New address added: {addr}")
        self.chat_label.text += f"\n{datagram}"
        print("\n" + datagram)

    def build(self):
        # Esto creo que sería como el run que yo hice
        self.request_ips()
        sm = ScreenManager()
        sm.add_widget(LoginLayout(name='LoginLayout'))
        sm.add_widget(ChatLayout(name='ChatLayout'))
        self.chat_label = sm.get_screen('ChatLayout').ids.chat_label
        return sm

if __name__ == '__main__':
    port = 9998
    host = '127.0.0.1'
    ChatApp(host, port).run()
