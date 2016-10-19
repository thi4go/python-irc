from socket import *
from select import *

def broadcast(sock, msg):
    for socket in connections   :
        if socket != sock and socket != server:
            try:
                socket.send(msg)
            except:
                #cliente se desconectou
                socket.close()
                connections.remove(socket)


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

        for sock in read_sockets:
            # nova conexao a ser estabelecida, por leitura do socket server
            if sock == server:
                socket, addr = server.accept()
                socket.send(MOTD)
                connections.append(socket)
                print 'Client (%s, %s) connected' % addr
                broadcast(socket, '[%s:%s] entrou na sala\n' % addr)
                continue
            # novas mensagens de algum client
            else:
                try:
                    msg = sock.recv(buffer_size)
                    if(msg):
                        print 'Recebida mensagem: ' + msg
                        broadcast(sock, '\r' + '<' + str(sock.getpeername()) + '>' + msg)
                except:
                    broadcast(sock, 'Client (%s, %s) se desligou do servidor' % addr)
                    print 'Client (%s, %s) se desligou' % addr
                    sock_close()
                    connection.remove(sock)
                    continue

    server.close()
