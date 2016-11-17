from socket import *
from select import *
from Entities import *
import sys, pickle, pprint

def chat():
    sys.stdout.write('\n<'+nickname+'> ')
    sys.stdout.flush()

def nickIsValid(nickList, nick):
    if nick in nickList:
        return False
    return True

if __name__ == "__main__":

    serverName  = 'localhost'
    serverPort  = 12003
    buffer_size = 1024

    nickname    = ''
    room        = ''

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
        print '\n' + MOTD + '\n'

    # recebe lista de nicks do servidor
    nickListSerialized = ClientSocket.recv(buffer_size)
    nickList           = pickle.loads(nickListSerialized)

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

                if msg.startswith('/nick'):
                    ClientSocket.send(msg)
                    string1   = msg.split(' ')
                    string2   = string1[1].split('\n')
                    newnick   = string2[0]
                    response  = ClientSocket.recv(buffer_size)
                    pprint.pprint(response)
                    raw_input()
                    if(response == 'valid'):
                        print '\nModificado nickname de <%s> para <%s>\n' % (nickname, newnick)
                        nickname  = newnick
                    else:
                        nickList = pickle.loads(response)

                        valid = nickIsValid(nickList, newnick)

                        while(valid == False):
                            print 'Este nickname ja esta sendo usado. Escolha outro: '
                            newnick = raw_input()
                            valid    = nickIsValid(nickList, newnick)

                        print '\nModificado nickname de <%s> para <%s>\n' % (nickname, newnick)
                        ClientSocket.send('/nick ' + newnick)
                        nickname  = newnick

                elif msg.startswith('/help'):
                    ClientSocket.send(msg)
                    response = ClientSocket.recv(buffer_size)
                    print '\r' + response

                elif msg.startswith('/list'):
                    ClientSocket.send(msg)
                    serialized = ClientSocket.recv(buffer_size)
                    roomList   = pickle.loads(serialized)
                    pprint.pprint(roomList)
                    # raw_input()

                else:
                    ClientSocket.send(msg)

                chat()
