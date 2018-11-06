from socket import *

meuHost = '127.0.0.1'
minhaPort = 50008
sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((meuHost, minhaPort))
sockobj.listen(1)

while True:
    conexão, endereço = sockobj.accept()
    print('Server conectado por', endereço)

    while True:
        data = conexão.recv(1024)
        print('Cliente enviou:', data.decode())
        resposta = 'Eco=>' + data.decode()
        conexão.send(resposta.encode())

        # envia resposta ao cliente
        resp = input()
        conexão.send(resp.encode())
    conexão.close()