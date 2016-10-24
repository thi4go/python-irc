from socket import *
from select import *
from Entities import Client
from pprint import pprint

def broadcast(sock, msg):
    for client in connections:
        if isinstance(client, Client) and client.socket != sock:
            try:
                client.socket.send(msg)
            except:
                #cliente se desconectou
                client.socket.close()
                connections.remove(client)

def acceptClient():
    socket, addr = server.accept()
    socket.send(MOTD)

    # Cria object client
    client = Client(socket, addr)
    connections.append(client)

    # Recebe o nickname do client
    client.nickname = socket.recv(buffer_size)
    print 'Client <%s> connected' % client.nickname
    broadcast(socket, '<%s> entrou na sala\n' % client.nickname)

if __name__ == "__main__":

    connections = []
    buffer_size = 1024
    MOTD        = 'Bem vindos ao sistema de comunicacao IRedesC !'
    port        = 12003

    server      = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', port))
    server.listen(5)

    connections.append(server)

    print "Servidor iniciado na porta " + str(port)

    while 1:
        read_sockets, write_sockets, error_sockets = select(connections,[],[])

        for client in read_sockets:
            # nova conexao a ser estabelecida, por leitura do socket server
            if isinstance(client, Client) == False:
                acceptClient()

            # novas mensagens de algum client
            else:
                try:
                    msg = client.socket.recv(buffer_size)
                    if(msg):
                        # print 'Recebida mensagem: ' + msg
                        broadcast(client.socket, '\r' + '<' + str(client.nickname) + '> ' + msg)
                except:
                    broadcast(client.socket, 'Client <%s> se desligou do servidor' % client.nickname)
                    print 'Client (%s, %s) se desligou' % client.address
                    client.socket.close()
                    if client in connections:
                        connections.remove(client)
                    continue

    server.close()
