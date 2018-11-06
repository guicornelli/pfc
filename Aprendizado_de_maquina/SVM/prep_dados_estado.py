"""
    Consulta a banco de dados com os alarmes e eventos

    Retorna dataframes: alarmes;
                        estados e comandos;
                        dataset alarmes p/ treino;
                        dataset alarmes p/ teste.
"""

import pymssql
import pandas as pd

# -------------------------------------------------------------------------------------------------------------------- # Configurar display de valores e resultados no console
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Conexão com BD SQL Server
sql_conn_gamesa = pymssql.connect(host='GUILHERME', user='roquec', password='roquec', database='GAMESA', as_dict=False, charset='UTF-8')

# String da consulta para puxar os dados
sql_alarmes_eventos = ("SELECT * "
                       "FROM [Alarmes_Morrinhos_6Aeros] "
                       "WHERE	[AlarmDesc] LIKE '518 %' "           # consultando apenas o alarme 518
                       "ORDER BY [TimeIniUTC]; ")

# Classificação das reações de cada alarme atuado --> reação = [lista de códigos dos alarmes correspondentes]
aviso = [117, 211, 315, 413, 419, 423, 427, 429, 430, 506, 514, 515, 516, 517,
         518, 703, 707, 711, 718, 721, 823, 1828, 2100, 2115, 2116, 2131, 2198]

pausa = [114, 203, 306, 312, 313, 402, 403, 407, 426, 500, 501, 502, 600,
         615, 915, 916, 1821, 1822, 2106]

stop = [103, 108, 110, 409, 812, 906, 913]

emerg = [119, 201, 205, 208, 212, 222, 405, 410, 416, 603, 700, 813, 900,
         901, 902, 907, 908, 911, 912, 1835, 1837, 2102, 2114, 2118, 5201,
         5203, 5204, 5210, 5212, 5213, 5216, 5226, 5232, 5237, 5238, 5240]

# Classificação da disponibilidade do aerogerador conforme cada alarme atuado --> disponibilidade = [lista de códigos dos alarmes correspondentes]
disp = [117, 211, 313, 315, 405, 413, 419, 423, 427, 429, 430, 506, 514, 515, 516,
        517, 518, 703, 707, 711, 718, 721, 823, 1828, 2100, 2115, 2116, 2131, 2198]


