from Entities import *
from socket import *
import pickle, logging, sys, pprint

class Server():

    buffer_size = 1024
    port        = 12003

    def __init__(self):
        self.connections = []
        self.rooms       = []
        self.server      = None
        self.logger      = None
        self.MOTD        = '<Servidor> Bem vindos ao sistema de comunicacao IRedesC !'

    def run():
        start_logger()
        start_socket_server()
        lobby = Room('Lobby', self.server)
        self.rooms.append(lobby)
        self.logger.info('Servidor iniciado na porta ' + str(self.port))

    def accept_client():
        socket, address = self.server.accept()
        socket.send(self.MOTD)
        self.send_nickname_list(socket)

        client          = Client(socket, address)
        client.room     = 'Lobby'
        client.nickname = socket.recv(buffer_size)

        self.connections.append(client)
        self.logger.info('Client <%s> se conectou' % client.nickname)
        self.broadcast(socket, '<%s> entrou na sala\n' % client.nickname)

    def send_nickname_list(socket):
        nicks = []
        for client in self.connections:
            if isinstance(client, Client):
                nicks.append(client.nickname)
        data = pickle.dumps(nicks)
        socket.send(data)

    def is_nick_valid(nickList, nick):
        if nick in nickList:
            return False
        return True

    def handle_help(client):
        start    = '\nLista dos comandos disponiveis:\n'
        nick     = '    /nick <novo nick> - modifica o seu nickname\n'
        listc    = '    /list             - lista as salas de chat criadas\n'
        leavec   = '    /leave            - sai da sala e retorna ao menu inicial\n'
        response = start + nick + listc + leavec
        client.socket.send(response)

    def handle_nick(msg, client):
        string1   = msg.split(' ')
        string2   = string1[1].split('\n')
        newnick   = string2[0]
        valid     = self.nick_is_valid(newnick)
        if(valid == True):
            client.socket.send('valid')
            self.broadcast(client.socket, '<Servidor> Cliente <%s> mudou seu nickname para <%s> ' % (client.nickname, newnick))
            self.logger.info('Client <%s> modificou o nick para <%s>' % (client.nickname, newnick))
            client.nickname = newnick
        else:
            self.send_nickname_list(client.socket)

    def handle_list(client):
        self.logger.info('/list chamado por %s' % client.nickname)
        names = []
        for room in rooms:
            names.append('id: ' + room.id + 'nome: ' + room.name)
        data = pickle.dumps(names)
        client.socket.send(data)

    def start_logger():
        logging.basicConfig(filename='IRedesC.log', level=logging.DEBUG, format="%(created)-15s %(levelname)8s %(name)s %(message)s")
        log = logging.getLogger(__name__)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        log.addHandler(ch)
        self.logger = log

    def start_socket_server():
        server = socket(AF_INET, SOCK_STREAM)
        self.server = server
        self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server.bind(('0.0.0.0', port))
        self.server.listen(5)
        self.connections.append(self.server)

    def broadcast(socket, msg):
        for client in self.connections:
            if isinstance(client, Client) and client.socket != socket:
                try:
                    client.socket.send(msg)
                except:
                    client.socket.close()
                    self.connections.remove(client)
