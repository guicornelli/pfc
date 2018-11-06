import os
import re
import collections
import numpy as np
import pandas as pd
from time import time
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

# -------------------------------------------------------------------------------------------------------------------- # Configurar display de valores e resultados no console
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 100)

# -------------------------------------------------------------------------------------------------------------------- # Leitura e extracao dos dados da pasta Webkb
data_folder = "C:/Users/guilh/Desktop/captions.txt"     # modificar para pasta em que se encontra o arquivo no seu pc

with open(data_folder, 'r') as f:
    i = 0
    for line in f:
        i = i + 1
        if (i+1) % 4 == 0:
            print(line)


words = re.findall('\w+', s.getText().lower())


ROOT_FOLDER = data_folder
data = []
for output in os.listdir(ROOT_FOLDER):                                                           # le todos os arquivos da pasta e coloca na lista data, separando pelas pastas
    for institution in os.listdir(os.path.join(ROOT_FOLDER, output)):
        for file_name in os.listdir(os.path.join(ROOT_FOLDER, output, institution)):
            if os.path.isfile(os.path.join(ROOT_FOLDER, output, institution, file_name)):
                data.append({
                    'classificacao': output,
                    'instituicao': institution,
                    'arquivo': file_name
                })

data = sorted(data, key=lambda p: p['classificacao'])                                            # organiza em ordem das pastas de classificacao
df = pd.DataFrame(data)                                                                          # passa lista para um dataframe da biblioteca pandas
outputs = df.classificacao.unique()                                                              # lista todas classificacoes unicas
institution = df.instituicao.unique()                                                            # lista todas instituicoes unicas
files = df.arquivo.unique()                                                                      # lista todos arquivos unicas
sw = stopwords.words("english")                                                                  # lista de palavras sem contexto
stemmer = SnowballStemmer("english")                                                             # irá reduzir as palavras, por ex: "solutions" > "solut", evitando alguns problemas de plural, por ex


def check_data(dataset):                                                                         # funcao verifica integridade dos dados
    if len(dataset) != 8282:
        print("Problema com os arquivos utilizados, a quantidade de arquivos deveria ser 8282, mas a quantidade encontrada foi de", len(data))
    else:
        print("Aparentemente tudo ok com os dados")


def get_file_path_from_item(item):                                                               # recebe como parametro uma linha de data, ou dataframe, e retorna o caminho do arquivo da linha
    return os.path.join(ROOT_FOLDER, item['classificacao'], item['instituicao'], item['arquivo'])


def get_soup(item):                                                                              # abre e le os arquivos html, com ajuda da biblioteca BeautifulSoup
    try:
        with open(get_file_path_from_item(item)) as f:
            s = BeautifulSoup(f, 'html.parser')
    except:
        with open(get_file_path_from_item(item), encoding="ISO-8859-1") as f:
            s = BeautifulSoup(f, 'html.parser')
    return s


def flattened(l):
    flat = [val for sublist in l for val in sublist]                                             # recebe lista de listas e retorna apenas uma lista
    return flat


def select(tuple_list, j):                                                                       # seleciona todos elementos do indice i da lista de tuplas
    elements = [x[j] for x in tuple_list]
    return elements


t0 = time()                                                                                      # inicia contagem de tempo para verificar tempo dos algoritmos
words_stemmer = [0] * len(df)
unique_words_stemmer = [0] * len(df)

# iteracao entre linhas do dataframe: nao foi usada a funcao df.apply pois esta se mostrou levemente mais rapida
for i, row in df.iterrows():                                                                     # i: dataframe index; row: each row in series format
    soup = get_soup(row)                                                                         # le o arquivo html da linha
    words = re.findall('\w+', soup.getText().lower())                                            # encontra todas as palavras separadamente, do arquivo
    no_integers = [x for x in words if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())]     # retira os numeros inteiros
    no_stopwords = [x for x in no_integers if len(x) > 1 and x not in sw]                        # retira os stopwords
    words_stemmer[i] = [stemmer.stem(i) for i in no_stopwords]                                   # realiza a compactacao de cada palavra
    count_stemmer = collections.Counter(words_stemmer[i]).most_common()                          # retorna lista com contagem de cada palavra apos reduzida, do arquivo html
    unique_words_stemmer[i] = len(count_stemmer)                                                 # valor numero de quantas palavras unicas, apos filtragem, existem no arquivo

t1 = time()
print("tempo de algoritmo dps loop:", round(t1-t0, 3), "s")

df_class = pd.DataFrame(data)
df_class["words_unique_stemmer"], df_class["words_stemmer"] = unique_words_stemmer, words_stemmer  # complementa dataframe df_class com os resultados das iteracoes anteriores
words_output = df_class.groupby('classificacao')['words_stemmer'].sum()                            # agrupa as palavras stemmer pela classificao
WORD = df_class['words_stemmer'].sum()                                                             # agrupa todas as palavras stemmer

t2 = time()
print("tempo de algoritmo:", round(t2-t0, 3), "s")

# -------------------------------------------------------------------------------------------------------------------- # Estruturaçao do dataframe
all_uniques_count = collections.Counter(WORD).most_common(500)                                   # seleciona as X palavras mais frequentes de todas as palavras existentes em todos so arquivos
all_uniques_count_words = select(all_uniques_count, 0)                                           # pega apenas o nome das palavras, retira da tupla com as frequencias

qts = [0] * len(df)
for k in all_uniques_count_words:                                                                # para cada palavra unica existente (da quantidade x selecionada anteriormente)
    for n, row in df_class.iterrows():                                                           # verifica pela linha do dataframe
        qts[n] = row.words_stemmer.count(k)                                                      # contabiliza quantas vezes essa palavra aparece na lista de palavras do arquivo
    df_class[k] = qts                                                                            # insere numa nova coluna criada do dataframe, a qual vira a ser uma feature

# Aqui se pode criar uma funcao para entrar como parametro qual algoritmo utilizar e acabar com a repeticao do codigo