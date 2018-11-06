# -------------------------------------------------------------------------------------------------------------------- # CONSULTAR E ANALISAR BANCO DE DADOS DE ALARMES E EVENTOS DOS 6 AEROGERADORES #
import pymssql
import numpy as np
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import pandas as pd
import squarify
import matplotlib

# -------------------------------------------------------------------------------------------------------------------- # Configurar display de valores e resultados no console
np.set_printoptions(linewidth=500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# -------------------------------------------------------------------------------------------------------------------- # Conexão com BD SQL Server
conn = pymssql.connect(host='GUILHERME', user='roquec', password='roquec', database='GAMESA', as_dict=False,
                       charset='UTF-8')

# -------------------------------------------------------------------------------------------------------------------- # String da consulta para puxar os dados
consulta = ("SELECT DATEADD(HOUR, 3, [TimeIni]) AS TimeIniUTC "
            ",DATEADD(HOUR, 3, [TimeEnd]) AS TimeEndUTC "
            ",[AlarmDesc] "
            ",[AlarmAero] "
            "FROM [Alarmes_Morrinhos_Resumo] "
            "ORDER BY [TimeIniUTC]; ")

# -------------------------------------------------------------------------------------------------------------------- # Biblioteca Pandas fará a consulta e disopnibilizará resultado no Dataframe
df = pd.read_sql(consulta, conn)
# df.head()                                                         # exemplifica como ficou
# df.info()                                                         # infos do dataframe
conn.close()                                                        # Fecha porta de comunicação com o BD

deltas = df['TimeEndUTC'] - df['TimeIniUTC']                        # faz o delta entre tempo de inicio e termino de atuacao
df.insert(loc=2, column='Delta', value=deltas)                      # insere os deltas no dataframe

codes = []
for n in df['AlarmDesc']:                                           # adicionar uma coluna com os códigos dos alarmes no dataframe df
    try:
        if (int(n[0:3])) != 175:
            codes.append(int(n[0:4]))
        else:
            codes.append(int(0))
    except ValueError:
        codes.append(int(0))
df.insert(loc=3, column='Codes', value=codes)

# -------- # Classificação das reações de cada alarme
aviso = [117, 211, 315, 413, 419, 423, 427, 429, 430, 506, 514, 515, 516, 517,
         518, 703, 707, 711, 718, 721, 823, 1828, 2100, 2115, 2116, 2131, 2198]

pausa = [114, 203, 306, 312, 313, 402, 403, 407, 426, 500, 501, 502, 600,
         615, 915, 916, 1821, 1822, 2106]

stop = [103, 108, 110, 409, 812, 906, 913]

emerg = [119, 201, 205, 208, 212, 222, 405, 410, 416, 603, 700, 813, 900,
         901, 902, 907, 908, 911, 912, 1835, 1837, 2102, 2114, 2118, 5201,
         5203, 5204, 5210, 5212, 5213, 5216, 5226, 5232, 5237, 5238, 5240]

# -------- # Classificação da disponibilidade do aerogerador conforme cada alarme atuado
disp = [117, 211, 313, 315, 405, 413, 419, 423, 427, 429, 430, 506, 514, 515, 516,
        517, 518, 703, 707, 711, 718, 721, 823, 1828, 2100, 2115, 2116, 2131, 2198]

reac = []
disponib = []

for i in df['Codes']:                                               # verifica linha por linha qual o código e cria uma lista com a reação e disponibilidade conforme o alarme / evento
    if i in aviso:
        reac.append("Aviso")
    elif i in pausa:
        reac.append("Pausa")
    elif i in stop:
        reac.append("Stop")
    elif i in emerg:
        reac.append("Emerg")
    else:
        reac.append("NaN")

for i in df['Codes']:
    i = i
    if i in disp:
        disponib.append("Sim")
    elif i == 0:
        disponib.append("NaN")
    else:
        disponib.append("Nao")

df.insert(loc=6, column='Reacao', value=reac)                       # adicionar as coluna com as reações e disponibilidade no dataframe df
df.insert(loc=7, column='Disponibilidade', value=disponib)

mask = df['Codes'] == 0                                             # separar o dataframe df em dois: ec = estados e comandos, al = alarmes da listagem Gamesa
ec = df[mask]
ec.reset_index(drop=True, inplace=True)                             # reset no index
al = df[~mask]
al.reset_index(drop=True, inplace=True)

# -------------------------------------------------------------------------------------------------------------------- # Visão Geral sobre os dados al
t_reg_al = len(al)                                               # total ocorrências
t_tim_al = al.Delta.sum()                                        # total tempo de atuados
ocorr_aero = al.AlarmAero.value_counts()                         # quantidade de ocorrências por aero
ocorr_alarm = al.Codes.value_counts()                            # quantidade de ocorrências de cada alarme
t_aero = al.groupby('AlarmAero')['Delta'].sum()                  # tempo de registros atuados por aero
t_alarm = al.groupby('Codes')['Delta'].sum()                     # tempo de registros atuados por alarm

# -------------------------------------------------------------------------------------------------------------------- # Análise 2D individual sobre os dados al
x = [i[0:4] for i in al.sort_values(by='Codes')['AlarmDesc'].unique()]                     # seleciona os primeiros 4 caracteres da string para pegar os códigos dos alarmes organizados e únicos
y = ocorr_alarm.sort_index().values                                                        # organiza a distribuição de ocorrencia dos alarmes pelo index, ou seja, pelos códigos
volume = t_alarm.astype('timedelta64[s]').astype(int).sort_index().values                  # organiza o tempo atuado dos alarmes (segundos) pelo index, ou seja, pelos códigos
# colors = 0.003*t_alarm.astype('timedelta64[s]').astype(int).sort_index().values/0.003*ocorr_alarm.sort_index().values  # lista de cores para o gráfico
label = []
for j in al.sort_values(by='Codes')['Codes'].unique():
    if al['Reacao'][np.where(al.Codes == j)[0][0]] == 'Aviso' and al['Disponibilidade'][np.where(al.Codes == j)[0][0]] == 'Sim':
        label.append('gold')
    elif al['Reacao'][np.where(al.Codes == j)[0][0]] == 'Aviso' and al['Disponibilidade'][np.where(al.Codes == j)[0][0]] == 'Nao':
        label.append('tan')
    elif al['Reacao'][np.where(al.Codes == j)[0][0]] == 'Pausa' and al['Disponibilidade'][np.where(al.Codes == j)[0][0]] == 'Sim':
        label.append('aqua')
    elif al['Reacao'][np.where(al.Codes == j)[0][0]] == 'Pausa' and al['Disponibilidade'][np.where(al.Codes == j)[0][0]] == 'Nao':
        label.append('blue')
    elif al['Reacao'][np.where(al.Codes == j)[0][0]] == 'Stop' and al['Disponibilidade'][np.where(al.Codes == j)[0][0]] == 'Sim':
        label.append('purple')
    elif al['Reacao'][np.where(al.Codes == j)[0][0]] == 'Stop' and al['Disponibilidade'][np.where(al.Codes == j)[0][0]] == 'Nao':
        label.append('plum')
    elif al['Reacao'][np.where(al.Codes == j)[0][0]] == 'Emerg' and al['Disponibilidade'][np.where(al.Codes == j)[0][0]] == 'Sim':
        label.append('salmon')
    elif al['Reacao'][np.where(al.Codes == j)[0][0]] == 'Emerg' and al['Disponibilidade'][np.where(al.Codes == j)[0][0]] == 'Nao':
        label.append('red')

colors = ['gold', 'tan', 'aqua', 'blue', 'purple', 'plum', 'salmon', 'red']
estados = ['Aviso / Disp', 'Aviso / Indisp', 'Pausa / Disp', 'Pausa / Indisp', 'Stop / Disp', 'Stop / Indisp', 'Emerg / Disp', 'Emerg / Indisp']

# -------------------------------------------------------------------------------------------------------------------- #
volume = volume/3600

yaw = al.sort_values(by='Codes')['Codes'].unique()[0:6]
yaw_v = volume[0:6]
hidr = al.sort_values(by='Codes')['Codes'].unique()[6:13]
hidr_v = volume[6:13]
amb = al.sort_values(by='Codes')['Codes'].unique()[13:17]
amb_v = volume[13:17]
mult = al.sort_values(by='Codes')['Codes'].unique()[17:31]
mult_v = volume[17:31]
ger = al.sort_values(by='Codes')['Codes'].unique()[31:40]
ger_v = volume[31:40]
contr = al.sort_values(by='Codes')['Codes'].unique()[40:43]
contr_v = volume[40:43]
comu = al.sort_values(by='Codes')['Codes'].unique()[43:49]
comu_v = volume[43:49]
pitch = al.sort_values(by='Codes')['Codes'].unique()[49:52]
pitch_v = volume[49:52]
oper = al.sort_values(by='Codes')['Codes'].unique()[52:63]
oper_v = volume[52:63]
conex = al.sort_values(by='Codes')['Codes'].unique()[63:68]
conex_v = volume[63:68]
soft = al.sort_values(by='Codes')['Codes'].unique()[68:77]
soft_v = volume[68:77]
ccu = al.sort_values(by='Codes')['Codes'].unique()[77:]
ccu_v = volume[77:]
areas = [yaw, hidr, amb, mult, ger, contr, comu, pitch, oper, conex, soft, ccu]
p = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
areas_n = ['Sist. Rotação', 'Und. Hidráulica', 'Ambiente', 'Gearbox', 'Gerador', 'Controle', 'Comunicações', 'Pitch', 'Estados', 'Conexão Rede', 'Software', 'CCU']
areas_v = [yaw_v, hidr_v, amb_v, mult_v, ger_v, contr_v, comu_v, pitch_v, oper_v, conex_v, soft_v, ccu_v]
val_inic = [0, 6, 13, 17, 31, 40, 43, 49, 52, 63, 68, 77]
colors_disp = ['#96f97b',                     # yaw        light green
               '#95d0fc',                     # hidr       light blue
               '#fffe7a',                     # amb        light yellow
               '#fea993',                     # gear       light red --> light salmon
               '#fdaa48',                     # gera       light orange
               '#bf77f6',                     # contr      light purple
               '#ad8150',                     # comu       light brown
               '#d8dcd6',                     # pitch      light grey
               '#ffd1df',                     # oper       light pink
               '#90e4c1',                     # conex      light teal
               '#acbf69',                     # soft       light olive
               '#c292a1'                      # ccu        light mauve
               ]
colors_indisp = ['#15b01a',                   # green
                 '#0343df',                   # blue
                 '#ffff14',                   # yellow
                 '#e50000',                   # red
                 '#f97306',                   # orange
                 '#7e1e9c',                   # purple
                 '#653700',                   # brown
                 '#929591',                   # grey
                 '#ff81c0',                   # pink
                 '#029386',                   # teal
                 '#6e750e',                   # olive
                 '#ae7181'                    # mauve
                 ]


# -------------------------------------------------------------------------------------------------------------------- #   Treemap dos alarmes que deixam o aero indisp
width = 100.
height = 100.
cmap = matplotlib.cm.viridis

t_alarm_indisp = t_alarm.drop(labels=disp)

yaw_isum = t_alarm_indisp[0:5].astype('timedelta64[s]').astype(int).sum()
hid_isum = t_alarm_indisp[5:11].astype('timedelta64[s]').astype(int).sum()
amb_isum = t_alarm_indisp[11:13].astype('timedelta64[s]').astype(int).sum()
gea_isum = t_alarm_indisp[13:20].astype('timedelta64[s]').astype(int).sum()
ger_isum = t_alarm_indisp[20:23].astype('timedelta64[s]').astype(int).sum()
ctr_isum = t_alarm_indisp[23:26].astype('timedelta64[s]').astype(int).sum()
com_isum = t_alarm_indisp[26:27].astype('timedelta64[s]').astype(int).sum()
pit_isum = t_alarm_indisp[27:29].astype('timedelta64[s]').astype(int).sum()
est_isum = t_alarm_indisp[29:40].astype('timedelta64[s]').astype(int).sum()
red_isum = t_alarm_indisp[40:44].astype('timedelta64[s]').astype(int).sum()
sof_isum = t_alarm_indisp[44:48].astype('timedelta64[s]').astype(int).sum()
ccu_isum = t_alarm_indisp[48:].astype('timedelta64[s]').astype(int).sum()

indispsum = [yaw_isum, hid_isum, amb_isum, gea_isum, ger_isum, ctr_isum, com_isum, pit_isum, est_isum, red_isum, sof_isum, ccu_isum]
indispsum = np.array(indispsum)

# color scale on the population
# min and max values without Pau
mini, maxi = indispsum.min(), indispsum.max()
norm = matplotlib.colors.Normalize(vmin=mini, vmax=maxi)
colors_tree = [cmap(norm(value)) for value in indispsum]
# colors_tree[1] = "#FBFCFE"

# labels for squares
names = ["%s\n%.2fh" % name for name in zip(areas_n, indispsum/3600)]
# names[11] = "MAZERES-\nLEZONS\n%d km2\n%d hab" % (df2["superf"]["MAZERES-LEZONS"], df2["p11_pop"]["MAZERES-LEZONS"])


# -------- # Plots Quantidades
def plot_qtdades():
    plt.figure(figsize=(10.8, 7.2), dpi=100)                         # inicia figura com dimensões 1080p x 720p
    plt.subplot(211)                                                 # determina um subplot dentro da figura, com 2 linhas, 1 coluna, e escolhe a 1a posição
    ocorr_aero.plot.bar(title='Registros por Aerogeradores')         # desenha o gráfico de barras com as infos da série

    # plt.xticks([0, 1, 2, 3, 4, 5], ["A01", "A02", "A03", "A04", "A05", "A06"], size=9, rotation=0)  # caso não queira mostrar os nomes dos aerogeradores

    plt.xticks(size=9, rotation=90)                                   # configurações das anotações do eixo x
    plt.xlabel("$Aerogeradores$")                                    # Label eixo x
    plt.ylabel("$Ocorrências$ $Alarmes$")                            # Label eixo y
    for ii in range(len(ocorr_aero)):                                 # inserir os valores de cada barra em cima das mesmas
        plt.text(x=ii-0.045, y=ocorr_aero[ii] + 10, s=ocorr_aero[ii], size=9, color='k', rotation=45)

    plt.subplot(212)                                                 # determina um subplot dentro da mesma figura, com 2 linhas, 1 coluna, e escolhe a 2a posição
    ocorr_alarm.plot.bar(title='Registros por Alarmes')              # desenha o gráfico de barras com as infos da série
    plt.xticks(rotation=90, size=7)
    plt.xlabel("$Alarmes$ $Listados$")
    plt.ylabel("$Ocorrências$ $Alarmes$")
    for ii in range(len(ocorr_alarm)):
        plt.text(x=ii-0.25, y=ocorr_alarm.values[ii]+50, s=ocorr_alarm.values[ii], size=8, rotation=0, color='k')
    plt.tight_layout(pad=0.4, w_pad=0.9, h_pad=0.5)                  # ajuste dos plots para ficarem melhor dispostos na figura
    plt.subplots_adjust(bottom=0.08, top=0.95)
    plt.show()


# -------- # Plots Tempos
def plot_tempos():
    plt.figure(figsize=(10.8, 7.2), dpi=100)
    plt.subplot(211)
    t_aero.astype('timedelta64[h]').sort_values(ascending=False).plot.bar(title='Tempo de Alarme por Aerogeradores')

    # plt.xticks([0, 1, 2, 3, 4, 5], ["A01", "A02", "A03", "A04", "A05", "A06"], size=9, rotation=0)

    plt.xticks(size=9, rotation=0)
    plt.xlabel("$Aerogeradores$")
    plt.ylabel("$Tempo$ $Alarmes$ $Atuados$ $(horas)$")
    for ii in range(len(t_aero)):
        plt.text(x=ii-0.045, y=t_aero.astype('timedelta64[h]').sort_values(ascending=False)[ii],
                 s=t_aero.astype('timedelta64[h]').sort_values(ascending=False)[ii], size=9, color='k')
    plt.subplot(212)
    t_alarm.astype('timedelta64[h]').sort_values(ascending=False).plot.bar(title='Tempo de Alarme por Alarmes')
    plt.xticks(rotation=90, size=7)
    plt.xlabel("$Alarmes$ $Listados$")
    plt.ylabel("$Tempo$ $Alarme$ $Atuado$ $(horas)$")
    for ii in range(len(t_alarm)):
        plt.text(x=ii-0.25, y=t_alarm.astype('timedelta64[h]').sort_values(ascending=False).astype(int).values[ii]+170,
                 s=t_alarm.astype('timedelta64[h]').sort_values(ascending=False).astype(int).values[ii], size=8, rotation=20, color='k')
    plt.tight_layout(pad=0.4, w_pad=0.9, h_pad=0.5)
    plt.subplots_adjust(bottom=0.08, top=0.95)
    plt.show()


# -------- # Plots QuantidadexOcorênciaxAlarme
def plot_qtdade_ocorr():
    fig, ax = plt.subplots(figsize=(10.8, 7.2), dpi=100)                                       # constroi uma figura e eixos
    plt.title('Registros x Tempo Atuado por Alarme (horas)', weight='bold', fontsize=10)
    ax.tick_params(axis='x', labelrotation=90)
    ax.set_ylabel("$Quantidade$ $de$ $Registros$")
    ax.set_xlabel("$Alarmes$ $Listados$ $(Códigos)$")
    ax.scatter(x, y, s=volume, label=None, c=label, alpha=0.7, edgecolors="grey")         # gráfico de pontos, alarmes no eixo x, quantidade total de ocorrencias eixo y e volume é em tempo atuado

    legend1_line2d = list()                                                                    # construção das legendas
    for step in range(len(colors)):
        legend1_line2d.append(mlines.Line2D([0], [0],
                                            linestyle='none',
                                            marker='o',
                                            alpha=0.6,
                                            markersize=6,
                                            markerfacecolor=colors[step]))
    legend1 = plt.legend(legend1_line2d,
                         estados,
                         numpoints=1,
                         fontsize=10,
                         loc='upper right',
                         shadow=True)
    legend2_line2d = list()
    legend2_line2d.append(mlines.Line2D([0], [0],
                                        linestyle='none',
                                        marker='o',
                                        alpha=0.6,
                                        markersize=np.sqrt(10),
                                        markerfacecolor='#D3D3D3'))
    legend2_line2d.append(mlines.Line2D([0], [0],
                                        linestyle='none',
                                        marker='o',
                                        alpha=0.6,
                                        markersize=np.sqrt(100),
                                        markerfacecolor='#D3D3D3'))
    legend2_line2d.append(mlines.Line2D([0], [0],
                                        linestyle='none',
                                        marker='o',
                                        alpha=0.6,
                                        markersize=np.sqrt(1000),
                                        markerfacecolor='#D3D3D3'))
    legend2 = plt.legend(legend2_line2d,
                         ['10', '100', '1000'],
                         title='Tempo atuado (h)',
                         numpoints=1,
                         fontsize=10,
                         loc='center right',
                         frameon=False,
                         labelspacing=3,
                         handlelength=5,
                         borderpad=1
                         )
    plt.gca().add_artist(legend1)
    plt.setp(legend2.get_title(), fontsize=10)
    plt.tight_layout(pad=0.4, w_pad=0.9, h_pad=0.5)
    plt.show()


# -------- # Plots QuantidadexOcorênciaxAlarme
def tempo_atuado_area():
    graf = 0
    plt.figure(figsize=(10.8, 7.2), dpi=100)
    for ii in range(0, 12):
        if al['Disponibilidade'][np.where(al.Codes == areas[i][0])[0][0]] == 'Nao':
            cor = colors_indisp[ii]
        else:
            cor = colors_disp[ii]
        plt.bar(ii, volume[val_inic[ii]], edgecolor='white', linewidth=0.3, color=cor)
    for ii in areas_v:
        somat = 0
        for nn in range(len(ii)-1):
            if al['Disponibilidade'][np.where(al.Codes == areas[graf][nn+1])[0][0]] == 'Nao':
                cor = colors_indisp[graf]
            else:
                cor = colors_disp[graf]
            somat = somat + ii[nn]
            plt.bar(graf, ii[nn+1], bottom=somat, edgecolor='white', linewidth=0.3, color=cor)
        graf = graf + 1
    plt.xticks(p, areas_n, rotation=15)
    plt.xlabel("Áreas dos Alarmes")
    plt.ylabel("Tempo de alarme atuado (horas)")

    legend2_line2d = list()                                                                                    # construção das legendas
    legend2_line2d.append(mlines.Line2D([0], [0],
                                        linestyle='none',
                                        marker='s',
                                        alpha=0.1,
                                        markersize=9,
                                        markerfacecolor='#000000'))
    legend2_line2d.append(mlines.Line2D([0], [0],
                                        linestyle='none',
                                        marker='s',
                                        alpha=0.7,
                                        markersize=9,
                                        markerfacecolor='#000000'))
    legend2 = plt.legend(legend2_line2d,
                         ['Disponível\n(Cor clara)', 'Indisponível\n (Cor escura)'],
                         title='Aerogerador',
                         numpoints=1,
                         fontsize=10,
                         loc='upper right',
                         shadow=True,
                         labelspacing=1,
                         handlelength=5,
                         borderpad=1
                         )
    plt.setp(legend2.get_title(), fontsize=10)
    plt.tight_layout()
    plt.show()


# -------- # Plots Treemap alarmes indisp
def plot_treemap():
    fig = plt.figure(figsize=(10.8, 7.2), dpi=100)
    fig.suptitle("Tempo de indisponibilidade por alarmes atuados", fontsize=20)
    ax = fig.add_subplot(111, aspect="equal")
    ax = squarify.plot(sizes=indispsum / 3600, label=names, color=colors_tree, alpha=.6, edgecolor='black', linewidth=0.3)  # make plot
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Tempo de indisponibilidade por alarmes atuados", fontsize=14, fontweight="bold")

    # color bar
    # create dummy invisible image with a color map
    img = plt.imshow([indispsum / 3600], cmap=cmap)
    img.set_visible(False)
    fig.colorbar(img, orientation="vertical", shrink=.96)

    fig.text(.76, .9, "Horas", fontsize=14)

    plt.tight_layout()
    plt.show()

# -------------------------------------------------------------------------------------------------------------------- # Mapa de calor de alarmes por área

debug = "debug"
print("acabou")

'''# matriz com quantidade de registros de cada alarm por aero
teste = df.groupby(['AlarmDesc', 'AlarmAero']).size().unstack()
teste.fillna(0, inplace=True)

# dataframe com totais
teste2 = teste.copy()
teste2['Total'] = teste2[teste2.columns].sum(axis=1)
teste2.loc['Total'] = teste2.sum()

# matriz com quantidade de registros de cada aero por alarm
teste = df.groupby(['AlarmAero', 'AlarmDesc']).size().unstack()
teste.fillna(0, inplace=True)
teste.reset_index(inplace=True)                                     # caso precise colocar os indices normais

sns.heatmap(alarmes.ix[0:6, 2:], annot=True, yticklabels=alarmes.ix[0:6, 1], cmap='OrRd')

# -------------------------------------------------------------------------------------------------------------------- #
print("Total Registros de Ocorrências dos 6 Aeros: ", totalregistros)

for i in range(len(aero)):
    print("%s, %d registros, %.3f%% do total" % (aero[i], ocorrenciasXaero[i],
                                                 ocorrenciasXaero[i]*100/totalregistros))

for i in range(len(alarm)):
    print("%s, %d registros, %.6f%% do total, atuado por %dd %dh %dm %ds" % (alarm[i], ocorrenciasXalarm[i],
                                                                                   ocorrenciasXalarm[i]*100/totalregistros,
                                                                                   TempoAtuado[i].days,
                                                                                   (TempoAtuado[i].seconds/3600),
                                                                                   ((TempoAtuado[i].seconds/3600) % 1)*60,
                                                                                   ((((TempoAtuado[i].seconds / 3600) % 1)*60) % 1)*60))'''
# -------------------------------------------------------------------------------------------------------------------- #
