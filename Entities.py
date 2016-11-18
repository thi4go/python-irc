from socket import *

class Client:
    def __init__(self, socket, address):
        self.socket   = socket
        self.address  = address
        self.nickname = address
        self.room     = ''

    def send(msg):
        return self.socket.send(msg)

    # implementacao para poder iterar no select()
    def fileno(self):
        return self.socket.fileno()


class Room:

    def __init__(self, name, admin):
        self.name  = name
        self.admin = admin
