import socket
import asyncore
import collections

class Client(asyncore.dispatcher):

    def __init__(self, host_address, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Connecting to host at %s', host_address
        self.connect( (host_address, port))
        self.outbox = collections.deque()

    def say(self, message):
        self.outbox.append(message)
        print 'Enqueued message: %s', message

    def handle_write(self):
        if not self.outbox:
            return
        message = self.outbox.popleft()
        if len(message) > 1024:
            raise ValueError('Message too long')
        self.send(message)

    def handle_read(self):
        message = self.recv(1024)
        print 'Received message: %s', message


if __name__ == "__main__":

    cl = Client('127.0.0.1', 12006)

    message = raw_input('Say: ')
    cl.send(message)
    asyncore.loop()