def prep_alarmes_estados(consulta, conn):

    # Biblioteca Pandas fará a consulta e disponibilizará resultado no dataframe 'df'
    df = pd.read_sql(consulta, conn)
    conn.close()                                                     # fecha porta de comunicação com o BD GAMESA
    # df.head()                                                        # exemplifica como ficou o dataframe
    # df.info()                                                        # infos do dataframe
    # df.describe()                                                    # estatísticas do dataframe

    # Selecionar o index dos pontos em que não há medição analógica (datas retiradas de análises visuais)
    indexes = df[((df['TimeIniUTC'] > pd.Timestamp(2017, 11, 10, 0, 0, 0)) &
                  (df['TimeIniUTC'] < pd.Timestamp(2017, 12, 27, 0, 0, 0))) |
                 (df['TimeIniUTC'] > pd.Timestamp(2018, 1, 9, 11, 0, 0))].index.values

    df.drop(indexes, inplace=True)                                   # remove do dataframe 'df' os indexes selecionados
    df.reset_index(drop=True, inplace=True)                          # reinicia o index do datrafame para sequenciá-lo novamente

    """
        *** Operações válidas somente para o alarme consultado ***
        
        Deve-se simplificar os alarmes. 
        Haviam muitas ocorrências curtas em sequência, o que é a mesma
            situação de uma ocorrência com período de tempo maior.
        Portanto, copia-se o tempo de término da última ocorrência
            da sequência e substitui na primeira, podendo excluir as demais. 

        Exemplo abaixo válido somente para o alarme consultado:
            518 - Temperatura alarma cojinete L.O.A 
            (Aviso de alta temperatura do rolamento NDE do gerador).  
        Caso for consultar outro alarme, deve-se analisar primeiro as 
            ocorrências e se é necessário realizar o mesmo procedimento.
    """
    # Copiando TimeEnd da última ocorrência para primeira, manualmente (através da análise do dataframe 'df')
    df['TimeEndUTC'][2] = pd.Timestamp(2017, 10, 16, 21, 0, 26)
    df['TimeEndUTC'][35] = pd.Timestamp(2017, 10, 21, 18, 43, 7)
    df['TimeEndUTC'][41] = pd.Timestamp(2017, 10, 25, 4, 28, 57)
    df['TimeEndUTC'][51] = pd.Timestamp(2017, 10, 25, 19, 45, 35)

    # Retirada das curtas ocorrências que não terão mais uso
    df.drop(range(3, 35), inplace=True)
    df.drop(range(36, 40), inplace=True)
    df.drop(range(42, 51), inplace=True)
    df.drop(range(52, 57), inplace=True)
    df.reset_index(drop=True, inplace=True)                          # reinicia o index do datrafame para sequenciá-lo novamente

    """
        *** Operações válidas para todos os alarmes, independente de consulta específica ***
        
        Adição de colunas ao dataframe 'df': 
            Deltas: diferença entre tempo final de atuação do alarme / evento e
                    tempo de ínicio;
            Codes: código (type int) do alarme para ordenação correta;
            Reação: reação do sistema para a atuação do alarme, podendo ser
                    aviso, pausa, stop ou emergência;
            Disponibilidade: informação se com o alarme atuado, o aerogerador
                             está disponível para operar ou não disponível.
    """
    # Criação da coluna 'Deltas' em 'df'
    deltas = df['TimeEndUTC'] - df['TimeIniUTC']                     # faz a diferença entre tempo de início e término de atuação
    df.insert(loc=2, column='Delta', value=deltas)                   # insere as diferenças de tempo calculadas (Deltas) no dataframe, sendo a propriedade loc = posição da coluna

    # Criação da coluna 'Codes' em 'df', onde os alarmes terão seus códigos Gamesa, e os eventos terão código 0 para facilitar separação futura do dataframe
    codes = []
    for n in df['AlarmDesc']:                                        # percorre cada linha do da coluna descrição de alarme do dataframe atual
        try:                                                         # função tentativa
            if (int(n[0:3])) != 175:                                 # tenta transformar os três primeiros caracteres em inteiros, e se forem diferentes de 175, adiciona-os na lista 'codes'
                codes.append(int(n[0:4]))
            else:                                                    # se forem igual a 175, adiciona-se o código 0 na lista 'codes', pois não se trata de um alarme
                codes.append(int(0))
        except ValueError:                                           # caso a tentativa de transformar os primeiros caracteres em inteiros for falha
            codes.append(int(0))                                     # adiciona-se 0 na lista 'codes', pois se tratam de eventos fora da lista de alarmes da Gamesa
    df.insert(loc=3, column='Codes', value=codes)                    # insere os códigos na coluna 'Codes' no dataframe após a coluna Deltas inserida anteriormente

    # Criação das colunas 'Reação' e 'Disponibilidade' em 'df'
    reac = []
    disponib = []
    for i in df['Codes']:                                            # percorre todas as linhas da coluna recém adicionada 'Codes'
        if i in aviso:                                               # se o respectivo código pertencer à algum tipo de reação, adiciona esta classificação na lista 'reac'
            reac.append("Aviso")
        elif i in pausa:
            reac.append("Pausa")
        elif i in stop:
            reac.append("Stop")
        elif i in emerg:
            reac.append("Emerg")
        else:
            reac.append("NaN")

        if i in disp:                                                # se o respectivo código pertencer à lista dos códigos 'disp', adiciona esta classificação na lista 'disponib'
            disponib.append("Sim")
        elif i == 0:
            disponib.append("NaN")
        else:
            disponib.append("Nao")

    df.insert(loc=6, column='Reacao', value=reac)                    # adicionar as colunas 'Reacao' e 'Disponibilidade' com as reações e disponibilidades de cada código no dataframe df
    df.insert(loc=7, column='Disponibilidade', value=disponib)

    """
        Realiza-se a separação do dataframe 'df' contendo alarmes e eventos,
            em dois dataframes: al --> contém apenas alarmes da listagem Gamesa;
                                ec --> contêm estados e comandos.
                                
        *** Operações válidas somente para o alarme consultado ***                        
        Posteriormente, para visualização e entendimento da ocorrência deste alarme,
            separamos o dataframe 'al' nos datasets para "treino" e "teste" dos algoritmos 
            de classificação, porém servirão apenas para orientar a pré-classificação dos
            conjuntos de dados das características selecionadas de medição dos aerogeradores. 
    """
    mask = df['Codes'] == 0                                          # máscara, seleciona tudo o que não é alarme
    ec = df[mask]                                                    # cria dataframe 'ec' contendo todas linhas e colunas de 'df' relacionadas aos estados e comandos
    ec.reset_index(drop=True, inplace=True)                          # reset nos índices de 'ec' para criar ordem
    al = df[~mask]                                                   # cria dataframe 'al' contendo todas linhas e colunas de 'df' relacionadas ao oposto de estados e comandos, ou seja, alarmes
    al.reset_index(drop=True, inplace=True)                          # reset nos índices de 'al' para criar ordem

    # tsuniques = al.groupby('AlarmAero')['TimeIniUTC'].unique()       # tempos que ocorreram as falhas por aero

    # Separando em dados para "treino" e "teste" da orientação da classificação por meio dos algoritmos de aprendizado de máquina
    dftrain1 = al.iloc[2:9]                                          # 2 datasets selecionados para orientação do treinamento
    dftrain2 = al.iloc[10:]
    dftest1 = al.iloc[:2]                                            # 2 dataset selecionados para orientação do teste
    dftest2 = al.iloc[9:10]
    dfframestrain = [dftrain1, dftrain2]                             # criação de lista de dataset de treino e dataset de teste, para realizar função de concatenar os datasets
    dfframestest = [dftest1, dftest2]
    df_train = pd.concat(dfframestrain)
    df_test = pd.concat(dfframestest)

    return al, ec, df_train, df_test

al, ec, df_train, df_test = prep_alarmes_estados(sql_alarmes_eventos, sql_conn_gamesa)
print(al)