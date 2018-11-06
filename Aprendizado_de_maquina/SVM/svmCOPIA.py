import pymssql
import numpy as np
# import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import pandas as pd
# import seaborn as sns
# import squarify
# import matplotlib
from datetime import timedelta
from sklearn.svm import SVC
from time import time
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, confusion_matrix

# -------------------------------------------------------------------------------------------------------------------- # Configurar display de valores e resultados no console
np.set_printoptions(linewidth=500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# -------------------------------------------------------------------------------------------------------------------- # Conexão com BD SQL Server
conn = pymssql.connect(host='GUILHERME', user='roquec', password='roquec', database='GAMESA', as_dict=False,
                       charset='UTF-8')

# -------------------------------------------------------------------------------------------------------------------- # String da consulta para puxar os dados
consulta = ("SELECT * "
            "FROM [Alarmes_Morrinhos_6Aeros]"
            "WHERE	[AlarmDesc] LIKE '518 %'"                                                                          # Consultando apenas o alarme 518
            "ORDER BY [TimeIniUTC];")

# -------------------------------------------------------------------------------------------------------------------- # Biblioteca Pandas fará a consulta e disopnibilizará resultado no Dataframe
df = pd.read_sql(consulta, conn)
# df.head()                                                         # exemplifica como ficou
# df.info()                                                         # infos do dataframe
conn.close()                                                        # fecha porta de comunicação com o BD GAMESA

indexes = df[((df['TimeIniUTC'] > pd.Timestamp(2017, 11, 10, 0, 0, 0)) & (df['TimeIniUTC'] < pd.Timestamp(2017, 12, 27, 0, 0, 0))) |         # pega os index dos pontos em que não ha mediçao analogica
             (df['TimeIniUTC'] > pd.Timestamp(2018, 1, 9, 11, 0, 0))].index.values
df.drop(indexes, inplace=True)                                                                                                               # remove do dataframe os index selecionados
df.reset_index(drop=True, inplace=True)
df['TimeEndUTC'][2] = pd.Timestamp(2017, 10, 16, 21, 0, 26)                                                                                  # estou simplificando os alarmes
df['TimeEndUTC'][35] = pd.Timestamp(2017, 10, 21, 18, 43, 7)                                                                                 # haviam muitas ocorrencias em sequencia, o que é a mesma
df['TimeEndUTC'][41] = pd.Timestamp(2017, 10, 25, 4, 28, 57)                                                                                 # situacao em que haver uma ocorrencia com periodo de tempo
df['TimeEndUTC'][51] = pd.Timestamp(2017, 10, 25, 19, 45, 35)                                                                                # maior
df.drop(range(3, 35), inplace=True)                                                                                                          # retiro onde há muitas ocorrencias
df.drop(range(36, 40), inplace=True)
df.drop(range(42, 51), inplace=True)
df.drop(range(52, 57), inplace=True)
df.reset_index(drop=True, inplace=True)                                                                                                      # reinicia o index

deltas = df['TimeEndUTC'] - df['TimeIniUTC']                          # faz o delta entre tempo de inicio e termino de atuacao
df.insert(loc=2, column='Delta', value=deltas)                        # insere os deltas no dataframe

codes = []
for n in df['AlarmDesc']:                                             # adicionar uma coluna com os códigos dos alarmes no dataframe df
    try:
        if (int(n[0:3])) != 175:
            codes.append(int(n[0:4]))
        else:
            codes.append(int(0))
    except ValueError:
        codes.append(int(0))
df.insert(loc=3, column='Codes', value=codes)

# -------- # Classificação das reações de cada alarme
aviso = [117, 211, 315, 413, 419, 423, 427, 429, 430, 506, 514, 515, 516, 517,
         518, 703, 707, 711, 718, 721, 823, 1828, 2100, 2115, 2116, 2131, 2198]

pausa = [114, 203, 306, 312, 313, 402, 403, 407, 426, 500, 501, 502, 600,
         615, 915, 916, 1821, 1822, 2106]

stop = [103, 108, 110, 409, 812, 906, 913]

emerg = [119, 201, 205, 208, 212, 222, 405, 410, 416, 603, 700, 813, 900,
         901, 902, 907, 908, 911, 912, 1835, 1837, 2102, 2114, 2118, 5201,
         5203, 5204, 5210, 5212, 5213, 5216, 5226, 5232, 5237, 5238, 5240]

# -------- # Classificação da disponibilidade do aerogerador conforme cada alarme atuado
disp = [117, 211, 313, 315, 405, 413, 419, 423, 427, 429, 430, 506, 514, 515, 516,
        517, 518, 703, 707, 711, 718, 721, 823, 1828, 2100, 2115, 2116, 2131, 2198]

reac = []
disponib = []

for i in df['Codes']:                                                 # verifica linha por linha qual o código e cria uma lista com a reação e disponibilidade conforme o alarme / evento
    if i in aviso:
        reac.append("Aviso")
    elif i in pausa:
        reac.append("Pausa")
    elif i in stop:
        reac.append("Stop")
    elif i in emerg:
        reac.append("Emerg")
    else:
        reac.append("NaN")

for i in df['Codes']:
    i = i
    if i in disp:
        disponib.append("Sim")
    elif i == 0:
        disponib.append("NaN")
    else:
        disponib.append("Nao")

df.insert(loc=6, column='Reacao', value=reac)                         # adicionar as coluna com as reações e disponibilidade no dataframe df
df.insert(loc=7, column='Disponibilidade', value=disponib)

mask = df['Codes'] == 0                                               # separar o dataframe df em dois: ec = estados e comandos, al = alarmes da listagem Gamesa
ec = df[mask]
ec.reset_index(drop=True, inplace=True)                               # reset no index
al = df[~mask]
al.reset_index(drop=True, inplace=True)

# tsuniques = al.groupby('AlarmAero')['TimeIniUTC'].unique()            # tempos que ocorreram as falhas por aero

dftrain1 = al.iloc[2:9]                                               # separando em dados para treino e teste
dftrain2 = al.iloc[10:]
dftest1 = al.iloc[:2]
dftest2 = al.iloc[9:10]
dfframestrain = [dftrain1, dftrain2]
dfframestest = [dftest1, dftest2]
df_train = pd.concat(dfframestrain)
df_test = pd.concat(dfframestest)

variables = ['GenNCSBearingTemp', 'GenSpeed', 'GridCurrent']          # variaveis analogicas a serem utilizadas

conn = pymssql.connect(host='GUILHERME', user='roquec', password='roquec', database='ISOTROL', as_dict=False,            # inicia conexao com BD ISOTROL
                       charset='UTF-8')

# -------------------------------------------------------------------------------------------------------------------- # aero 20
cur = conn.cursor()
cur.execute("SELECT dbo.GenNCSBearingTemp_A20.TimeStampDateTimeUTC, dbo.GenNCSBearingTemp_A20.FieldValueConvert, "
            "dbo.GenSpeed_A20.FieldValueConvert, dbo.GridCurrent_A20.FieldValueConvert "
            "FROM dbo.GenNCSBearingTemp_A20 INNER JOIN "
            "dbo.GenSpeed_A20 ON dbo.GenNCSBearingTemp_A20.TimeStampDateTimeUTC = dbo.GenSpeed_A20.TimeStampDateTimeUTC INNER JOIN "
            "dbo.GridCurrent_A20 ON dbo.GenSpeed_A20.TimeStampDateTimeUTC = dbo.GridCurrent_A20.TimeStampDateTimeUTC "
            "ORDER BY [TimeStampDateTimeUTC]; ")

timestamp20 = []
val_genNCS20 = []
val_genS20 = []
val_curGrid20 = []

for row in cur:
    timestamp20.append(row[0])
    val_genNCS20.append(row[1])
    val_genS20.append(row[2])
    val_curGrid20.append(row[3])

cur.close()
timestamp20 = np.array(timestamp20)
val_genNCS20 = np.array(val_genNCS20)
val_genS20 = np.array(val_genS20)
val_curGrid20 = np.array(val_curGrid20)
amostra20 = len(timestamp20)
# --------------------------------------------Duplicados e Congelados--------------------------------------------- #
errorsTS20 = []
errorsV120 = []
errorsV220 = []
errorsV320 = []
val_ncs20 = []
val_s20 = []
val_cur20 = []
ts20 = []

for k in range(amostra20 - 1):
    k = k + 1
    diffTS20 = timestamp20[k] - timestamp20[k - 1]
    diffV120 = val_genNCS20[k] - val_genNCS20[k - 1]
    diffV220 = val_genS20[k] - val_genS20[k - 1]
    diffV320 = val_curGrid20[k] - val_curGrid20[k - 1]
    if diffTS20 == timedelta(0):                                                    # duplicados
        if (timestamp20[k - 1].minute % 10 == 0) and (timestamp20[k - 1].second < 7):
            ts20.append(timestamp20[k])
            val_ncs20.append(val_genNCS20[k])
            val_s20.append(val_genS20[k])
            val_cur20.append(val_curGrid20[k])
        else:
            errorsTS20.append(timestamp20[k])
            errorsV120.append(val_genNCS20[k])
            errorsV220.append(val_genS20[k])
            errorsV320.append(val_curGrid20[k])
    elif (timestamp20[k].minute % 10 == 0) and (timestamp20[k].second < 7):           # congelados
        if (timestamp20[k - 1].minute % 10 == 0) and (timestamp20[k - 1].second < 7) and (diffTS20.seconds < 500):
            ts20.append(timestamp20[k])
            val_ncs20.append(val_genNCS20[k])
            val_s20.append(val_genS20[k])
            val_cur20.append(val_curGrid20[k])
        else:
            errorsTS20.append(timestamp20[k])
            errorsV120.append(val_genNCS20[k])
            errorsV220.append(val_genS20[k])
            errorsV320.append(val_curGrid20[k])
    else:                                                                         # amostra filtrada
        ts20.append(timestamp20[k])
        val_ncs20.append(val_genNCS20[k])
        val_s20.append(val_genS20[k])
        val_cur20.append(val_curGrid20[k])

val_genNCS20 = np.array(val_ncs20)
val_genS20 = np.array(val_s20)
val_curGrid20 = np.array(val_cur20)
timestamp20 = np.array(ts20)

# -------------------------------------------------------------------------------------------------------------------- # aero 58
cur = conn.cursor()
cur.execute("SELECT dbo.GenNCSBearingTemp_A58.TimeStampDateTimeUTC, dbo.GenNCSBearingTemp_A58.FieldValueConvert, "
            "dbo.GenSpeed_A58.FieldValueConvert, dbo.GridCurrent_A58.FieldValueConvert "
            "FROM dbo.GenNCSBearingTemp_A58 INNER JOIN "
            "dbo.GenSpeed_A58 ON dbo.GenNCSBearingTemp_A58.TimeStampDateTimeUTC = dbo.GenSpeed_A58.TimeStampDateTimeUTC INNER JOIN "
            "dbo.GridCurrent_A58 ON dbo.GenSpeed_A58.TimeStampDateTimeUTC = dbo.GridCurrent_A58.TimeStampDateTimeUTC "
            "ORDER BY [TimeStampDateTimeUTC]; ")

timestamp58 = []
val_genNCS58 = []
val_genS58 = []
val_curGrid58 = []

for row in cur:
    timestamp58.append(row[0])
    val_genNCS58.append(row[1])
    val_genS58.append(row[2])
    val_curGrid58.append(row[3])

cur.close()
timestamp58 = np.array(timestamp58)
val_genNCS58 = np.array(val_genNCS58)
val_genS58 = np.array(val_genS58)
val_curGrid58 = np.array(val_curGrid58)
amostra58 = len(timestamp58)
# --------------------------------------------Duplicados e Congelados--------------------------------------------- #
errorsTS58 = []
errorsV158 = []
errorsV258 = []
errorsV358 = []
val_ncs58 = []
val_s58 = []
val_cur58 = []
ts58 = []

for k in range(amostra58 - 1):
    k = k + 1
    diffTS58 = timestamp58[k] - timestamp58[k - 1]
    diffV158 = val_genNCS58[k] - val_genNCS58[k - 1]
    diffV258 = val_genS58[k] - val_genS58[k - 1]
    diffV358 = val_curGrid58[k] - val_curGrid58[k - 1]
    if diffTS58 == timedelta(0):                                                    # duplicados
        if (timestamp58[k - 1].minute % 10 == 0) and (timestamp58[k - 1].second < 7):
            ts58.append(timestamp58[k])
            val_ncs58.append(val_genNCS58[k])
            val_s58.append(val_genS58[k])
            val_cur58.append(val_curGrid58[k])
        else:
            errorsTS58.append(timestamp58[k])
            errorsV158.append(val_genNCS58[k])
            errorsV258.append(val_genS58[k])
            errorsV358.append(val_curGrid58[k])
    elif (timestamp58[k].minute % 10 == 0) and (timestamp58[k].second < 7):           # congelados
        if (timestamp58[k - 1].minute % 10 == 0) and (timestamp58[k - 1].second < 7) and (diffTS58.seconds < 500):
            ts58.append(timestamp58[k])
            val_ncs58.append(val_genNCS58[k])
            val_s58.append(val_genS58[k])
            val_cur58.append(val_curGrid58[k])
        else:
            errorsTS58.append(timestamp58[k])
            errorsV158.append(val_genNCS58[k])
            errorsV258.append(val_genS58[k])
            errorsV358.append(val_curGrid58[k])
    else:                                                                         # amostra filtrada
        ts58.append(timestamp58[k])
        val_ncs58.append(val_genNCS58[k])
        val_s58.append(val_genS58[k])
        val_cur58.append(val_curGrid58[k])

val_genNCS58 = np.array(val_ncs58)
val_genS58 = np.array(val_s58)
val_curGrid58 = np.array(val_cur58)
timestamp58 = np.array(ts58)

conn.close()                                                                       # fecha porta de comunicação com o BD

# -------------------------------------------------------------------------------------------------------------------- #


def removeoutlier(values1, values2, values3, times):  # define a função com uma variavel de entrada
    fator = 3  # 1.5 é o fator de multiplicacao
    q75, q25 = np.percentile(values1, [75, 25])  # retorna o terceiro e primeiro quartil
    iqr = q75 - q25  # calcula o iqr(interquartile range)

    lowpass = q25 - (iqr * fator)  # calcula o valor minimo para aplicar no filtro
    highpass = q75 + (iqr * fator)  # calcula o valor maximo para aplicar no filtro

    outliers = np.argwhere(values1 < lowpass)  # descobre onde estao os valores menores que o valor minimo
    values1 = np.delete(values1, outliers)     # deleta esses valores
    values2 = np.delete(values2, outliers)
    values3 = np.delete(values3, outliers)
    times = np.delete(times, outliers)

    outliers = np.argwhere(values1 > highpass)  # descobre onde estao os valores maiores que o valor maximo
    values1 = np.delete(values1, outliers)  # deleta esses valores
    values2 = np.delete(values2, outliers)
    values3 = np.delete(values3, outliers)
    times = np.delete(times, outliers)

    return values1, values2, values3, times, q75, q25  # retorna a variavel sem outliers


val1SemOut20, val2SemOut20, val3SemOut20, tsSemOut20, q7520, q2520 = removeoutlier(val_genNCS20, val_genS20, val_curGrid20, timestamp20)
val1SemOut58, val2SemOut58, val3SemOut58, tsSemOut58, q7558, q2558 = removeoutlier(val_genNCS58, val_genS58, val_curGrid58, timestamp58)
# -------------------------------------------------------------------------------------------------------------------- #
dados1 = {'Timestamp': tsSemOut20, 'GenNCSBearingTemp': val1SemOut20, 'GenSpeed': val2SemOut20, 'GridCurrent': val3SemOut20}
df_analogic1 = pd.DataFrame(data=dados1)
dados2 = {'Timestamp': tsSemOut58, 'GenNCSBearingTemp': val1SemOut58, 'GenSpeed': val2SemOut58, 'GridCurrent': val3SemOut58}
df_analogic2 = pd.DataFrame(data=dados2)

'''fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex='all', sharey='all', figsize=(19.2, 10.8), dpi=100)
df_analogic1.plot(x='Timestamp', y='GenNCSBearingTemp', style=".", ax=ax1)
df_analogic1.plot(x='Timestamp', y='GenSpeed', style=".", ax=ax2)
df_analogic1.plot(x='Timestamp', y='GridCurrent', style=".", ax=ax3)'''

classifications1 = []
classifications2 = []
df_analogic1["Labels"] = ""
df_analogic2["Labels"] = ""

# abs(al['TimeIniUTC'][al['AlarmAero'] == 'MOR05'][0]-df_analogic['Timestamp'][100000])

# np.where(abs(al['TimeIniUTC'][al['AlarmAero'] == 'MOR05'][0] - df_analogic.Timestamp) < timedelta(0,3600))[0]

for n in al['TimeIniUTC'][al['AlarmAero'] == 'MOR05']:
    df_analogic2.loc[np.where(abs(n - df_analogic2.Timestamp) < timedelta(0, 3600))[0], 'Labels'] = 1

for n in al['TimeIniUTC'][al['AlarmAero'] == 'CF206']:
    df_analogic1.loc[np.where(abs(n - df_analogic1.Timestamp) < timedelta(0, 3600))[0], 'Labels'] = 1

df_analogic1.loc[np.where(df_analogic1.Labels != 1)[0], 'Labels'] = 0
df_analogic2.loc[np.where(df_analogic2.Labels != 1)[0], 'Labels'] = 0

from mpl_toolkits.mplot3d import Axes3D
x1 = df_analogic1['GenNCSBearingTemp'][df_analogic1['Labels'] == 1]
y1 = df_analogic1['GenSpeed'][df_analogic1['Labels'] == 1]
z1 = df_analogic1['GridCurrent'][df_analogic1['Labels'] == 1]

x0 = df_analogic1['GenNCSBearingTemp'][df_analogic1['Labels'] == 0]
y0 = df_analogic1['GenSpeed'][df_analogic1['Labels'] == 0]
z0 = df_analogic1['GridCurrent'][df_analogic1['Labels'] == 0]

fig = plt.figure(figsize=(10.8, 7.2), dpi=100)
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x1, y1, z1, c='r', marker='^')
ax.set_xlabel('Gen NCS Temp A20')
ax.set_ylabel('Gen Speed A20')
ax.set_zlabel('Curr Grid A20')
# ax.scatter(x0, y0, z0)

