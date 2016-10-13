from socket import *

serverName = '127.0.0.1'
serverPort = 12002



while 1:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect( (serverName, serverPort) )
    message = raw_input('Input lowercase sentence: ')

    clientSocket.send(message)

    modifiedMessage = clientSocket.recv(2048)

    print 'From Server: ', modifiedMessage

clientSocket.close()
