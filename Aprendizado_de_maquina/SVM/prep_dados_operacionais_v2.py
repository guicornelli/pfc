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
sql_analogicas = ("SELECT DISTINCT [TimeStampDateTimeUTC], "
                  "[FieldValueConvert] "
                  "FROM [ISOTROL].[dbo].[ActivePower_A01] "
                  "ORDER BY [TimeStampDateTimeUTC]; ")

print("primeiro exemplo iniciado")

t0 = time()
cur = sql_conn_isotrol.cursor()
cur.execute(sql_analogicas)

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

errorsT = []
errorsV = []
val = []
ts = []

t2 = time()

for k in range(amostra - 1):
    k = k + 1
    diffTS20 = timestamp[k] - timestamp[k - 1]
    if diffTS20 == timedelta(0):                                                    # duplicados
        if (timestamp[k - 1].minute % 10 == 0) and (timestamp[k - 1].second < 7):
            ts.append(timestamp[k])
            val.append(value[k])
        else:
            errorsT.append(timestamp[k])
            errorsV.append(value[k])
    elif (timestamp[k].minute % 10 == 0) and (timestamp[k].second < 7):             # congelados
        if (timestamp[k - 1].minute % 10 == 0) and (timestamp[k - 1].second < 7) and (diffTS20.seconds < 500):
            ts.append(timestamp[k])
            val.append(value[k])
        else:
            errorsT.append(timestamp[k])
            errorsV.append(value[k])
    else:                                                                           # amostra filtrada
        ts.append(timestamp[k])
        val.append(value[k])

valnp = np.array(val)
valnp = np.array(ts)

t3 = time()
t_filtragem = round(t3-t2, 3)
t_total = t_consulta + t_filtragem

print("primeiro exemplo finalizado em:", t_total, " segundos")

#############################################################################################################################################################################
#############################################################################################################################################################################
#############################################################################################################################################################################
print("segundo exemplo iniciado")

errorsT2 = []
errorsV2 = []
val2 = []
ts2 = []

time2 = time()

for k in range(amostra - 1):
    k = k + 1
    if (timestamp[k].minute % 10 == 0) and (timestamp[k].second == 0):               # congelados
        if abs(timestamp[k+1] - timestamp[k]) == timedelta(0):
            ts2.append(timestamp[k])
            val2.append(value[k])
        else:
            errorsT2.append(timestamp[k])
            errorsV2.append(value[k])
    else:                                                                           # amostra filtrada
        ts2.append(timestamp[k])
        val2.append(value[k])

valnp2 = np.array(val2)
valnp2 = np.array(ts2)

time3 = time()
time_filtragem = round(time3-time2, 3)
time_total = t_consulta + time_filtragem

print("segundo exemplo finalizado em:", time_total, " segundos")
#############################################################################################################################################################################
#############################################################################################################################################################################
#############################################################################################################################################################################
print("terceiro exemplo iniciado")

time0 = time()
dataframe = pd.read_sql(sql_analogicas, sql_conn_isotrol)
time1 = time()
time_consulta = round(time1-time0, 3)

time2 = time()

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

print("terceiro exemplo finalizado em:", time_filtragem, " segundos")

#############################################################################################################################################################################
#############################################################################################################################################################################
#############################################################################################################################################################################
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