from socket import *

serverHost = 'localhost'
serverPort = 50008
sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.connect((serverHost, serverPort))

while True:
    msg = input()
    sockobj.send(msg.encode())
    data = sockobj.recv(1024)
    print('Cliente recebeu:', data.decode())

    # criada uma nova variavel para receber a resposta do servidor
    data2 = sockobj.recv(1024)
    print('Servidor enviou:', data2.decode())
sockobj.close()