x12 = df_analogic2['GenNCSBearingTemp'][df_analogic2['Labels'] == 1]
y12 = df_analogic2['GenSpeed'][df_analogic2['Labels'] == 1]
z12 = df_analogic2['GridCurrent'][df_analogic2['Labels'] == 1]

x02 = df_analogic2['GenNCSBearingTemp'][df_analogic2['Labels'] == 0]
y02 = df_analogic2['GenSpeed'][df_analogic2['Labels'] == 0]
z02 = df_analogic2['GridCurrent'][df_analogic2['Labels'] == 0]

fig2 = plt.figure(figsize=(10.8, 7.2), dpi=100)
ax2 = fig2.add_subplot(111, projection='3d')
ax2.scatter(x12, y12, z12, c='r', marker='^')
ax2.set_xlabel('Gen NCS Temp A58')
ax2.set_ylabel('Gen Speed A58')
ax2.set_zlabel('Curr Grid A58')
# ax2.scatter(x02, y02, z02, facecolors='none', edgecolors='', marker=',', marker='o', lw=0, s=(72./fig.dpi)**2)

# -------------------------------------------------------------------------------------------------------------------- # agr separar em analogic treino e teste
first_cut_date1 = np.argwhere(abs(df_analogic1['Timestamp'] - pd.Timestamp(2017, 4, 19)) < timedelta(0, 360))[0][0]
second_cut_date1 = np.argwhere(abs(df_analogic1['Timestamp'] - pd.Timestamp(2017, 5, 10)) < timedelta(0, 360))[0][0]
third_cut_date1 = np.argwhere(abs(df_analogic1['Timestamp'] - pd.Timestamp(2017, 9, 21)) < timedelta(0, 360))[0][0]
fourth_cut_date1 = np.argwhere(abs(df_analogic1['Timestamp'] - pd.Timestamp(2017, 10, 12)) < timedelta(0, 360))[0][0]
fifith_cut_date1 = np.argwhere(abs(df_analogic1['Timestamp'] - pd.Timestamp(2018, 1, 2)) < timedelta(0, 360))[0][0]
sixth_cut_date1 = np.argwhere(abs(df_analogic1['Timestamp'] - pd.Timestamp(2018, 1, 7)) < timedelta(0, 360))[0][0]
seventh_cut_date1 = np.argwhere(abs(df_analogic1['Timestamp'] - pd.Timestamp(2018, 1, 9, 10)) < timedelta(0, 360))[0][0]

