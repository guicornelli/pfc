"""
    Consulta a banco de dados com as variáveis analógicas.

    Evitou-se usar a biblioteca Pandas neste código por razões de
        apresentarem desempenho muito mais lento do que listas e Numpy.

    Retorna arrays com as variáveis consultadas filtradas.
"""

"""puxar os dados brutos, filtrar, jogar de volta no banco
filtrar = retirar pontos repetidos, erros, copias, outliers, variaveis vazias"""

import pymssql
import numpy as np
import pandas as pd
from time import time
from datetime import timedelta
import matplotlib.pyplot as plt

# Configurações de visualização dos dataframes no PyCharm
np.set_printoptions(linewidth=500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

variaveis = ['ActivePower', 'ActivePowerSetpoint', 'AmbientTemperature', 'AuxReactivePower', 'BusVoltage',
             'CapacityFactor', 'ControlModuleTemp', 'ConvAirTemp', 'CoolerTemp', 'CosPhi', 'DeltaControlSP',
             'FG8AirTemp', 'GearboxBearingTemp', 'GearboxOilParticleFlow', 'GearboxOilTemp',
             'GearboxShaftBearingGrease', 'GenActivePower', 'GenCSBearingTemp', 'GenNCSBearingTemp', 'GenRingTemp',
             'GenSpeed', 'GenSpeedOGS', 'GenSpeedTop', 'GenWinding1Temp', 'GenWinding2Temp', 'GenWinding3Temp',
             'GreaseGenBearingTank', 'GridCurrent', 'GridFrec', 'GridFrecPLC', 'GridHAvailability', 'GridIndTemp',
             'GridRectTemp', 'GridVoltage', 'HAvailability', 'HPauseIceTotal', 'HService', 'HydrOilTemp', 'HydrPress',
             'IceDetTemp', 'NacelleOrientation', 'NacelleTemp', 'NoiseLevel', 'NoiseLevelCommLost', 'NoiseLeverLowWind',
             'PitchAngle', 'PLimitAvailableStator', 'ProduciblePower', 'ProducibleQCap', 'ProducibleQInd',
             'Radiator1Temp', 'Radiator2Temp', 'ReactivePower', 'RectActivePower', 'RectCurrent', 'RotorCurrent',
             'RotorInvTemp', 'RotorSpeed', 'ServoVoltage', 'SPCosPhi', 'SPGenSpeed', 'SPPitchAngle', 'SPStatorP',
             'SPStatorQ', 'StatorActivePower', 'StatorCurrent', 'StatorReactivePower', 'StatusWT', 'StoopedByTool',
             'TotalProduction', 'TowerFrecuency', 'TrafoWinding1Temp', 'TrafoWinding2Temp', 'TrafoWinding3Temp',
             'TurbHAvailability', 'WindDirection', 'WindDirectionRelNac', 'WindSpeed', 'WindSpeedNotF', 'YawBrakePress']

var_retiradas = ['DeltaControlSP', 'GearboxOilParticleFlow', 'GearboxShaftBearingGrease', 'GenSpeedOGS', 'GreaseGenBearingTank', 'HPauseIceTotal',
                 'NoiseLeverLowWind', 'ProducibleQCap', 'ProducibleQInd']

var_retiradas2 = ['IceDetTemp', 'NoiseLevel', 'NoiseLevelCommLost', 'ActivePower', 'ActivePowerSetpoint', 'TowerFrecuency', 'GenSpeed',
                  'GridHAvailability', 'HAvailability', 'HService', 'TurbHAvailability', 'GenWinding2Temp', 'GenWinding3Temp',
                  'SPCosPhi', 'SPGenSpeed', 'SPPitchAngle', 'SPStatorP', 'SPStatorQ', 'StatorActivePower', 'GridCurrent',
                  'RotorSpeed', 'ReactivePower', 'StatusWT', 'WindSpeedNotF', 'ConvAirTemp', 'Radiator2Temp', 'CapacityFactor',
                  'ProduciblePower', 'StoopedByTool', 'RotorCurrent', 'AmbientTemperature']

variaveis_atuais = []

for v in variaveis:
    if v not in var_retiradas or var_retiradas2:
        variaveis_atuais.append(v)

t0 = time()
# Conexão com BD SQL Server
sql_conn_isotrol = pymssql.connect(host='GUILHERME', user='roquec', password='roquec', database='ISOTROL', as_dict=False, charset='UTF-8')

t0 = time()
cur = sql_conn_isotrol.cursor()
cur.execute("SELECT DISTINCT [TimeStampDateTimeUTC], "
            "[FieldValueConvert] "
            "FROM [ISOTROL].[dbo].[ActivePower_A01] "
            "ORDER BY [TimeStampDateTimeUTC]; ")

timestamp = []
value = []

for row in cur:
    timestamp.append(row[0])
    value.append(row[1])
cur.close()

timestamp = np.array(timestamp)
value = np.array(value)
amostra = len(timestamp)

t1 = time()
t_consulta = round(t1-t0, 3)


"""cur1 = sql_conn_isotrol.cursor()
cur1.execute("SELECT name FROM sys.tables;")
tables = cur1.fetchall()
cur1.close()"""

sql_analogicas = ("SELECT DISTINCT [TimeStampDateTimeUTC], "
                  "[FieldValueConvert] "
                  "FROM [ISOTROL].[dbo].[ActivePower_A01] "
                  "ORDER BY [TimeStampDateTimeUTC]; ")

dataframe = pd.read_sql(sql_analogicas, sql_conn_isotrol)
t1 = time()
t_consulta = round(t1-t0, 3)

df = pd.concat([dataframe.shift(1), dataframe], axis=1)
df.columns = ['TimeStampDateTimeUTC_SHIFTED', 'FieldValueConvert_SHIFTED', 'TimeStampDateTimeUTC', 'FieldValueConvert']

indexes_rej = []
t2 = time()
for i, row in df.iterrows():
    if (row['TimeStampDateTimeUTC'].minute % 10 == 0) and (row['TimeStampDateTimeUTC'].second < 7):
        if (row['TimeStampDateTimeUTC_SHIFTED'].minute % 10 == 0) and (row['TimeStampDateTimeUTC_SHIFTED'].second < 7) and \
                ((row['TimeStampDateTimeUTC'] - row['TimeStampDateTimeUTC_SHIFTED']).seconds < 500):
            indexes_rej.append(i)
t3 = time()
t_filtragem1 = round(t3-t2, 3)

df2 = pd.concat([dataframe.shift(2), dataframe.shift(1), dataframe], axis=1)
df2.columns = ['TimeStampDateTimeUTC_SHIFTEDx2', 'FieldValueConvert_SHIFTEDx2', 'TimeStampDateTimeUTC_SHIFTEDx1', 'FieldValueConvert_SHIFTEDx1', 'TimeStampDateTimeUTC', 'FieldValueConvert']

indexes_rej2 = []
t4 = time()
for j, row2 in df2.iterrows():
    if (row2['TimeStampDateTimeUTC'].minute % 10 == 0) and (row2['TimeStampDateTimeUTC'].second == 0):
        if (row2['FieldValueConvert'] == row2['FieldValueConvert_SHIFTEDx1']) or (row2['FieldValueConvert'] == row2['FieldValueConvert_SHIFTEDx2']):
            indexes_rej2.append(j)
t5 = time()
t_filtragem2 = round(t5-t4, 3)


def filtrar(item):
    try:
        asd = pd.where(item['TimeStampDateTimeUTC'].dt.minute % 10 == 0)
    except:
        print("erro")

    return asd

ddd = df.apply(filtrar, axis=1, result_type='expand')


#semnan = Out[22].dropna(axis=0, how='all')

"""
for i, row in df.iterrows():                                                                     # i: dataframe index; row: each row in series format
    soup = get_soup(row)                                                                         # le o arquivo html da linha
    words = re.findall('\w+', soup.getText().lower())                                            # encontra todas as palavras separadamente, do arquivo
    no_integers = [x for x in words if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())]     # retira os numeros inteiros
    no_stopwords = [x for x in no_integers if len(x) > 1 and x not in sw]                        # retira os stopwords
    words_stemmer[i] = [stemmer.stem(i) for i in no_stopwords]                                   # realiza a compactacao de cada palavra
    count_stemmer = collections.Counter(words_stemmer[i]).most_common()                          # retorna lista com contagem de cada palavra apos reduzida, do arquivo html
    unique_words_stemmer[i] = len(count_stemmer)

df.drop(indexes, inplace=True)                                                                                                               # remove do dataframe os index selecionados
df.reset_index(drop=True, inplace=True)

for i, row in df.iterrows():
    i = i + 1
    diffTS = row['TimeStampDateTimeUTC'][i] - row['TimeStampDateTimeUTC'][i - 1]
    if (row['TimeStampDateTimeUTC'][i].minute % 10 == 0) and (row['TimeStampDateTimeUTC'][i].second < 7):
        if (row['TimeStampDateTimeUTC'][i - 1].minute % 10 == 0) and (row['TimeStampDateTimeUTC'][i - 1].second < 7) and (diffTS.seconds < 500):
            indexes_rej.append(i)


for i in range(len(df.index) - 1):
    i = i + 1
    diffTS = df['TimeStampDateTimeUTC'][i] - df['TimeStampDateTimeUTC'][i - 1]
    if (df['TimeStampDateTimeUTC'][i].minute % 10 == 0) and (df['TimeStampDateTimeUTC'][i].second < 7):
        if (df['TimeStampDateTimeUTC'][i - 1].minute % 10 == 0) and (df['TimeStampDateTimeUTC'][i - 1].second < 7) and (diffTS.seconds < 500):
            indexes_rej.append(i)

plt.scatter(df.index, df['FieldValueConvert'], marker='.', alpha=0.4)

fig, (ax1, ax2) = plt.subplots(2, 1, sharex='all', sharey='all', figsize=(19.2, 10.8), dpi=100)

ax1.scatter(df['TimeStampDateTimeUTC'], df['FieldValueConvert'], c="k", alpha=0.5, marker='.')
ax1.set_ylabel("Raw Data")
ax1.grid(True)

ax2.scatter(ts, val, c="b", alpha=0.5, marker='.')
ax2.set_ylabel("Filtered Data")
ax2.grid(True)

plt.xlabel("Timestamp")


sql_conn_isotrol.close()


print("pera")


def prep_analogicas_listas(consulta1, consulta2, conn):


df.index = pd.DatetimeIndex(df.Timestamp)
df['GenNCSBearingTemp'].resample('1Min').mean()

novo = pd.DataFrame()
novo['GenNCSBearingTemp'] = df.GenNCSBearingTemp.resample('1Min').mean()


    # --------------------------------------------Duplicados e Congelados--------------------------------------------- #
    errorsTS20 = []
    errorsV120 = []
    errorsV220 = []
    errorsV320 = []
    errorsV420 = []
    errorsV520 = []
    val_ncs20 = []
    val_s20 = []
    val_cur20 = []
    val_g20 = []
    val_r20 = []
    ts20 = []

    for k in range(amostra20 - 1):
        k = k + 1
        diffTS20 = timestamp20[k] - timestamp20[k - 1]
        diffV120 = val_genNCS20[k] - val_genNCS20[k - 1]
        diffV220 = val_genS20[k] - val_genS20[k - 1]
        diffV320 = val_curGrid20[k] - val_curGrid20[k - 1]
        diffV420 = val_genAc20[k] - val_genAc20[k - 1]
        diffV520 = val_rotS20[k] - val_rotS20[k - 1]
        if diffTS20 == timedelta(0):                                                    # duplicados
            if (timestamp20[k - 1].minute % 10 == 0) and (timestamp20[k - 1].second < 7):
                ts20.append(timestamp20[k])
                val_ncs20.append(val_genNCS20[k])
                val_s20.append(val_genS20[k])
                val_cur20.append(val_curGrid20[k])
                val_g20.append(val_genAc20[k])
                val_r20.append(val_rotS20[k])
            else:
                errorsTS20.append(timestamp20[k])
                errorsV120.append(val_genNCS20[k])
                errorsV220.append(val_genS20[k])
                errorsV320.append(val_curGrid20[k])
                errorsV420.append(val_genAc20[k])
                errorsV520.append(val_rotS20[k])
        elif (timestamp20[k].minute % 10 == 0) and (timestamp20[k].second < 7):           # congelados
            if (timestamp20[k - 1].minute % 10 == 0) and (timestamp20[k - 1].second < 7) and (diffTS20.seconds < 500):
                ts20.append(timestamp20[k])
                val_ncs20.append(val_genNCS20[k])
                val_s20.append(val_genS20[k])
                val_cur20.append(val_curGrid20[k])
                val_g20.append(val_genAc20[k])
                val_r20.append(val_rotS20[k])
            else:
                errorsTS20.append(timestamp20[k])
                errorsV120.append(val_genNCS20[k])
                errorsV220.append(val_genS20[k])
                errorsV320.append(val_curGrid20[k])
                errorsV420.append(val_genAc20[k])
                errorsV520.append(val_rotS20[k])
        else:                                                                         # amostra filtrada
            ts20.append(timestamp20[k])
            val_ncs20.append(val_genNCS20[k])
            val_s20.append(val_genS20[k])
            val_cur20.append(val_curGrid20[k])
            val_g20.append(val_genAc20[k])
            val_r20.append(val_rotS20[k])

    val_genNCS20 = np.array(val_ncs20)
    val_genS20 = np.array(val_s20)
    val_curGrid20 = np.array(val_cur20)
    val_genAc20 = np.array(val_g20)
    val_rotS20 = np.array(val_r20)
    timestamp20 = np.array(ts20)

    # -------------------------------------------------------------------------------------------------------------------- # aero 58
    cur = conn.cursor()
    cur.execute(consulta2)

    timestamp58 = []
    val_genNCS58 = []
    val_genS58 = []
    val_curGrid58 = []
    val_genAc58 = []
    val_rotS58 = []

    for row in cur:
        timestamp58.append(row[0])
        val_genNCS58.append(row[1])
        val_genS58.append(row[2])
        val_curGrid58.append(row[3])
        val_genAc58.append(row[4])
        val_rotS58.append(row[5])

    cur.close()
    timestamp58 = np.array(timestamp58)
    val_genNCS58 = np.array(val_genNCS58)
    val_genS58 = np.array(val_genS58)
    val_curGrid58 = np.array(val_curGrid58)
    val_genAc58 = np.array(val_genAc58)
    val_rotS58 = np.array(val_rotS58)
    amostra58 = len(timestamp58)
    # --------------------------------------------Duplicados e Congelados--------------------------------------------- #
    errorsTS58 = []
    errorsV158 = []
    errorsV258 = []
    errorsV358 = []
    errorsV458 = []
    errorsV558 = []
    val_ncs58 = []
    val_s58 = []
    val_cur58 = []
    val_g58 = []
    val_r58 = []
    ts58 = []

    for k in range(amostra58 - 1):
        k = k + 1
        diffTS58 = timestamp58[k] - timestamp58[k - 1]
        diffV158 = val_genNCS58[k] - val_genNCS58[k - 1]
        diffV258 = val_genS58[k] - val_genS58[k - 1]
        diffV358 = val_curGrid58[k] - val_curGrid58[k - 1]
        diffV458 = val_genAc58[k] - val_genAc58[k - 1]
        diffV558 = val_rotS58[k] - val_rotS58[k - 1]
        if diffTS58 == timedelta(0):                                                    # duplicados
            if (timestamp58[k - 1].minute % 10 == 0) and (timestamp58[k - 1].second < 7):
                ts58.append(timestamp58[k])
                val_ncs58.append(val_genNCS58[k])
                val_s58.append(val_genS58[k])
                val_cur58.append(val_curGrid58[k])
                val_g58.append(val_genAc58[k])
                val_r58.append(val_rotS58[k])
            else:
                errorsTS58.append(timestamp58[k])
                errorsV158.append(val_genNCS58[k])
                errorsV258.append(val_genS58[k])
                errorsV358.append(val_curGrid58[k])
                errorsV458.append(val_genAc58[k])
                errorsV558.append(val_rotS58[k])
        elif (timestamp58[k].minute % 10 == 0) and (timestamp58[k].second < 7):           # congelados
            if (timestamp58[k - 1].minute % 10 == 0) and (timestamp58[k - 1].second < 7) and (diffTS58.seconds < 500):
                ts58.append(timestamp58[k])
                val_ncs58.append(val_genNCS58[k])
                val_s58.append(val_genS58[k])
                val_cur58.append(val_curGrid58[k])
                val_g58.append(val_genAc58[k])
                val_r58.append(val_rotS58[k])
            else:
                errorsTS58.append(timestamp58[k])
                errorsV158.append(val_genNCS58[k])
                errorsV258.append(val_genS58[k])
                errorsV358.append(val_curGrid58[k])
                errorsV458.append(val_genAc58[k])
                errorsV558.append(val_rotS58[k])
        else:                                                                         # amostra filtrada
            ts58.append(timestamp58[k])
            val_ncs58.append(val_genNCS58[k])
            val_s58.append(val_genS58[k])
            val_cur58.append(val_curGrid58[k])
            val_g58.append(val_genAc58[k])
            val_r58.append(val_rotS58[k])

    val_genNCS58 = np.array(val_ncs58)
    val_genS58 = np.array(val_s58)
    val_curGrid58 = np.array(val_cur58)
    val_genAc58 = np.array(val_g58)
    val_rotS58 = np.array(val_r58)
    timestamp58 = np.array(ts58)

    conn.close()                                                                       # fecha porta de comunicação com o BD

    # -------------------------------------------------------------------------------------------------------------------- #


    def removeoutlier(values1, values2, values3, values4, values5, times):  # define a função com uma variavel de entrada
        fator = 3  # 1.5 é o fator de multiplicacao
        q75, q25 = np.percentile(values1, [75, 25])  # retorna o terceiro e primeiro quartil
        iqr = q75 - q25  # calcula o iqr(interquartile range)

        lowpass = q25 - (iqr * fator)  # calcula o valor minimo para aplicar no filtro
        highpass = q75 + (iqr * fator)  # calcula o valor maximo para aplicar no filtro

        outliers = np.argwhere(values1 < lowpass)  # descobre onde estao os valores menores que o valor minimo
        values1 = np.delete(values1, outliers)     # deleta esses valores
        values2 = np.delete(values2, outliers)
        values3 = np.delete(values3, outliers)
        values4 = np.delete(values4, outliers)
        values5 = np.delete(values5, outliers)
        times = np.delete(times, outliers)

        outliers = np.argwhere(values1 > highpass)  # descobre onde estao os valores maiores que o valor maximo
        values1 = np.delete(values1, outliers)  # deleta esses valores
        values2 = np.delete(values2, outliers)
        values3 = np.delete(values3, outliers)
        values4 = np.delete(values4, outliers)
        values5 = np.delete(values5, outliers)
        times = np.delete(times, outliers)

        return values1, values2, values3, values4, values5, times, q75, q25  # retorna a variavel sem outliers


    val1SemOut20, val2SemOut20, val3SemOut20, val4SemOut20, val5SemOut20, tsSemOut20, q7520, q2520 = removeoutlier(val_genNCS20, val_genS20, val_curGrid20, val_genAc20, val_rotS20, timestamp20)
    val1SemOut58, val2SemOut58, val3SemOut58, val4SemOut58, val5SemOut58, tsSemOut58, q7558, q2558 = removeoutlier(val_genNCS58, val_genS58, val_curGrid58, val_genAc58, val_rotS58, timestamp58)

    print("tempo de códigos com listas e Numpy:", round(time() - t0, 3), "s")

    return val1SemOut20, val2SemOut20, val3SemOut20, val4SemOut20, val5SemOut20, tsSemOut20, q7520, q2520, val1SemOut58, val2SemOut58, val3SemOut58, val4SemOut58, val5SemOut58, tsSemOut58, q7558, q2558


def prep_analogicas_pandas(consulta1, consulta2, conn):
    t1 = time()

    df = pd.read_sql(consulta1, conn)

    conn.close()

    timestamp20 = []
    val_genNCS20 = []
    val_genS20 = []
    val_curGrid20 = []
    val_genAc20 = []
    val_rotS20 = []

    # --------------------------------------------Duplicados e Congelados--------------------------------------------- #
    errorsTS20 = []
    errorsV120 = []
    errorsV220 = []
    errorsV320 = []
    errorsV420 = []
    errorsV520 = []
    val_ncs20 = []
    val_s20 = []
    val_cur20 = []
    val_g20 = []
    val_r20 = []
    ts20 = []

    for k in range(len(df) - 1):
        k = k + 1
        diffTS20 = timestamp20[k] - timestamp20[k - 1]
        diffV120 = val_genNCS20[k] - val_genNCS20[k - 1]
        diffV220 = val_genS20[k] - val_genS20[k - 1]
        diffV320 = val_curGrid20[k] - val_curGrid20[k - 1]
        diffV420 = val_genAc20[k] - val_genAc20[k - 1]
        diffV520 = val_rotS20[k] - val_rotS20[k - 1]
        if diffTS20 == timedelta(0):  # duplicados
            if (timestamp20[k - 1].minute % 10 == 0) and (timestamp20[k - 1].second < 7):
                ts20.append(timestamp20[k])
                val_ncs20.append(val_genNCS20[k])
                val_s20.append(val_genS20[k])
                val_cur20.append(val_curGrid20[k])
                val_g20.append(val_genAc20[k])
                val_r20.append(val_rotS20[k])
            else:
                errorsTS20.append(timestamp20[k])
                errorsV120.append(val_genNCS20[k])
                errorsV220.append(val_genS20[k])
                errorsV320.append(val_curGrid20[k])
                errorsV420.append(val_genAc20[k])
                errorsV520.append(val_rotS20[k])
        elif (timestamp20[k].minute % 10 == 0) and (timestamp20[k].second < 7):  # congelados
            if (timestamp20[k - 1].minute % 10 == 0) and (timestamp20[k - 1].second < 7) and (diffTS20.seconds < 500):
                ts20.append(timestamp20[k])
                val_ncs20.append(val_genNCS20[k])
                val_s20.append(val_genS20[k])
                val_cur20.append(val_curGrid20[k])
                val_g20.append(val_genAc20[k])
                val_r20.append(val_rotS20[k])
            else:
                errorsTS20.append(timestamp20[k])
                errorsV120.append(val_genNCS20[k])
                errorsV220.append(val_genS20[k])
                errorsV320.append(val_curGrid20[k])
                errorsV420.append(val_genAc20[k])
                errorsV520.append(val_rotS20[k])
        else:  # amostra filtrada
            ts20.append(timestamp20[k])
            val_ncs20.append(val_genNCS20[k])
            val_s20.append(val_genS20[k])
            val_cur20.append(val_curGrid20[k])
            val_g20.append(val_genAc20[k])
            val_r20.append(val_rotS20[k])

    val_genNCS20 = np.array(val_ncs20)
    val_genS20 = np.array(val_s20)
    val_curGrid20 = np.array(val_cur20)
    val_genAc20 = np.array(val_g20)
    val_rotS20 = np.array(val_r20)
    timestamp20 = np.array(ts20)

    # -------------------------------------------------------------------------------------------------------------------- # aero 58
    cur = conn.cursor()
    cur.execute(consulta2)

    timestamp58 = []
    val_genNCS58 = []
    val_genS58 = []
    val_curGrid58 = []
    val_genAc58 = []
    val_rotS58 = []

    for row in cur:
        timestamp58.append(row[0])
        val_genNCS58.append(row[1])
        val_genS58.append(row[2])
        val_curGrid58.append(row[3])
        val_genAc58.append(row[4])
        val_rotS58.append(row[5])

    cur.close()
    timestamp58 = np.array(timestamp58)
    val_genNCS58 = np.array(val_genNCS58)
    val_genS58 = np.array(val_genS58)
    val_curGrid58 = np.array(val_curGrid58)
    val_genAc58 = np.array(val_genAc58)
    val_rotS58 = np.array(val_rotS58)
    amostra58 = len(timestamp58)
    # --------------------------------------------Duplicados e Congelados--------------------------------------------- #
    errorsTS58 = []
    errorsV158 = []
    errorsV258 = []
    errorsV358 = []
    errorsV458 = []
    errorsV558 = []
    val_ncs58 = []
    val_s58 = []
    val_cur58 = []
    val_g58 = []
    val_r58 = []
    ts58 = []

    for k in range(amostra58 - 1):
        k = k + 1
        diffTS58 = timestamp58[k] - timestamp58[k - 1]
        diffV158 = val_genNCS58[k] - val_genNCS58[k - 1]
        diffV258 = val_genS58[k] - val_genS58[k - 1]
        diffV358 = val_curGrid58[k] - val_curGrid58[k - 1]
        diffV458 = val_genAc58[k] - val_genAc58[k - 1]
        diffV558 = val_rotS58[k] - val_rotS58[k - 1]
        if diffTS58 == timedelta(0):  # duplicados
            if (timestamp58[k - 1].minute % 10 == 0) and (timestamp58[k - 1].second < 7):
                ts58.append(timestamp58[k])
                val_ncs58.append(val_genNCS58[k])
                val_s58.append(val_genS58[k])
                val_cur58.append(val_curGrid58[k])
                val_g58.append(val_genAc58[k])
                val_r58.append(val_rotS58[k])
            else:
                errorsTS58.append(timestamp58[k])
                errorsV158.append(val_genNCS58[k])
                errorsV258.append(val_genS58[k])
                errorsV358.append(val_curGrid58[k])
                errorsV458.append(val_genAc58[k])
                errorsV558.append(val_rotS58[k])
        elif (timestamp58[k].minute % 10 == 0) and (timestamp58[k].second < 7):  # congelados
            if (timestamp58[k - 1].minute % 10 == 0) and (timestamp58[k - 1].second < 7) and (diffTS58.seconds < 500):
                ts58.append(timestamp58[k])
                val_ncs58.append(val_genNCS58[k])
                val_s58.append(val_genS58[k])
                val_cur58.append(val_curGrid58[k])
                val_g58.append(val_genAc58[k])
                val_r58.append(val_rotS58[k])
            else:
                errorsTS58.append(timestamp58[k])
                errorsV158.append(val_genNCS58[k])
                errorsV258.append(val_genS58[k])
                errorsV358.append(val_curGrid58[k])
                errorsV458.append(val_genAc58[k])
                errorsV558.append(val_rotS58[k])
        else:  # amostra filtrada
            ts58.append(timestamp58[k])
            val_ncs58.append(val_genNCS58[k])
            val_s58.append(val_genS58[k])
            val_cur58.append(val_curGrid58[k])
            val_g58.append(val_genAc58[k])
            val_r58.append(val_rotS58[k])

    val_genNCS58 = np.array(val_ncs58)
    val_genS58 = np.array(val_s58)
    val_curGrid58 = np.array(val_cur58)
    val_genAc58 = np.array(val_g58)
    val_rotS58 = np.array(val_r58)
    timestamp58 = np.array(ts58)

    conn.close()  # fecha porta de comunicação com o BD

    # -------------------------------------------------------------------------------------------------------------------- #

    def removeoutlier(values1, values2, values3, values4, values5, times):  # define a função com uma variavel de entrada
        fator = 3  # 1.5 é o fator de multiplicacao
        q75, q25 = np.percentile(values1, [75, 25])  # retorna o terceiro e primeiro quartil
        iqr = q75 - q25  # calcula o iqr(interquartile range)

        lowpass = q25 - (iqr * fator)  # calcula o valor minimo para aplicar no filtro
        highpass = q75 + (iqr * fator)  # calcula o valor maximo para aplicar no filtro

        outliers = np.argwhere(values1 < lowpass)  # descobre onde estao os valores menores que o valor minimo
        values1 = np.delete(values1, outliers)  # deleta esses valores
        values2 = np.delete(values2, outliers)
        values3 = np.delete(values3, outliers)
        values4 = np.delete(values4, outliers)
        values5 = np.delete(values5, outliers)
        times = np.delete(times, outliers)

        outliers = np.argwhere(values1 > highpass)  # descobre onde estao os valores maiores que o valor maximo
        values1 = np.delete(values1, outliers)  # deleta esses valores
        values2 = np.delete(values2, outliers)
        values3 = np.delete(values3, outliers)
        values4 = np.delete(values4, outliers)
        values5 = np.delete(values5, outliers)
        times = np.delete(times, outliers)

        return values1, values2, values3, values4, values5, times, q75, q25  # retorna a variavel sem outliers

    val1SemOut20, val2SemOut20, val3SemOut20, val4SemOut20, val5SemOut20, tsSemOut20, q7520, q2520 = removeoutlier(val_genNCS20, val_genS20, val_curGrid20, val_genAc20, val_rotS20, timestamp20)
    val1SemOut58, val2SemOut58, val3SemOut58, val4SemOut58, val5SemOut58, tsSemOut58, q7558, q2558 = removeoutlier(val_genNCS58, val_genS58, val_curGrid58, val_genAc58, val_rotS58, timestamp58)

    print("tempo codigos com Pandas:", round(time() - t1, 3), "s")

    return val1SemOut20, val2SemOut20, val3SemOut20, val4SemOut20, val5SemOut20, tsSemOut20, q7520, q2520, val1SemOut58, val2SemOut58, val3SemOut58, val4SemOut58, val5SemOut58, tsSemOut58, q7558, q2558

#prep_analogicas_listas(consulta1, consulta2, conn)
#prep_analogicas_pandas(consulta1, consulta2, conn)
"""
