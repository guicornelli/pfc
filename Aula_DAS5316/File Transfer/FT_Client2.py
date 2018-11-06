import socket

s2 = socket.socket()
host = 'localhost'
port = 60002

s2.connect((host, port))

# recebe o novo arquivo editado, sobrescrevendo o primeiro enviado

with open('FT_teste.xlsx', 'wb') as f:
    print('Arquivo Aberto')
    while True:
        print('Recebendo dados...')
        data = s2.recv(1024*16)
        if not data:
            break
        f.write(data)


f.close()
print('Transferência realizada com sucesso')
s2.close()
print('Conexão fechada')