from socket import *

MOTD = 'Bem vindos ao sistema de comunicacao IRedesC !'
serverPort = 12002
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))

serverSocket.listen(1)

print MOTD

while 1:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(5)

    if sentence.startswith('/'):
        print 'eh comando'
        if sentence == '/help':
            print MOTD
            print 'Vamos te ajudar a entender o sistema'

    print "Msg orig: ", sentence, " from: ", addr
    modifiedMessage = sentence.upper()
    connectionSocket.send(modifiedMessage)
    connectionSocket.close()