first_cut_date2 = np.argwhere(abs(df_analogic2['Timestamp'] - pd.Timestamp(2017, 4, 19)) < timedelta(0, 360))[0][0]
second_cut_date2 = np.argwhere(abs(df_analogic2['Timestamp'] - pd.Timestamp(2017, 5, 10)) < timedelta(0, 360))[0][0]
third_cut_date2 = np.argwhere(abs(df_analogic2['Timestamp'] - pd.Timestamp(2017, 9, 21)) < timedelta(0, 360))[0][0]
fourth_cut_date2 = np.argwhere(abs(df_analogic2['Timestamp'] - pd.Timestamp(2017, 10, 12)) < timedelta(0, 360))[0][0]
fifith_cut_date2 = np.argwhere(abs(df_analogic2['Timestamp'] - pd.Timestamp(2018, 1, 2)) < timedelta(0, 360))[0][0]
sixth_cut_date2 = np.argwhere(abs(df_analogic2['Timestamp'] - pd.Timestamp(2018, 1, 7)) < timedelta(0, 360))[0][0]
seventh_cut_date2 = np.argwhere(abs(df_analogic2['Timestamp'] - pd.Timestamp(2018, 1, 9, 10)) < timedelta(0, 360))[0][0]

dftrain_A11 = df_analogic1.iloc[:first_cut_date1]                                                                       # separando em dados para treino e teste
dftrain_A21 = df_analogic1.iloc[second_cut_date1:third_cut_date1]
dftrain_A31 = df_analogic1.iloc[fourth_cut_date1:fifith_cut_date1]
dftrain_A41 = df_analogic1.iloc[sixth_cut_date1:seventh_cut_date1]
dftest_A11 = df_analogic1.iloc[first_cut_date1:second_cut_date1]
dftest_A21 = df_analogic1.iloc[third_cut_date1:fourth_cut_date1]
dftest_A31 = df_analogic1.iloc[fifith_cut_date1:sixth_cut_date1]
dfframestrain_A1 = [dftrain_A11, dftrain_A21, dftrain_A31, dftrain_A41]
dfframestest_A1 = [dftest_A11, dftest_A21, dftest_A31]
dftrain_A1 = pd.concat(dfframestrain_A1)
dftest_A1 = pd.concat(dfframestest_A1)

