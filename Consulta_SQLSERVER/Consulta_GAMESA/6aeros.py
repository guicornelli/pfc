# -------------------------------------------------------------------------------------------------------------------- # CONSULTAR E ANALISAR BANCO DE DADOS DE ALARMES E EVENTOS DOS 6 AEROGERADORES #
import pymssql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------------------------------------------------------------------------------- # Configurar display de valores e resultados no console
np.set_printoptions(linewidth=500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# -------------------------------------------------------------------------------------------------------------------- # Conexão com BD SQL Server
conn = pymssql.connect(host='GUILHERME', user='roquec', password='roquec', database='GAMESA', as_dict=False,
                       charset='UTF-8')

# -------------------------------------------------------------------------------------------------------------------- # String da consulta para puxar os dados
consulta = ("SELECT DISTINCT * "
            "FROM [Alarmes_Morrinhos_6Aeros] "
            "ORDER BY [TimeIniUTC]; ")

# -------------------------------------------------------------------------------------------------------------------- # Biblioteca Pandas fará a consulta e disopnibilizará resultado no Dataframe
df = pd.read_sql(consulta, conn)
# df.head()                                                         # exemplifica como ficou
# df.info()                                                         # infos do dataframe
conn.close()                                                        # Fecha porta de comunicação com o BD

deltas = df['TimeEndUTC'] - df['TimeIniUTC']                        # faz o delta entre tempo de inicio e termino de atuacao
df.insert(loc=2, column='Delta', value=deltas)                      # insere os deltas no dataframe

indexes = df[((df['TimeIniUTC'] > pd.Timestamp(2017, 11, 10, 0, 0, 0)) & (df['TimeIniUTC'] < pd.Timestamp(2017, 12, 27, 0, 0, 0))) |         # pega os index dos pontos em que não ha mediçao analogica
             (df['TimeIniUTC'] > pd.Timestamp(2018, 1, 9, 11, 0, 0))].index.values
df.drop(indexes, inplace=True)                                                                                                               # remove do dataframe os index selecionados
df.reset_index(drop=True, inplace=True)

codes = []
for n in df['AlarmDesc']:                                           # adicionar uma coluna com os códigos dos alarmes no dataframe df
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

for i in df['Codes']:                                               # verifica linha por linha qual o código e cria uma lista com a reação e disponibilidade conforme o alarme / evento
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

df.insert(loc=6, column='Reacao', value=reac)                       # adicionar as coluna com as reações e disponibilidade no dataframe df
df.insert(loc=7, column='Disponibilidade', value=disponib)

mask = df['Codes'] == 0                                             # separar o dataframe df em dois: ec = estados e comandos, al = alarmes da listagem Gamesa
ec = df[mask]
ec.reset_index(drop=True, inplace=True)                             # reset no index
al = df[~mask]
al.reset_index(drop=True, inplace=True)

# -------------------------------------------------------------------------------------------------------------------- # Visão Geral sobre os dados al
t_reg_al = len(al)                                               # total ocorrências
t_tim_al = al.Delta.sum()                                        # total tempo de atuados
ocorr_aero = al.AlarmAero.value_counts()                         # quantidade de ocorrências por aero
ocorr_alarm = al.Codes.value_counts()                            # quantidade de ocorrências de cada alarme
t_aero = al.groupby('AlarmAero')['Delta'].sum()                  # tempo de registros atuados por aero
t_alarm = al.groupby('Codes')['Delta'].sum()                     # tempo de registros atuados por alarm

df_qt = pd.DataFrame()
oa = ocorr_alarm.reset_index()
qts = [0] * len(ocorr_alarm)
df_qt["Alarm"] = ocorr_alarm.index

for k in df["AlarmAero"].unique():
    for n, row in oa.iterrows():
        try:
            qts[n] = al.loc[(al["Codes"]==row["index"])]["AlarmAero"].value_counts()[k]
        except:
            qts[n] = 0
    df_qt[k] = qts

n       Z
df_copy['Total'] = df_copy[df_copy.columns[1:]].sum(axis=1)
df_copy.loc['Total'] = df_copy.sum()

alarmes_escolhidos = [315, 514, 516, 907, 908, 518, 2100, 823, 5204, 5216, 707, 426, 515]

al_copy = al[al['Codes'].isin(alarmes_escolhidos)]

plt.scatter(al_copy["TimeIniUTC"].values, list(map(str, al_copy["Codes"].values)), alpha=0.85, s=10)

print("cabou")

