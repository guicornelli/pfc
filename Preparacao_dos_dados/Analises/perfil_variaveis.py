# ----------------------- Perfil das variáveis contidas no Banco de Dados ISOTROL - MSQLServer ----------------------- #

# ---------------------------------------------------- Imports ------------------------------------------------------- #
from infos_variaveis import perfil
from infos_variaveis_copia import caracteristicas
from sklearn.preprocessing import MinMaxScaler
import pymssql
import time
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------ Main -------------------------------------------------------- #
conn = pymssql.connect(host='GUILHERME', user='roquec', password='roquec', database='GAMESA', as_dict=False,
                       charset='UTF-8')
cur1 = conn.cursor()
cur1.execute("SELECT name FROM sys.tables;")
tables = np.delete(np.sort(np.array(cur1.fetchall()).ravel()), [1, 35, 43, 69])  # Delete unnecessary tables,
cur1.close()                                                                     # (sequential delete)

# Functions


def movingaverage(interval, window_size):
    window = np.ones(int(window_size)) / float(window_size)
    return np.convolve(interval, window, 'same')


def featurescaling(arr):
    scaler = MinMaxScaler(feature_range=(0.2, 0.5))  # Color opacity range
    rescaled_arr = scaler.fit_transform(arr)
    return rescaled_arr


def pol2cart(r, theta):
    x = r * np.cos(np.deg2rad(theta))
    y = r * np.sin(np.deg2rad(theta))
    return x, y


colorsfig = [plt.cm.Blues, plt.cm.Reds, plt.cm.Greens, plt.cm.Purples, plt.cm.Greys, plt.cm.Oranges, plt.cm.pink]

# Radar chart
categories = ['     Max $x10^3$', 'Avg\n'
                                  '$x10^3$', '   Avg$_{mov}$\n'
                                             '   $x10^3$', 'Min $x10^3$     ', 'N$_{Points}$      \n'
                                                                               '$x10^6$       ', 'T$_{Calc}$\n'
                                                                                                 'Min']
N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]  # Add first angle for close graph

# Table plot
columns = ['Com Outliers', 'Sem Outliers']
rows = ['$Max$', '$Min$', '$Avg$', '$Avg_{mov}$', '$N_{Points}$', '$T_{Calc(m)}$']

# Classification Chart
labels_gender = ['AmbientTemperature', 'ControlModuleTemp', 'ConvAirTemp', 'CoolerTemp', 'FG8AirTemp',
                 'GearboxBearingTemp', 'GearboxOilTemp', 'GenCSBearingTemp', 'GenRingTemp', 'GenWinding1Temp',
                 'GenWinding2Temp', 'GenWinding3Temp', 'GridIndTemp', 'GridRectTemp', 'HydrOilTemp',
                 'NacelleTemp', 'Radiator1Temp', 'Radiator2Temp', 'RotorInvTemp', 'TrafoWinding1Temp',
                 'TrafoWinding2Temp', 'TrafoWinding3Temp',

                 'ActivePower', 'ActivePowerSetpoint', 'AuxReactivePower', 'GenActivePower', 'GenSpeed', 'GenSpeedOGS',
                 'GenSpeedTop', 'NacelleOrientation', 'PitchAngle', 'PLimitAvilableStator', 'ProduciblePower',
                 'ProducibleQCap', 'ProducibleQInd', 'ReactivePower', 'RectActivePower', 'RotorSpeed',
                 'StatorActivePower', 'StatorReactivePower', 'TotalProduction', 'WindDirectionRelNac', 'WindSpeed',
                 'WindSpeedNotF',

                 'BusVoltage', 'GridCurrent', 'GridFrec', 'GRidFrecPLC', 'GridVoltage', 'RectCurrent', 'RotorCurrent',
                 'ServoVoltage', 'StatorCurrent', 'TowerFrecuency',

                 'GearboxOilParticleFlow', 'GearboxShaftBearingGrease', 'GreaseGenBearingTank', 'HydrPress',
                 'YawBrakePress',

                 'NoiseLevel', 'NoiseLevelCommLost', 'NoiseLeverLowWind',

                 'GridHAvailability', 'HAvailability', 'HService', 'TurbHAvailability',

                 'StatusWT', 'StoopedByTool']
sizes_gender = np.array([(caracteristicas.get(i + "_A01").get('tamanho')) for i in labels_gender])
labels_sizes = np.rec.fromarrays((labels_gender, sizes_gender), names=('name', 'lenght'))
temp = labels_sizes[0:22]
perf = labels_sizes[22:44]
eel = labels_sizes[44:54]
oil = labels_sizes[54:59]
vib = labels_sizes[59:62]
avail = labels_sizes[62:66]
stat = labels_sizes[66:]
sizes = np.array([sum(temp['lenght']), sum(perf['lenght']), sum(eel['lenght']), sum(oil['lenght']), sum(vib['lenght']),
                  sum(avail['lenght']), sum(stat['lenght'])])
