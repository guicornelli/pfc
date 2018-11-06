""" A raiz quadrada de um numero x é um y tal que y*y = x

1 - Comece com um valor estimado g
2 - Se g*g está perto o suficiente de x, pare e diga que g é a resposta
3 - Caso contrário, faça uma nova estimativa calculando a média g e x/g
4 - Usando uma nova estimativa, repita o processo até chegar perto do valor"""


def raiz(numero):
    g = 1
    est = g*g
    while abs(numero-est) > 0.001:
        num_g = numero/g
        med = (num_g + g) / 2
        g = med
        est = med*med
        print(g, est)
    print (g, est)

raiz(10)