dftrain_A12 = df_analogic2.iloc[:first_cut_date2]                                             # separando em dados para treino e teste
dftrain_A22 = df_analogic2.iloc[second_cut_date2:third_cut_date2]
dftrain_A32 = df_analogic2.iloc[fourth_cut_date2:fifith_cut_date2]
dftrain_A42 = df_analogic2.iloc[sixth_cut_date2:seventh_cut_date2]
dftest_A12 = df_analogic2.iloc[first_cut_date2:second_cut_date2]
dftest_A22 = df_analogic2.iloc[third_cut_date2:fourth_cut_date2]
dftest_A32 = df_analogic2.iloc[fifith_cut_date2:sixth_cut_date2]
dfframestrain_A2 = [dftrain_A12, dftrain_A22, dftrain_A32, dftrain_A42]
dfframestest_A2 = [dftest_A12, dftest_A22, dftest_A32]
dftrain_A2 = pd.concat(dfframestrain_A2)
dftest_A2 = pd.concat(dfframestest_A2)

'''fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex='all', sharey='all', figsize=(19.2, 10.8), dpi=100)
dftrain_A1.plot(x='Timestamp', y='Labels', style=".", ax=ax1)
dftest_A1.plot(x='Timestamp', y='Labels', style=".", ax=ax2)
dftrain_A2.plot(x='Timestamp', y='Labels', style=".", ax=ax3)
dftest_A2.plot(x='Timestamp', y='Labels', style=".", ax=ax4)'''

# -------------------------------------------------------------------------------------------------------------------- # concatenando e dividindo

result_train = pd.concat([dftrain_A1, dftrain_A2])
result_train.drop('Timestamp', axis=1, inplace=True)
result_train.reset_index(drop=True, inplace=True)

xtrain = result_train.drop('Labels', axis=1)
ytrain = result_train['Labels']

result_test = pd.concat([dftest_A1, dftest_A2])
result_test.drop('Timestamp', axis=1, inplace=True)
result_test.reset_index(drop=True, inplace=True)

xtest = result_test.drop('Labels', axis=1)
ytest = result_test['Labels']

svclassifier = SVC(kernel='rbf', C=1, gamma=100)

t0 = time()
svclassifier.fit(xtrain, ytrain)
print("tempo de treinamento:", round(time()-t0, 3), "s")
t1 = time()
y_pred = svclassifier.predict(xtest)
print("tempo de testes:", round(time()-t1, 3), "s")

acc = accuracy_score(y_pred, ytest)
print("accuracy: ", acc)
print(confusion_matrix(ytest, y_pred))
print(classification_report(ytest, y_pred))


