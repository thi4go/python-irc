from socket import *

class Client:
    def __init__(self, socket, address):
        self.socket  = socket
        self.address = address
        self.nickname    = address

    def setName(string):
        self.name = string

    def getName():
        return self.name

    def getSocket():
        return self.socket

    def getAddress():
        return self.address

    def send(msg):
        return self.socket.send(msg)

    # implementacao para poder iterar no select()
    def fileno(self):
        return self.socket.fileno()
