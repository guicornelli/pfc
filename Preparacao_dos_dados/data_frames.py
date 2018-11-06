# -------------------------------------------Análise e retirada de Outliers------------------------------------------- #
import pymssql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
import time
from tipos import temperature, performance, eletric, oil, vibration, availability, status, setpoints

inicio = time.time()


def movingaverage(interval, window_size):
    window = np.ones(int(window_size)) / float(window_size)
    return np.convolve(interval, window, 'same')


parques = ['01', '20', '38', '58', '63', '88']
np.random.shuffle(parques)
comparacoes = 1

variaveisScada = [temperature, performance, eletric, oil, vibration, availability, status, setpoints]

conn = pymssql.connect(host='GUILHERME', user='roquec', password='roquec', database='ISOTROL', as_dict=False,
                       charset='UTF-8')

for k in parques[0:comparacoes]:
    print(k)
    consulta = ("SELECT [TimeStampDateTimeUTC] AS timestamp, [FieldValueConvert] AS value "
                "FROM [AmbientTemperature_A"+k+"]"
                "ORDER BY [TimeStampDateTimeUTC];")
    df = pd.read_sql(consulta, conn)
    df2 = df.copy()
    amostra = len(df)

    # --------------------------------------------Duplicados e Congelados--------------------------------------------- #
    indices_manter = []
    indices_descartar = []
    for i in range(amostra - 1):
        i = i + 1
        diffTS = df["timestamp"][i] - df["timestamp"][i-1]
        diffV = df["value"][i] - df["value"][i-1]
        if diffTS == timedelta(0):  # duplicados
            if (df["timestamp"][i-1].minute % 10 == 0) and (df["timestamp"][i-1].second < 7):
                indices_manter.append(i)
            else:
                indices_descartar.append(i)
        elif (df["timestamp"][i].minute % 10 == 0) and (df["timestamp"][i].second < 7):  # congelados
            if (df["timestamp"][i-1].minute % 10 == 0) and (df["timestamp"][i-1].second < 7) and (diffTS.seconds < 500):
                indices_manter.append(i)
            else:
                indices_descartar.append(i)
        else:  # amostra filtrada
            indices_manter.append(i)
    erros = len(indices_descartar)
    uteis = len(indices_manter)
    mediabruta = df["value"].mean()
    mediamovelbruta = movingaverage(df["value"], 1000).mean()

    df = df.take(list(indices_manter))
    df2 = df.take(list(indices_descartar))

    # ----------------------------------------------------Outliers---------------------------------------------------- #
    '''def get_median_filtered(signal, threshold=3):
        signal = signal.copy()
        difference = np.abs(signal - np.median(signal))
        median_difference = np.median(difference)
        if median_difference == 0:
            s = 0
        else:
            s = difference / float(median_difference)
        mask = s > threshold
        signal[mask] = np.median(signal)
        return signal


    def detect_outlier_position_by_fft(signal, threshold_freq=0.1,
                                       frequency_amplitude=.001):
        signal = signal.copy()
        fft_of_signal = np.fft.fft(signal)
        outlier = np.max(signal) if abs(np.max(signal)) > abs(np.min(signal)) else np.min(signal)
        if np.any(np.abs(fft_of_signal[threshold_freq:]) > frequency_amplitude):
            index_of_outlier = np.where(signal == outlier)
            return index_of_outlier[0]
        else:
            return None'''
    # ----------------------------------------------------Prints------------------------------------------------------ #

    print("Total de registros da amostra: %d" % amostra)
    print("Registros inválidos: %d, sendo %.2f%% da amostra" % (erros, (erros*100/amostra)))
    print("Resumo: amostra final filtrada possui %d pontos, sobrando %.2f%% da original" % ((amostra-erros),
                                                                                            (100-(erros*100/amostra))))
    print("Media da amostra bruta é %.2f" % (mediabruta))
    print("M_movel amostra bruta: %.2f" % (mediamovelbruta))

    # ---------------------------------------------------------------------------------------------------------------- #
    '''fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex='all', sharey='all', figsize=(19.2, 10.8), dpi=100)
    
    ax1.scatter(df["timestamp"], df["value"], c="k", alpha=0.5, marker='o')
    ax1.set_ylabel("Raw Data")
    ax1.grid(True)
    # y_av = movingaverage(value, 1000)
    # plt.plot(timestamp, y_av, "r")
    
    ax2.scatter(ts, val, c="b", alpha=0.5, marker='o')
    ax2.set_ylabel("Filtered Data")
    ax2.grid(True)

    ax3.scatter(df2["timestamp"], df2["value"], c="r", alpha=0.5, marker='o')
    ax3.set_ylabel("igual")
    ax3.grid(True)
    
    # ax4.scatter(timestamp[indicesduplicatas], value[indicesduplicatas], c="g", alpha=0.5, marker='o')
    # ax4.set_ylabel("Duplicates")
    # ax4.grid(True)
    
    plt.xlabel("Timestamp")


    plt.show()'''
    termino = time.time()
    print("tempo deu: ", (termino-inicio))
# -------------------------------------------------------------------------------------------------------------------- #
    boxp = plt.boxplot(val, showcaps=True, showbox=True, showfliers=True, showmeans=True)
    plt.show()

'''
    k = np.concatenate(k)
    timestamp = np.array(timestamp)
    #var = np.rec.fromarrays((value, timestamp), names=('value', 'ts'))

    deltas = []
    for i in range((len(value)-1)):
        i = i + 1
        if value[i] != value[i-1]:
            delta = abs(value[i] - value[i-1])
            deltas.append(delta)

    mindelta = min(deltas)
    maxdelta = max(deltas)

    #plt.scatter(var['ts'], var['value'], c="k", alpha=0.5)
    y_av = movingaverage(var['value'], 10)
    plt.plot(var['ts'], y_av, "r", marker='.')
    plt.xlabel("Timestamp")
    plt.ylabel("Value")
    plt.grid(True)
    plt.autoscale(enable=True, axis='both', tight=None)
    plt.show()
    plt.close('all')
plt.boxplot(k)
plt.show()
'''

# -------------------------------------------------------------------------------------------------------------------- #
conn.close()
# plt.savefig('C:/Users/g.souza/PycharmProjects/COAtlantic-17247/Perfis/Boxplots' + str(name) + '.png')
