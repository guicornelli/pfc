# -------------------------------------------Análise e retirada de Outliers------------------------------------------- #
import pymssql
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
from tipos import temperature, performance, eletric, oil, vibration, availability, status, setpoints


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
    cur = conn.cursor()
    cur.execute("SELECT [FieldValueConvert], [TimeStampDateTimeUTC] "
                "FROM [GenSpeed_A"+k+"]"
                "ORDER BY [TimeStampDateTimeUTC];")

    # ---------------------------------------------------------------------------------------------------------------- #
    value = []
    timestamp = []
    for row in cur:
        value.append(row[0])
        timestamp.append(row[1])
    cur.close()

    value = np.array(value)
    timestamp = np.array(timestamp)
    amostra = len(timestamp)

    # --------------------------------------------Duplicados e Congelados--------------------------------------------- #
    errorsTS = []
    errorsV = []
    val = []
    ts = []
    cDupVal = 0
    cDup = 0
    for i in range(amostra - 1):
        i = i + 1
        diffTS = timestamp[i] - timestamp[i-1]
        diffV = value[i] - value[i-1]
        if diffTS == timedelta(0):  # duplicados
            if (timestamp[i-1].minute % 10 == 0) and (timestamp[i-1].second < 7):
                ts.append(timestamp[i])
                val.append(value[i])
                cDupVal = cDupVal + 1
            else:
                errorsTS.append(timestamp[i])
                errorsV.append(value[i])
                cDup = cDup + 1
        elif (timestamp[i].minute % 10 == 0) and (timestamp[i].second < 7):  # congelados
            if (timestamp[i-1].minute % 10 == 0) and (timestamp[i-1].second < 7) and (diffTS.seconds < 500):
                ts.append(timestamp[i])
                val.append(value[i])
            else:
                errorsTS.append(timestamp[i])
                errorsV.append(value[i])
        else:  # amostra filtrada
            ts.append(timestamp[i])
            val.append(value[i])
    erros = len(errorsTS)
    uteis = len(ts)
    val = np.array(val)
    ts = np.array(ts)
    errorsTS = np.array(errorsTS)
    errorsV = np.array(errorsV)
    mediabruta = value.mean()
    mediafiltrada = val.mean()
    mediaerros = errorsV.mean()
    mediamovelbruta = movingaverage(value, 1000).mean()
    mediamovelfiltrada = movingaverage(val, 1000).mean()
    mediamovelerros = movingaverage(errorsV, 1000).mean()

    # ----------------------------------------------------Outliers---------------------------------------------------- #
    def removeoutlier(values, times):  # define a função com uma variavel de entrada
        fator = 3  # 1.5 é o fator de multiplicacao
        q75, q25 = np.percentile(values, [75, 25])  # retorna o terceiro e primeiro quartil
        iqr = q75 - q25  # calcula o iqr(interquartile range)

        lowpass = q25 - (iqr * fator)  # calcula o valor minimo para aplicar no filtro
        highpass = q75 + (iqr * fator)  # calcula o valor maximo para aplicar no filtro

        outliers = np.argwhere(values < lowpass)  # descobre onde estao os valores menores que o valor minimo
        values = np.delete(values, outliers)  # deleta esses valores
        times = np.delete(times, outliers)

        outliers = np.argwhere(values > highpass)  # descobre onde estao os valores maiores que o valor maximo
        values = np.delete(values, outliers)  # deleta esses valores
        times = np.delete(times, outliers)

        return values, times, q75, q25  # retorna a variavel sem outliers

    valSemOut, tsSemOut, q75, q25 = removeoutlier(val, ts)
    # ----------------------------------------------------Prints------------------------------------------------------ #
    print("Total de registros da amostra: %d" % amostra)
    print("Registros inválidos: %d, sendo %.2f%% da amostra" % (erros, (erros*100/amostra)))
    print("Resumo: amostra final filtrada possui %d pontos, sobrando %.2f%% da original" % ((amostra-erros),
                                                                                            (100-(erros*100/amostra))))
    print("Media da amostra bruta é %.2f, sendo a da amostra filtrada igual à %.2f e dos erros %.2f" % (mediabruta,
                                                                                                        mediafiltrada,
                                                                                                        mediaerros))
    print("M_movel amostra bruta: %.2f, amostra filtrada: %.2f, erros:  %.2f" % (mediamovelbruta,
                                                                                 mediamovelfiltrada,
                                                                                 mediamovelerros))
    print("Count duplic", cDup)
    print("Count duplic valid", cDupVal)

    print("tamanho a amostra sem outlier: ", len(valSemOut))
    print("quantidade de outliers encontrados: ", amostra-len(valSemOut))

    # ---------------------------------------------------------------------------------------------------------------- #
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex='all', sharey='all', figsize=(19.2, 10.8), dpi=100)

    ax1.scatter(timestamp, value, c="k", alpha=0.5, marker='o')
    ax1.set_ylabel("Raw Data")
    ax1.grid(True)
    # y_av = movingaverage(value, 1000)
    # plt.plot(timestamp, y_av, "r")

    ax2.scatter(ts, val, c="b", alpha=0.5, marker='o')
    ax2.set_ylabel("Filtered Data")
    ax2.grid(True)

    ax3.scatter(errorsTS, errorsV, c="r", alpha=0.5, marker='o')
    ax3.set_ylabel("Errors")
    ax3.grid(True)

    ax4.scatter(tsSemOut, valSemOut, c="g", alpha=0.5, marker='o')
    ax4.set_ylabel("Sem Outliers")
    ax4.grid(True)

    plt.xlabel("Timestamp")
    plt.show()

# -------------------------------------------------------------------------------------------------------------------- #
    boxp = plt.boxplot(val, showcaps=True, showbox=True, showfliers=True, showmeans=True)
    plt.show()

# -------------------------------------------------------------------------------------------------------------------- #
conn.close()
