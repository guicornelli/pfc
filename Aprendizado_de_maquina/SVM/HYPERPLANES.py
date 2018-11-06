import pymssql
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import timedelta
from time import time

# -------------------------------------------------------------------------------------------------------------------- # Configurar display de valores e resultados no console
np.set_printoptions(linewidth=500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

variables = ['GenNCSBearingTemp', 'GenSpeed', 'GridCurrent']          # variaveis analogicas a serem utilizadas

conn = pymssql.connect(host='GUILHERME', user='roquec', password='roquec', database='ISOTROL', as_dict=False,            # inicia conexao com BD ISOTROL
                       charset='UTF-8')
t0 = time()
# -------------------------------------------------------------------------------------------------------------------- # aero 20
cur = conn.cursor()
cur.execute("SELECT DISTINCT [TimeStampDateTimeUTC], "
            "[FieldValueConvert] "
            "FROM [ISOTROL].[dbo].[ActivePower_A01] "
            "ORDER BY [TimeStampDateTimeUTC]; ")

timestamp20 = []
val_genNCS20 = []

for row in cur:
    timestamp20.append(row[0])
    val_genNCS20.append(row[1])
cur.close()

timestamp20 = np.array(timestamp20)
val_genNCS20 = np.array(val_genNCS20)
amostra20 = len(timestamp20)
t1 = time()
t_consulta = round(t1-t0, 3)
# --------------------------------------------Duplicados e Congelados--------------------------------------------- #
errorsTS20 = []
errorsV120 = []
val_ncs20 = []
ts20 = []
t2 = time()
for k in range(amostra20 - 1):
    k = k + 1
    diffTS20 = timestamp20[k] - timestamp20[k - 1]
    diffV120 = val_genNCS20[k] - val_genNCS20[k - 1]
    if diffTS20 == timedelta(0):                                                    # duplicados
        if (timestamp20[k - 1].minute % 10 == 0) and (timestamp20[k - 1].second < 7):
            ts20.append(timestamp20[k])
            val_ncs20.append(val_genNCS20[k])
        else:
            errorsTS20.append(timestamp20[k])
            errorsV120.append(val_genNCS20[k])
    elif (timestamp20[k].minute % 10 == 0) and (timestamp20[k].second < 7):           # congelados
        if (timestamp20[k - 1].minute % 10 == 0) and (timestamp20[k - 1].second < 7) and (diffTS20.seconds < 500):
            ts20.append(timestamp20[k])
            val_ncs20.append(val_genNCS20[k])
        else:
            errorsTS20.append(timestamp20[k])
            errorsV120.append(val_genNCS20[k])
    else:                                                                         # amostra filtrada
        ts20.append(timestamp20[k])
        val_ncs20.append(val_genNCS20[k])

val_genNCS20 = np.array(val_ncs20)
timestamp20 = np.array(ts20)
t3 = time()
t_filtrag1 = round(t3-t2, 3)


# -------------------------------------------------------------------------------------------------------------------- #
def removeoutlier(values1, times):  # define a função com uma variavel de entrada
    fator = 3  # 1.5 é o fator de multiplicacao
    q75, q25 = np.percentile(values1, [75, 25])  # retorna o terceiro e primeiro quartil
    iqr = q75 - q25  # calcula o iqr(interquartile range)

    lowpass = q25 - (iqr * fator)  # calcula o valor minimo para aplicar no filtro
    highpass = q75 + (iqr * fator)  # calcula o valor maximo para aplicar no filtro

    outliers = np.argwhere(values1 < lowpass)  # descobre onde estao os valores menores que o valor minimo
    values1 = np.delete(values1, outliers)     # deleta esses valores
    times = np.delete(times, outliers)

    outliers = np.argwhere(values1 > highpass)  # descobre onde estao os valores maiores que o valor maximo
    values1 = np.delete(values1, outliers)  # deleta esses valores
    times = np.delete(times, outliers)

    return values1, times, q75, q25  # retorna a variavel sem outliers


val1SemOut20, tsSemOut20, q7520, q2520 = removeoutlier(val_genNCS20, timestamp20)
# -------------------------------------------------------------------------------------------------------------------- #
dados1 = {'Timestamp': timestamp20, 'semerros': val_genNCS20}
df_analogic1 = pd.DataFrame(data=dados1)
dados2 = {'Timestamp': errorsTS20, 'erros': errorsV120}
df_analogic2 = pd.DataFrame(data=dados2)
dados3 = {'Timestamp': tsSemOut20, 'semOut': val1SemOut20}
df_analogic3 = pd.DataFrame(data=dados3)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex='all', sharey='all', figsize=(19.2, 10.8), dpi=100)
df_analogic1.plot(x='Timestamp', y='semerros', style=".", ax=ax1)
df_analogic2.plot(x='Timestamp', y='erros', style=".", ax=ax2)
df_analogic3.plot(x='Timestamp', y='semOut', style=".", ax=ax3)