labels = ["Temperature - %.2f%%" % (round((sum(temp['lenght']) / sum(labels_sizes['lenght'])) * 100, 3)),
          "Performance - %.2f%%" % (round((sum(perf['lenght']) / sum(labels_sizes['lenght'])) * 100, 3)),
          "Eletric - %.2f%%" % (round((sum(eel['lenght']) / sum(labels_sizes['lenght'])) * 100, 3)),
          "Oil - %.2f%%" % (round((sum(oil['lenght']) / sum(labels_sizes['lenght'])) * 100, 3)),
          "Vibration - %.2f%%" % (round((sum(vib['lenght']) / sum(labels_sizes['lenght'])) * 100, 3)),
          "Availability - %.2f%%" % (round((sum(avail['lenght']) / sum(labels_sizes['lenght'])) * 100, 3)),
          "Status - %.2f%%" % (round((sum(stat['lenght']) / sum(labels_sizes['lenght'])) * 100, 3))]
expl_gender_value = 0.05  # Parameter explode all variables of pie plot of type selected variable
sizes_gender_parts = np.array([temp, perf, eel, oil, vib, avail, stat])
colors_gender = []
sizes_sorted = []
for ii in sizes_gender_parts:
    scale = featurescaling(np.sort(ii['lenght']).reshape(-1, 1)).reshape(1, -1).ravel()
    if np.array_equal(ii, temp):
        [colors_gender.append(colorsfig[0](jj)) for jj in scale]
    elif np.array_equal(ii, perf):
        [colors_gender.append(colorsfig[1](jj)) for jj in scale]
    elif np.array_equal(ii, eel):
        [colors_gender.append(colorsfig[2](jj)) for jj in scale]
    elif np.array_equal(ii, oil):
        [colors_gender.append(colorsfig[3](jj)) for jj in scale]
    elif np.array_equal(ii, vib):
        [colors_gender.append(colorsfig[4](jj)) for jj in scale]
    elif np.array_equal(ii, avail):
        [colors_gender.append(colorsfig[5](jj)) for jj in scale]
    else:
        [colors_gender.append(colorsfig[6](jj)) for jj in scale]
    [sizes_sorted.append(value) for value in np.sort(ii, order='lenght')]
sizes_sorted = np.array(sizes_sorted)

