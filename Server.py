from socket import *
from select import *
from Entities import Client
import pickle, logging, sys

# logging.basicConfig(filename='IRedesC.log',level=logging.DEBUG)
logging.basicConfig(filename='IRedesC.log', level=logging.DEBUG, format="%(created)-15s %(levelname)8s %(name)s %(message)s")
log = logging.getLogger(__name__)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)

log.addHandler(ch)

def broadcast(sock, msg):
    for client in connections:
        if isinstance(client, Client) and client.socket != sock:
            try:
                client.socket.send(msg)
            except:
                #cliente se desconectou
                client.socket.close()
                connections.remove(client)

def sendNicknameList(socket):
    nicks = []
    for client in connections:
        if isinstance(client, Client):
            nicks.append(client.nickname)
    data = pickle.dumps(nicks)
    socket.send(data)

def acceptClient():
    socket, addr = server.accept()
    socket.send(MOTD)
    sendNicknameList(socket)

    # Cria object client
    client = Client(socket, addr)
    connections.append(client)

    # Recebe o nickname do client
    client.nickname = socket.recv(buffer_size)
    log.info('Client <%s> se conectou' % client.nickname)
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

    log.info("Servidor iniciado na porta " + str(port))
    # print "Servidor iniciado na porta " + str(port)

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
                        if msg.startswith('/'):
                            if str(msg) == '/help':
                                print 'eh /help'
                                start    = 'Lista dos comandos disponiveis:\n'
                                listc    = '/list  - lista as salas de chat criadas\n'
                                leavec   = '/leave - sai da sala e retorna ao menu inicial\n'
                                response = start + listc + leavec
                                client.socket.send(response)
                        else:
                            log.info('Recebida mensagem de + str(client.address) + : ' + msg)
                            broadcast(client.socket, '<' + str(client.nickname) + '> ' + msg)
                except:
                    broadcast(client.socket, 'Client <%s> se desligou do servidor' % client.nickname)
                    log.info('Client (%s, %s) se desligou' % client.address)
                    client.socket.close()
                    if client in connections:
                        connections.remove(client)
                    continue

    server.close()
