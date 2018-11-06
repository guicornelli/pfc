# -------------------------------------------------------------------------------------------------------------------- # CONSULTAR E ANALISAR BANCO DE DADOS DE ALARMES E EVENTOS DOS 6 AEROGERADORES #
import pymssql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import time
import seaborn as sns
import hypertools as hyp
from feature_selector.feature_selector import FeatureSelector

# -------------------------------------------------------------------------------------------------------------------- # Configurar display de valores e resultados no console
np.set_printoptions(linewidth=500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# -------------------------------------------------------------------------------------------------------------------- # Conexão com BD SQL Server
tini = time.time()
conn = pymssql.connect(host='GUILHERME', user='roquec', password='roquec', database='ISOTROL', as_dict=False,
                       charset='UTF-8')

# -------------------------------------------------------------------------------------------------------------------- # String da consulta para puxar os dados
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
# -------------------------------------------------------------------------------------------------------------------- # Biblioteca Pandas fará a consulta e disopnibilizará resultado no Dataframe
parques = ['01', '20', '38', '58', '63', '88']

#sql_comp_variavel_aeros = ("SELECT * "
#                           "FROM [TotalProduction_A"+str(k)+"] "
#                           "ORDER BY [TimeStampDateTimeUTC]; ")

sql_analogicas = ("SELECT DISTINCT dbo.GenNCSBearingTemp_A20.TimeStampDateTimeUTC AS Timestamp, "
                  "dbo.GenNCSBearingTemp_A20.FieldValueConvert AS GenNCSBearingTemp "
                  "FROM dbo.GenNCSBearingTemp_A20 "
                  "ORDER BY Timestamp; ")

df = pd.read_sql(sql_analogicas, conn)
conn.close()

rejeitados = []

for i in range(len(df.index) - 1):
    i = i + 1
    diffTS = df['Timestamp'][i] - df['Timestamp'][i - 1]
    if (df['Timestamp'][i].minute % 10 == 0) and (df['Timestamp'][i].second < 7):
        if (df['Timestamp'][i - 1].minute % 10 == 0) and (df['Timestamp'][i - 1].second < 7) and (diffTS.seconds < 500):
            rejeitados.append(i)

plt.scatter(df.index, df['GenNCSBearingTemp'], marker='.', alpha=0.4)

fig, (ax1, ax2) = plt.subplots(2, 1, sharex='all', sharey='all', figsize=(19.2, 10.8), dpi=100)

ax1.scatter(df['Timestamp'], df['GenNCSBearingTemp'], c="k", alpha=0.5, marker='.')
ax1.set_ylabel("Raw Data")
ax1.grid(True)

df.index = pd.DatetimeIndex(df.Timestamp)
df['GenNCSBearingTemp'].resample('1Min').mean()

novo = pd.DataFrame()
novo['GenNCSBearingTemp'] = df.GenNCSBearingTemp.resample('1Min').mean()


consulta_1min = ("With cte As "
                 "(Select DateAdd(minute, 1 * (DateDiff(minute, '20000101', TimeStampDateTimeUTC) / 1), '20000101') As TimeStampDateTimeUTC, FieldValueConvert " 
                 "From [ISOTROL].[dbo].[ActivePower_A01]) "
                 "Select TimeStampDateTimeUTC, Cast(Avg(FieldValueConvert) As decimal(12,2)) As FieldValueConvert "
                 "From cte "
                 "Group By TimeStampDateTimeUTC "
                 "Order By TimeStampDateTimeUTC;")

consulta_1hour = ("With cte As "
                  "(Select DateAdd(hour, 1 * (DateDiff(hour, '20000101', TimeStampDateTimeUTC) / 1), '20000101') As TimeStampDateTimeUTC, FieldValueConvert " 
                  "From [ISOTROL].[dbo].[ActivePower_A01]) "
                  "Select TimeStampDateTimeUTC, Cast(Avg(FieldValueConvert) As decimal(12,2)) As FieldValueConvert "
                  "From cte "
                  "Group By TimeStampDateTimeUTC "
                  "Order By TimeStampDateTimeUTC;")

min1 = pd.DataFrame()
min1["timestamp"] = pd.date_range(start='27/12/2016 14:00:00', end='10/11/2017 07:00:00', freq='min')

min2 = pd.DataFrame()
min2["timestamp"] = pd.date_range(start='27/12/2017 07:00:00', end='01/10/2018 12:00:00', freq='min')

df_1min = pd.concat([min1, min2])
df_1min.reset_index(drop=True, inplace=True)
# df = pd.read_sql(consulta, conn)

for k in variaveis:   # consultar medias de 1 min para retirar variaveis inuteis
    print(k)
    cur = conn.cursor()
    cur.execute("With cte As "
                "(Select DateAdd(minute, 1 * (DateDiff(minute, '20000101', TimeStampDateTimeUTC) / 1), '20000101') As TimeStampDateTimeUTC, FieldValueConvert " 
                "From [ISOTROL].[dbo].["+k+"_A01]) "
                "Select TimeStampDateTimeUTC, Cast(Avg(FieldValueConvert) As decimal(12,2)) As FieldValueConvert "
                "From cte "
                "Group By TimeStampDateTimeUTC "
                "Order By TimeStampDateTimeUTC;")
    for row in cur:
        idx = df_1min.index[df_1min["timestamp"] == row[0]].tolist()
        df_1min.loc[idx, ""+k+""] = row[1]
    cur.close()

tfim = time.time()
texec = (tfim - tini)
print(round((texec / 60.0), 3))
conn.close()
print("acabou df")
df_copy = df_1min.copy()
teste = df_copy.drop('timestamp', axis=1)
teste.fillna(0, inplace=True)
scatter_matrix(teste.astype(float), alpha=0.2, figsize=(10.8, 7.2), diagonal='kde')

plt.tight_layout()

"""‘bar’ or ‘barh’ for bar plots
‘hist’ for histogram
‘box’ for boxplot
‘kde’ or 'density' for density plots
‘area’ for area plots
‘scatter’ for scatter plots
‘hexbin’ for hexagonal bin plots
‘pie’ for pie plots"""

correlations = teste.astype(float).corr(method='pearson')

plt.matshow(correlations.corr())

fig, ax = plt.subplots(figsize=(10.8, 7.2))
ax.matshow(correlations)
plt.xticks(range(len(correlations.columns)), correlations.columns, rotation=90)
plt.yticks(range(len(correlations.columns)), correlations.columns)

sns.heatmap(correlations,
            xticklabels=correlations.columns.values,
            yticklabels=correlations.columns.values)

plt.tight_layout()

f, ax = plt.subplots(figsize=(10.8, 7.2))

sns.heatmap(correlations, mask=np.zeros_like(correlations, dtype=np.bool), cmap=sns.diverging_palette(220, 10, as_cmap=True),
            square=True, ax=ax)


teste = teste.drop(var_retiradas, axis=1)
correlations_pearson = teste.astype(float).corr(method='pearson')
correlations_spearman = teste.astype(float).corr(method='spearman')
correlations_kendall = teste.astype(float).corr(method='kendall')


geo = hyp.load(teste)
print(geo.get_data().head())
geo.plot()
hyp.plot(teste)
hyp.describe(teste)
data = hyp.analyze(teste, normalize='within', reduce='PCA', ndims=10,
                align='hyper')
# plot it
hyp.plot(data)


for i, row in correlations.iterrows():
    for j, column in row.iteritems():
        if column > 0.98:
            print(column, i, j)


# plot correlated values
plt.rcParams['figure.figsize'] = [16, 6]

fig2, ax = plt.subplots(nrows=1, ncols=4)

ax = ax.flatten()

cols = ['ActivePowerSetpoint', 'NoiseLevelCommLost', 'IceDetTemp', 'GridRectTemp']
colors = ['#415952', '#f35134', '#243AB5', '#243AB5']
j = 0

for i in ax:
    if j == 0:
        i.set_ylabel('NOISE LEVEL')
    i.scatter(teste[cols[j]], teste['NoiseLevel'],  alpha=0.5, color=colors[j])
    i.set_xlabel(cols[j])
    i.set_title('Pearson: %s' % correlations_pearson.loc[cols[j]]["NoiseLevel"].round(6)+' Spearman: %s \n' % correlations_spearman.loc[cols[j]]["NoiseLevel"].round(6)+
                ' Kendall: %s' % correlations_kendall.loc[cols[j]]["NoiseLevel"].round(6))
    j += 1

plt.show()

plt.tight_layout()


### consultar dados por minuto, retirar linhas zeradas, juntar com aero1,2,3,4,5,6, classificar os alertas, aplicar algoritmo, ver resultados
### comparar com uso de todas as variaveis

#    indexes = df[((df['TimeIniUTC'] > pd.Timestamp(2017, 11, 10, 0, 0, 0)) & (df['TimeIniUTC'] < pd.Timestamp(2017, 12, 27, 0, 0, 0))) |  # pega os index dos pontos em que não ha mediçao analogica
 #                (df['TimeIniUTC'] > pd.Timestamp(2018, 1, 9, 11, 0, 0))].index.values
#    df.drop(indexes, inplace=True)  # remove do dataframe os index selecionados
#   df.reset_index(drop=True, inplace=True)