# ------------------------------------------------------ Loop -------------------------------------------------------- #
for k in tables:
    # Config Figure of Plot
    plt.rcParams['figure.facecolor'] = colorsfig[4](0.1)  # Background color
    plt.figure(figsize=(19.2, 10.8), dpi=200)
    plt.suptitle("Variables Profile", weight='bold', verticalalignment='top', fontsize=14)

    tini = time.time()
    if k not in perfil.keys():
        print(k)
        cur2 = conn.cursor()
        cur2.execute("SELECT * "
                     "FROM ["+k+"]"
                     "ORDER BY TimeStampConvert;")
        value = []
        timestamp = []
        for row in cur2:
            value.append(row[1])
            timestamp.append(row[3])
        cur2.close()
        value = np.array(value)
        timestamp = np.array(timestamp)
        name = row[0]+"_A01"

        # --------------------------------------------- Variables Calc ----------------------------------------------- #
        mov_avg_points = 1000
        y_av = movingaverage(value, mov_avg_points)
        maximo = value.max()
        minimo = value.min()
        media = value.mean()
        mediamovel = y_av.mean()
        totalpontos = len(value)
        primeiradata = timestamp[0]
        ultimadata = timestamp[-1]
        tempomedicao = (ultimadata - primeiradata)
        tempototal = "%d dias e %d horas" % (tempomedicao.days, (round(tempomedicao.seconds/3600)))
        tfim = time.time()
        texec = (tfim - tini)

        pos = np.where(sizes_sorted['name'] == row[0])[0][0]
        explode = np.zeros(len(labels))
        explode_gender = np.zeros(len(labels_gender))
        if pos < 22:
            ind = 0
            explode_gender[0:22] = expl_gender_value
        elif 22 <= pos < 44:
            ind = 1
            explode_gender[22:44] = 0
        elif 44 <= pos < 54:
            ind = 2
            explode_gender[44:54] = expl_gender_value
        elif 54 <= pos < 61:
            ind = 3
            explode_gender[54:61] = expl_gender_value
        elif 61 <= pos < 64:
            ind = 4
            explode_gender[61:64] = expl_gender_value
        elif 64 <= pos < 68:
            ind = 5
            explode_gender[64:68] = expl_gender_value
        else:
            ind = 6
            explode_gender[68:] = expl_gender_value

        # --------------------------------------- Moving Avg and Scatter Plot --------------------------------------- #
        plt.subplot(211)
        plt.scatter(timestamp, value, c="k", alpha=0.4, label="Raw Data")
        plt.plot(timestamp, y_av, "r", label="Mov Avg ("+str(mov_avg_points)+" $points$)")
        plt.title(""+name+" - Raw Data and Moving Avg with our without Outliers", weight='bold', fontsize=12)
        plt.xlabel("$Timestamp$")
        plt.ylabel("$Values$")
        plt.grid(True)
        plt.legend()
        plt.tight_layout(pad=0.4, w_pad=0.6, h_pad=5.0)
        # ------------------------------------------------- Outliers ------------------------------------------------- #



        # --------------------------------------------- Radar Chart Plot --------------------------------------------- #
        values = [(maximo/1000.0), abs(media/1000.0), abs(mediamovel/1000.0), abs(minimo/1000.0), (totalpontos/1000000),
                  (texec/60), (maximo/1000.0)]
        ax1 = plt.subplot(234, polar=True)
        plt.xticks(angles[:-1], categories, color='grey', size=9)
        ax1.set_rlabel_position(0)
        ax1.set_theta_offset(np.pi / 2)
        ax1.set_theta_direction(-1)
        plt.title('Radar Profile', weight='bold', fontsize=10)
        plt.yticks([1, 2, 3, 4, 5, 6], ["1", "2", "3", "4", "5", "6"], color="grey", size=9)
        plt.ylim(0, 6)
        plt.plot(angles, values, linewidth=1, linestyle='solid')
        plt.fill(angles, values, 'b', alpha=0.1)

        # --------------------------------------------- Values Table Plot -------------------------------------------- #
        valTab = [[round(maximo, 3), round(maximo, 3)],
                  [round(minimo, 3), round(minimo, 3)],
                  [round(media, 3), round(media, 3)],
                  [round(mediamovel, 3), round(mediamovel, 3)],
                  [totalpontos, totalpontos],
                  [round((texec / 60.0), 3), round((texec / 60.0), 3)]]
        plt.subplot(235)
        plt.title('  Values With x Without Outliers', weight='bold', fontsize=10)
        tabela = plt.table(cellText=valTab, rowLabels=rows, colLabels=columns, cellLoc='center', loc='center',
                           bbox=[0.05, 0, 0.9, 1])  # [left, bottom, width, height]
        plt.axis('off')

        # -------------------------------------------- Classify Pie Plot --------------------------------------------- #
        if ind != 1:
            explode[ind] = 0.1
        explode_gender[pos] = 0.2
        plt.subplot(236)
        plt.title('Type Classification', weight='bold', fontsize=10)
        plt.axis('equal')
        mypie, textos = plt.pie(sizes, radius=1.2, explode=explode, colors=[colorsfig[0](0.6), colorsfig[1](0.6),
                                                                            colorsfig[2](0.6), colorsfig[3](0.6),
                                                                            colorsfig[4](0.6), colorsfig[5](0.6),
                                                                            colorsfig[6](0.6)])
        plt.setp(mypie, width=0.2, edgecolor='white')
        mypie2, __ = plt.pie(sizes_sorted['lenght'], radius=1.3 - 0.3, explode=explode_gender, colors=colors_gender)
        plt.setp(mypie2, width=0.4)
        plt.margins(0, 0)
        meio = ((mypie2[pos].theta1 + mypie2[pos].theta2) / 2.0)
        xis, yps = pol2cart((mypie2[pos].r + mypie2[pos].center[0]), meio)
        plt.annotate(row[0], xy=(xis, yps), xytext=(xis + 0.2, yps + 0.3), fontsize=8, weight='bold',
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))
        plt.legend(labels, loc="best", prop={'size': 9})

        # --------------------------------------- Show, Save and Config Plots ---------------------------------------- #
        # plt.tight_layout()
        plt.subplots_adjust(top=0.92, bottom=0.025, left=0.045, right=0.98, hspace=0.2)
        # plt.show()
        plt.savefig('C:/Users/guilh/PycharmProjects/17274-COAtlantic/Preparacao_dos_dados/Analises/Perfis' + str(name) + '.png')
        plt.close('all')
        with open('C:/Users/guilh/PycharmProjects/17274-COAtlantic/Preparacao_dos_dados/Analises/infos_variaveis.py', 'a') as arq:
            novosvalores = "perfil[" + "\"" + name + "\"" + "]={'max':"+" "+str(maximo)+", 'min':"+" "+str(minimo)+"," \
                           " 'media':"+" "+str(media)+", 'mediamovel':"+" "+str(mediamovel)+"," \
                           " 'tamanho':"+" "+str(totalpontos)+", 't(s)exec':"+" "+str(texec)+"," \
                           " 'primeiroponto':" + " \'" + str(primeiradata) + "\'" + "," \
                           " 'ultimoponto':" + " \'" + str(ultimadata) + "\'" + "," \
                           " 'tempo de medicao':" + " \'" + str(tempototal) + "\'" + "}\n"
            arq.write(novosvalores)

conn.close()

# ---------------------------------------------------- End Loop ------------------------------------------------------ #
