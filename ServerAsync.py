
from Client import Client
import socket
import asyncore
import collections
import logging

chat_room = {}

logging.basicConfig(level=logging.DEBUG, format="")
log                     = logging.getLogger(__name__)

BACKLOG                 = 5
SIZE                    = 1024

class Server(asyncore.dispatcher):

    def __init__(self):
        asyncore.dispatcher.__init__(self, map=chat_room)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('', 12006))
        self.listen(5)
        self.client_list = []

    def handle_accept(self):
        log.debug("handle_accept")
        (sock, addr) = self.accept() # For the remote client.
        Handler(sock, addr)
        log.info("conn_made: client_address=%s:%s" % \
                     (sock, addr))
        self.client_list.append( (True, (sock, addr)))
        sock.send('Server: conexao aceita')

    def handle_close(self):
        self.close()

class Handler(asyncore.dispatcher):
    """Handles echoing messages from a single client.
    """

    def __init__(self, sock, addr):
        self.is_writable    = False
        self.addr           = addr
        self.buffer         = ""
        asyncore.dispatcher.__init__(self, sock)

    def writable(self):
        return self.is_writable

    def readable(self):
        return True

    def handle_read(self):
        log.debug("handle_read")
        data = self.recv(SIZE)
        # log.debug('handle_read() -> (%d) "%s"', len(data), data)
        if data:
            log.debug("got data")
            self.buffer += data
            self.is_writable = True  # sth to send back now
        else:
            log.debug("got null data")

    def handle_write(self):
        log.debug("handle_write")
        if self.buffer:
            sent = self.send(self.buffer)
            log.debug("sent data")
            self.buffer = self.buffer[sent:]
        else:
            log.debug("nothing to send")
        if len(self.buffer) == 0:
            self.is_writable = False


    def handle_close(self):
        log.debug("handle_close")
        log.info("conn_closed: client_address=%s:%s" % \
                     (self.addr[0],
                      self.addr[1]))
        self.close()


if __name__ == "__main__":

    sv = Server()

    print 'serving'
    asyncore.loop(map=chat_room)
