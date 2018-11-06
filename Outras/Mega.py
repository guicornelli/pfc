#!/usr/bin/python

import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import numpy as np

xlsx = pd.ExcelFile('C:/Users/guilh/Desktop/Valores.xlsx')

df = pd.read_excel(xlsx, 'Planilha3')
df.boxplot()
df.hist()
scatter_matrix(df, alpha=0.2, figsize=(6, 6), diagonal='kde')
# print (df.index, df.columns, df.count())
print(df.describe())

jogos = []
resultados = []

for i in range(df.shape[0]):
    dados = (df.PrimDezena[i], df.SegDezena[i], df.TerDezena[i], df.QuaDezena[i], df.QuiDezena[i], df.SexDezena[i])
    marcacoes = (df.Ganhadores_Sena[i])
    if marcacoes > 1:
        marcacoes = 1
    jogos.append(dados)
    resultados.append(marcacoes)

x_treino, x_teste, y_treino, y_teste = train_test_split(jogos, resultados)

Param_C = []
Param_Gamma = []
Accuracy = []

maxScore = 0
maxC = 0
maxG = 0

for cc in np.linspace(1, 10000, 5000):
    for gg in np.linspace(0.01, 10, 200):
        clf = SVC(kernel='rbf', C=cc, gamma=gg)
        clf.fit(x_treino, y_treino)
        # pred = clf.predict(x_teste)
        # acc = accuracy_score(pred, y_teste)
        score = clf.score(x_teste, y_teste)
        # print 'C = %d | acc = %f | max acc = %f'%(cc, score, maxScore)

        if score > maxScore:
            maxScore = score
            maxC = cc
            maxG = gg
            Accuracy.append((maxScore*100))
            Param_C.append(maxC)
            Param_Gamma.append(maxG)
            print('Encontrados novos cc = %d e gg = %.3f, resultando em precisao de %.3f' % (cc, gg, (score*100)), '%')

print('Max C: %d | Max Gamma = %.3f' % (maxC, maxG))
print('Max Accuracy: %.3f' % maxScore, "%")
