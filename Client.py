from socket import *
from select import *
import sys

serverName = 'localhost'
serverPort = 12003

def chat():
    sys.stdout.write('<Me> ')
    sys.stdout.flush()

if __name__ == "__main__":

    buffer_size  = 1024
    ClientSocket = socket(AF_INET, SOCK_STREAM)
    ClientSocket.settimeout(2)

    try:
        ClientSocket.connect((serverName, serverPort))
    except:
        print 'Nao foi possivel conectar ao servidor'
        sys.exit()

    # captura mensagem de entrada no servidor, se houver1
    MOTD = ClientSocket.recv(buffer_size)
    if MOTD:
        print "<Servidor> " + MOTD

    chat()

    while 1:
        readables = [sys.stdin, ClientSocket]
        read_sockets, write_sockets, error_sockets = select(readables , [], [])

        for sock in read_sockets:
            # mensagem do servidor
            if sock == ClientSocket:
                msg = sock.recv(buffer_size)
                if msg:
                    print 'Server: %s' + msg
                    chat()
                else:
                    print 'Disconectado do servidor'
                    sys.exit()
            else:
                msg = sys.stdin.readline()
                ClientSocket.send(msg)
                chat()
