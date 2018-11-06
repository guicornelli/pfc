import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

##isotrol = pd.read_excel("C:/Users/g.souza/Desktop/alarmesisotrol.xlsx", sheet_name="isotrol", pairse_cols=0)
##gamesa = pd.read_excel("C:/Users/g.souza/Desktop/alarmesgamesa.xlsx", sheet_name="gamesa", pairse_cols=0)

##for i in isotrol.values:
##    for j in gamesa.values:



##if gamesa['desc'] == 'Aerogenerador en MARCHA':
##    gamesa.drop('')

##df = pd.DataFrame({'Data': [10, 20, 30, 20, 15, 30, 45]})

'''writer = pd.ExcelWriter("pandas_datetime.xlsx",
                        engine='xlsxwriter',
                        datetime_format='mmm d yyyy hh:mm:ss',
                        date_format='mmmm dd yyyy')

df.to_excel(writer, sheet_name='Sheet1', startrow=1, startcol=8, header=False, index=False)  # mindados

writer.save()

b = []
for i in dataFrame.ExtraídoIsotrol:
    for j in df.keys():
        if i == j[0:-4]:
            print('max eh %f em %s' % ((df[j][0]), j))
            b.append(df[j][6])
[round(elem, 2) for elem in b]'''

df = pd.read_csv("C:/Users/guilh/Desktop/dadosgerados_real.csv", header=None, names=["Amostras"])
df["Amostras em ms"] = df["Amostras"]/1000000
##df.hist()


ax = df.hist(column="Amostras em ms", bins=150, grid=False, figsize=(12,8), color='#86bf91', zorder=2, rwidth=0.9)

ax = ax[0]
for x in ax:

    # Despine
    x.spines['right'].set_visible(False)
    x.spines['top'].set_visible(False)
    x.spines['left'].set_visible(False)

    # Switch off ticks
    x.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="on")

    # Draw horizontal axis lines
    vals = x.get_yticks()
    for tick in vals:
        x.axhline(y=tick, linestyle='dashed', alpha=0.4, color='#eeeeee', zorder=1)

    # Remove title
    x.set_title("")

    # Set x-axis label
    x.set_xlabel("Tempo de execução (milisegundos)", labelpad=20, weight='bold', size=12)

    # Set y-axis label
    x.set_ylabel("Amostras", labelpad=20, weight='bold', size=12)

    # Format y-axis label
    x.yaxis.set_major_formatter(StrMethodFormatter('{x:,g}'))

print("teste")