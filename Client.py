from socket import *
from select import *
from Entities import Client
import sys, pickle

def chat():
    sys.stdout.write('<'+nickname+'> ')
    sys.stdout.flush()

def nickIsValid(nickList, nickname):
    for n in nickList:
        if n == nickname:
            return False
    return True    

if __name__ == "__main__":

    serverName  = 'localhost'
    serverPort  = 12003
    buffer_size = 1024
    nickname    = ''

    ClientSocket = socket(AF_INET, SOCK_STREAM)
    ClientSocket.settimeout(2)

    try:
        ClientSocket.connect((serverName, serverPort))
    except:
        print 'Nao foi possivel conectar ao servidor'
        sys.exit()

    # captura mensagem de entrada no servidor, se houver
    MOTD = ClientSocket.recv(buffer_size)
    if MOTD:
        print '\n<Servidor> ' + MOTD + '\n'

    # recebe lista de nicks do servidor
    nickListSerialized = ClientSocket.recv(buffer_size)
    nickList = pickle.loads(nickListSerialized)
    # verifica unicidade dos nicks
    print 'Escolha o seu nickname: '
    nickname = raw_input()
    valid = nickIsValid(nickList, nickname)
    while(valid == False):
        print 'Este nickname ja esta sendo usado. Escolha outro: '
        nickname = raw_input()
        valid = nickIsValid(nickList, nickname)

    ClientSocket.send(nickname)

    chat()

    while 1:
        readables = [sys.stdin, ClientSocket]
        read_sockets, write_sockets, error_sockets = select(readables , [], [])

        for sock in read_sockets:
            # mensagem do servidor
            if sock == ClientSocket:
                msg = sock.recv(buffer_size)
                if msg:
                    print '\r' + msg
                    chat()
                else:
                    print 'Disconectado do servidor'
                    sys.exit()
            else:
                msg = sys.stdin.readline()
                ClientSocket.send(msg)
                chat()
