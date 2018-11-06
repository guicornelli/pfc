# --------------------------------- Tamanho das Variáveis e Linha tempo de Consulta ---------------------------------- #

# ---------------------------------------------------- Imports ------------------------------------------------------- #
from infos_variaveis_copia import caracteristicas
import matplotlib.pyplot as plt
import numpy as np
import operator

# --------------------------------------------------- Bar Graph ------------------------------------------------------ #
a = []
for i in caracteristicas.keys():
    a.append([i[0:-4], caracteristicas.get(i).get('tamanho'), caracteristicas.get(i).get('t(s)exec')])
a.sort(key=operator.itemgetter(1))
a = np.array(a)

nomes = a[:, 0]
tamanho = a[:, 1].astype(int)
tempo = [round(x, 2) for x in a[:, 2].astype(float)]

fig1, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.set_xlabel("Variavel")
ax1.set_ylabel("Quantidade de pontos gravados")
ax2.set_ylabel("Tempo execução (s)")
ax1.tick_params(axis='x', labelrotation=90)
ax2.plot(tempo, 'k', marker='.', alpha=0.6)
ax1.bar(nomes, tamanho, width=0.9, alpha=0.7, label='teste')

for i in range(len(a)):
    ax1.text(x=i-0.25, y=tamanho[i]+200000, s=tamanho[i], size=8, rotation=90, color='k')
plt.subplots_adjust(bottom=0.2, top=0.99)
plt.show()

# --------------------------------------------- Range Min, Max and Avg ----------------------------------------------- #
b = []
for j in caracteristicas.keys():
    if (j != "TotalProduction_A01") and (j != "StoopedByTool_A01"):
        b.append([j[0:-4], caracteristicas.get(j).get('min'), caracteristicas.get(j).get('max'),
                  caracteristicas.get(j).get('media')])
b.sort(key=operator.itemgetter(2))
b = np.array(b)

nomes = b[:, 0]
minimo = [round(x, 2) for x in b[:, 1].astype(float)]
maximo = [round(x, 2) for x in b[:, 2].astype(float)]
avg = [round(x, 2) for x in b[:, 3].astype(float)]

plt.xlabel("Variavel")
plt.ylabel("Min, Max and Avg")
plt.xticks(rotation=90)
plt.plot(avg, 'k', marker='.', alpha=0.6)
plt.bar(nomes, minimo, width=0.9, alpha=0.7, color='r')
plt.bar(nomes, maximo, width=0.9, alpha=0.7, color='b')

for i in range(len(b)):
    plt.text(x=i-0.25, y=minimo[i]-25, s=minimo[i], size=8, rotation=90, color='k')
    plt.text(x=i-0.25, y=maximo[i]+150, s=maximo[i], size=8, rotation=90, color='k')
plt.subplots_adjust(bottom=0.2, top=0.99)
plt.show()

# ------------------------------------------------------ End --------------------------------------------------------- #
