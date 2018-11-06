import pymssql
import numpy as np
import pandas as pd
from datetime import timedelta
from sklearn.svm import SVC
from time import time
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, confusion_matrix

np.set_printoptions(linewidth=500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

variaveis = ['ActivePower', 'AmbientTemperature', 'BusVoltage', 'CapacityFactor', 'ControlModuleTemp',
             'ConvAirTemp', 'CoolerTemp', 'FG8AirTemp', 'GearboxBearingTemp', 'GearboxOilTemp',
             'GearboxShaftBearingGrease', 'GenActivePower', 'GenCSBearingTemp', 'GenNCSBearingTemp',
             'GenRingTemp', 'GenSpeedTop', 'GenWinding1Temp', 'GenWinding2Temp', 'GenWinding3Temp',
             'GreaseGenBearingTank', 'GridCurrent', 'GridFrec', 'GridIndTemp', 'GridRectTemp', 'GridVoltage',
             'HydrOilTemp', 'HydrPress', 'NacelleOrientation', 'NacelleTemp', 'PitchAngle', 'ProduciblePower',
             'Radiator1Temp', 'Radiator2Temp', 'ReactivePower', 'RectActivePower', 'RectCurrent', 'RotorCurrent',
             'RotorInvTemp', 'RotorSpeed', 'ServoVoltage', 'StatorActivePower', 'StatorCurrent', 'StatorReactivePower',
             'TrafoWinding1Temp', 'TrafoWinding2Temp', 'TrafoWinding3Temp', 'WindDirection', 'WindSpeed', 'YawBrakePress']

# Conexão com BD SQL Server
sql_conn_isotrol = pymssql.connect(host='GUILHERME', user='roquec', password='roquec', database='ISOTROL', as_dict=False, charset='UTF-8')
cont = 0
meusdados=pd.DataFrame(data=None, columns=variaveis)

for i in variaveis:
    cont = cont + 1
    sql_analogicas = ("SELECT DISTINCT dbo."+i+"_A20.TimeStampDateTimeUTC AS Timestamp, "
                      "dbo."+i+"_A20.FieldValueConvert AS "+i+" "
                      "FROM dbo."+i+"_A20 "
                      "WHERE ([TimeStampDateTimeUTC] > CONVERT(datetime, CAST('2017-04-27 00:00:00.000' AS DATETIMEOFFSET(4)), 1) AND "
                      "[TimeStampDateTimeUTC] < CONVERT(datetime, CAST('2017-04-30 12:00:00.000' AS DATETIMEOFFSET(4)), 1)) OR "
                      "([TimeStampDateTimeUTC] > CONVERT(datetime, CAST('2017-10-03 00:00:00.000' AS DATETIMEOFFSET(4)), 1) AND "
                      "[TimeStampDateTimeUTC] < CONVERT(datetime, CAST('2017-10-07 00:00:00.000' AS DATETIMEOFFSET(4)), 1)) OR "
                      "([TimeStampDateTimeUTC] > CONVERT(datetime, CAST('2017-10-14 00:00:00.000' AS DATETIMEOFFSET(4)), 1) AND "
                      "[TimeStampDateTimeUTC] < CONVERT(datetime, CAST('2017-10-17 12:00:00.000' AS DATETIMEOFFSET(4)), 1)) OR "
                      "([TimeStampDateTimeUTC] > CONVERT(datetime, CAST('2017-10-18 00:00:00.000' AS DATETIMEOFFSET(4)), 1) AND "
                      "[TimeStampDateTimeUTC] < CONVERT(datetime, CAST('2017-10-26 12:00:00.000' AS DATETIMEOFFSET(4)), 1)) OR "
                      "([TimeStampDateTimeUTC] > CONVERT(datetime, CAST('2017-12-26 00:00:00.000' AS DATETIMEOFFSET(4)), 1) AND "
                      "[TimeStampDateTimeUTC] < CONVERT(datetime, CAST('2017-12-30 00:00:00.000' AS DATETIMEOFFSET(4)), 1)) OR "
                      "([TimeStampDateTimeUTC] > CONVERT(datetime, CAST('2018-01-03 00:00:00.000' AS DATETIMEOFFSET(4)), 1) AND "
                      "[TimeStampDateTimeUTC] < CONVERT(datetime, CAST('2018-01-09 11:00:00.000' AS DATETIMEOFFSET(4)), 1)) "
                      "ORDER BY TimeStampDateTimeUTC; ")

    df = pd.read_sql(sql_analogicas, sql_conn_isotrol, index_col=['Timestamp'])

    '''df2 = pd.read_sql(sql_analogicas, sql_conn_isotrol)
    df2.index = pd.DatetimeIndex(df2.Timestamp)

    writer = pd.ExcelWriter('PythonExport.xlsx')
    df1.to_excel(writer, 'Sheet1')
    df2.to_excel(writer, 'Sheet2')
    writer.save()'''

    meusdados[i] = df[i].resample('1Min').mean().values

df.insert(loc=1, column='Timestamp', value=df.index)

rejeitados = []

for i in range(len(df.index) - 1):
    i = i + 1
    diffTS = df['Timestamp'][i] - df['Timestamp'][i - 1]
    if (df['Timestamp'][i].minute % 10 == 0) and (df['Timestamp'][i].second < 7):
        if (df['Timestamp'][i - 1].minute % 10 == 0) and (df['Timestamp'][i - 1].second < 7) and (diffTS.seconds < 500):
            rejeitados.append(i)

print("pera")
sql_conn_isotrol.close()