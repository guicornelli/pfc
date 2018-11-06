import asyncio
import datetime
import random
import websockets

# browser vai esperar uma mensagem qualquer do server, e printar no browser o que for digitado

# apos, servidor deve enviar 2 numeros, em sequencia, e o browser retornará a soma dos mesmos

async def time(websocket, path):
    while True:
        now = input("Mensagem: ")
        await websocket.send(now)
        await asyncio.sleep(random.random() * 3)
        numero1 = int(input("insira um numero: "))
        numero2 = int(input("insira outro numero: "))
        soma = numero1 + numero2
        soma = str(soma)
        await websocket.send(soma)
        await asyncio.sleep(random.random() * 3)

start_server = websockets.serve(time, '127.0.0.1', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
