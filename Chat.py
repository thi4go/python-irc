from socket import *
from select import *
from Entities import *
from ServerEntity import *
import pickle, logging, sys, pprint


if __name__ == "__main__":

    buffer_size = 1024

    server = Server()
    server.run()

    while 1:
        read_sockets, write_sockets, error_sockets = select(server.connections,[],[])

        for client in read_sockets:
            # nova conexao a ser estabelecida, por leitura do socket server
            if isinstance(client, Client) == False:
                server.accept_client()

            # novas mensagens de algum client
            else:
                try:
                    msg = client.socket.recv(buffer_size)

                    if(msg):
                        if msg.startswith('/help'):
                            server.handle_help()
                        elif msg.startswith('/nick'):
                            server.handle_nick()
                        elif msg.startswith('/list'):
                            server.handle_list()
                        else:
                            server.logger.info('Recebida mensagem de <%s>: %s' % (client.nickname, msg))
                            server.broadcast(client.socket, '<%s> %s' % (client.nickname, msg))
                except:
                    server.broadcast(client.socket, '<Servidor> Client <%s> se desligou do servidor' % client.nickname)
                    server.logger.info('Client (%s, %s) se desligou' % client.address)
                    client.socket.close()
                    if client in server.connections:
                        server.connections.remove(client)
                    continue

    server.server.close()
