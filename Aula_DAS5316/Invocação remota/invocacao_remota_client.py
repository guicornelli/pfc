import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://localhost:8000')

numero1 = input("1o numero: ")
numero2 = input("2o numero: ")

print('Soma: ', s.add(int(numero1), int(numero2)))
print('Mult: ', s.mult(int(numero1), int(numero2)))
print('Pot: ', s.exp(int(numero1), int(numero2)))
print('Sub: ', s.sub(int(numero1), int(numero2)))
