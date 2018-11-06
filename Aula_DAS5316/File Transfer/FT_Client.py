import socket

s = socket.socket()
s2 = socket.socket()
host = 'localhost'
port = 60001
port2 = 60002
s.connect((host, port))

with open('FT_arquivo_recebido.xlsx', 'wb') as f:
    print('Arquivo Aberto')
    while True:
        print('Recebendo dados...')
        data = s.recv(1024*16)
        if not data:
            break
        f.write(data)

f.close()
print('Transferência realizada com sucesso')
s.close()
print('Conexão fechada')

# após primeira transferência de arquivo, a execução ira aguardar um ok
# este ok é dado após editar manualmente o arquivo transferido
# e entao o cliente transfere o arquivo editado para outro cliente

print(input("espera meu ok: "))

s2.bind((host, port2))
s2.listen(1)

while True:
    conn2, addr2 = s2.accept()
    print('Conectado por:', addr2)

    filename = 'FT_arquivo_recebido.xlsx'
    f2 = open(filename, 'rb')
    l2 = f2.read(1024*16)
    while (l2):
       conn2.send(l2)
       l2 = f2.read(1024*16)
    f2.close()

    print('Envio completo')
    conn2.close()

s2.close()
print('Conexão fechada')