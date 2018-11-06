import pymssql
import numpy as np
import matplotlib.pyplot as plt


def movingaverage(interval, window_size):
    window = np.ones(int(window_size)) / float(window_size)
    return np.convolve(interval, window, 'same')


def compar_variavel_aeros(consulta, conn, comparacoes):
    np.random.shuffle(parques)
    position = 1
    fig, (axes) = plt.subplots(comparacoes, 1, sharex='all', figsize=(19.2, 10.8), dpi=100)
    plt.suptitle("Comparation Values", weight='bold', verticalalignment='top', fontsize=14)

    for kk in parques[0:comparacoes]:
        print(kk)
        cur = conn.cursor()
        cur.execute(consulta)
        value = []
        timestamp = []

        for row in cur:
            value.append(row[1])
            timestamp.append(row[2])

        # plt.subplot(int(str(comparacoes)+"1"+str(position)))
        axes[position-1].scatter(timestamp, value, c="k", alpha=0.5)
        y_av = movingaverage(value, 1000)
        axes[position - 1].plot(timestamp, y_av, "r")
        axes[position - 1].set_ylabel("Aero "+kk+"")
        axes[position - 1].grid(True)
        position += 1
        deltavalue = []
        deltatime = []

        for i in range((len(value) - 1)):
            i = i + 1
            deltat = timestamp[i] - timestamp[i - 1]
            deltatime.append(deltat)
            if value[i] != value[i - 1]:
                deltav = abs(value[i] - value[i - 1])
                deltavalue.append(deltav)
        mindeltav = min(deltavalue)
        maxdeltav = max(deltavalue)
        mindeltat = min(deltatime)
        maxdeltat = max(deltatime)
        print("media movel %d e values %d" % (len(y_av), len(value)))
        print("max delta value %f e min delta value %f" % (maxdeltav, mindeltav))
        print("max delta time: %ddias %dhoras %dmins e min delta time: %dseg %dms" % (maxdeltat.days,
                                                                                      maxdeltat.seconds/3600,
                                                                                      maxdeltat.seconds/60,
                                                                                      mindeltat.seconds,
                                                                                      mindeltat.microseconds))
    plt.subplots_adjust(top=0.94, bottom=0.05, left=0.045, right=0.98, hspace=0.2)
    plt.xlabel("Timestamp")
    plt.show()


def consulta_individual(consulta, conn):
    cur = conn.cursor()
    cur.execute(consulta)
    value = []
    timestamp = []

    for row in cur:
        value.append(row[1])
        timestamp.append(row[2])

    cur.close()
    conn.close()
    value = np.array(value)
    timestamp = np.array(timestamp)
    print(len(value))
    plt.scatter(timestamp, value, c="k", alpha=0.5)
    y_av = movingaverage(value, 1000)
    plt.plot(timestamp, y_av, "r")
    plt.xlabel("Timestamp")
    plt.ylabel("Value")
    plt.grid(True)
    plt.show()

    return value, timestamp

def consulta_relacionada(consulta, conn):
    cur = conn.cursor()
    cur.execute(consulta)
    nacelledirect = []
    windspeed = []
    winddirect = []
    timestamp = []

    for row in cur:
        timestamp.append(row[0])
        nacelledirect.append(row[1])
        winddirect.append(row[2])
        windspeed.append(row[3])

    cur.close()
    conn.close()
    nacelledirect = np.array(nacelledirect)
    # windspeed = np.array(windspeed)
    # winddirect = np.array(winddirect)
    timestamp = np.array(timestamp)
    x = timestamp
    y1 = nacelledirect
    # y2 = windspeed
    # y3 = winddirect
    plt.scatter(x, y1, c="k", alpha=0.5)
    y_av = movingaverage(y1, 1000)
    plt.plot(x, y_av, "r")
    plt.xlabel("Timestamp")
    plt.ylabel("Value")
    plt.grid(True)
    plt.show()


parques = ['01', '20', '38', '58', '63', '88']
k = 0
sql_conn_isotrol = pymssql.connect(host='GUILHERME', user='roquec', password='roquec', database='ISOTROL', as_dict=False, charset='UTF-8')

sql_comp_variavel_aeros = ("SELECT * "
                           "FROM [TotalProduction_A"+str(k)+"] "
                           "ORDER BY [TimeStampDateTimeUTC]; ")

sql_consult_indiv = ("SELECT * "
                     "FROM [GenRingTemp_A63] "
                     "ORDER BY [TimeStampDateTimeUTC]; ")

sql_consult_relac = ("SELECT dbo.GenNCSBearingTemp_A20.FieldValueConvert, dbo.GenNCSBearingTemp_A20.TimeStampDateTimeUTC, "
                     "dbo.GenSpeed_A20.FieldValueConvert, dbo.GridCurrent_A20.FieldValueConvert "
                     "FROM dbo.GenNCSBearingTemp_A20 INNER JOIN "
                     "dbo.GenSpeed_A20 ON dbo.GenNCSBearingTemp_A20.TimeStampDateTimeUTC = dbo.GenSpeed_A20.TimeStampDateTimeUTC INNER JOIN "
                     "dbo.GridCurrent_A20 ON dbo.GenSpeed_A20.TimeStampDateTimeUTC = dbo.GridCurrent_A20.TimeStampDateTimeUTC "
                     "ORDER BY [TimeStampDateTimeUTC]; ")

# Curva gamesa Pot x Wind
gamesaP = [18, 87, 208, 383, 620, 938, 1348, 1743, 1937, 1988, 1998, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000,
           1906, 1681, 1455, 1230]
gamesaW = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

# compar_variavel_aeros(sql_comp_variavel_aeros, sql_conn_isotrol, 3)
# consulta_individual(sql_consult_indiv, sql_conn_isotrol)
# consulta_relacionada(sql_consult_relac, sql_conn_isotrol)
