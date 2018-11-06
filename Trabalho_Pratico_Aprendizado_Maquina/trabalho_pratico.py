import os
import re
import collections
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from nltk.stem.snowball import SnowballStemmer
import string
from time import time

# -------------------------------------------------------------------------------------------------------------------- # Configurar display de valores e resultados no console
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 100)

data_folder = "C:/Users/guilh/PycharmProjects/17274-COAtlantic/Trabalho_Pratico_Aprendizado_Maquina/webkb"
ROOT_FOLDER = data_folder
data = []
for output in os.listdir(ROOT_FOLDER):                                                                       # le todos os arquivos da pasta e coloca na lista data, separando pelas pastas
    for institution in os.listdir(os.path.join(ROOT_FOLDER, output)):
        for file_name in os.listdir(os.path.join(ROOT_FOLDER, output, institution)):
            if os.path.isfile(os.path.join(ROOT_FOLDER, output, institution, file_name)):
                data.append({
                    'output': output,
                    'institution': institution,
                    'file_name': file_name
                })

data = sorted(data, key=lambda k: k['output'])                                                               # organiza em ordem das pastas de classificacao
df = pd.DataFrame(data)                                                                                      # passa lista para um dataframe em pandas
outputs = df.output.unique()                                                                                 # lista todas classificacoes unicas
institution = df.institution.unique()                                                                        # lista todas instituicoes unicas
files = df.file_name.unique()                                                                                # lista todos arquivos unicas


def check_data(dataset):
    if len(dataset) != 8282:
        print("Problema com os arquivos utilizados, a quantidade de arquivos deveria ser 8282, mas a quantidade encontrada foi de", len(data))
    else:
        print("Aparentemente tudo ok com os dados")


def get_file_path_from_item(item):
    return os.path.join(ROOT_FOLDER, item['output'], item['institution'], item['file_name'])


def get_soup(item):
    try:
        with open(get_file_path_from_item(item)) as f:
            soup = BeautifulSoup(f, 'html.parser')
    except:
        print("deu erro aqui vei")
    return soup


def get_soup_ifhaserror(item):
    try:
        with open(get_file_path_from_item(item)) as f:
            soup = BeautifulSoup(f, 'html.parser')
    except:
        with open(get_file_path_from_item(item), encoding="ISO-8859-1") as f:
            soup = BeautifulSoup(f, 'html.parser')
    return soup


def funcaotop(item):
    try:
        with open(get_file_path_from_item(item)) as f:
            soup = BeautifulSoup(f, 'html.parser')
    except:
        with open(get_file_path_from_item(item), encoding="ISO-8859-1") as f:
            soup = BeautifulSoup(f, 'html.parser')

    words = re.findall('\w+', soup.getText().lower())
    no_integers = [x for x in words if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())]
    no_stopwords = [x for x in no_integers if len(x)>1 and x not in sw]
    count = collections.Counter(no_stopwords).most_common()
    words_stemmer = [stemmer.stem(i) for i in no_stopwords]
    count_stemm = collections.Counter(words_stemmer).most_common()
    words_count = len(no_stopwords)
    unique_words = len(count)
    unique_words_stemm = len(count_stemm)
    # all_words.append(no_integers)

    return words_count, unique_words, unique_words_stemm, words_stemmer, no_stopwords


def flattened(counter):
    flat = [val for sublist in counter for val in sublist]
    return flat


def select(count):
    first = [x[0] for x in count]
    return first

t0 = time()

all_words = []
sw = stopwords.words("english")
stemmer = SnowballStemmer("english")

check_data(data)
asd = df.apply(funcaotop, axis=1, result_type='expand')                                                                                    # aplica funcaotop no df

t1 = time()
print("tempo de algoritmo dps loop:", round(t1-t0, 3), "s")

df["words_count"], df["words_unique"], df["words_unique_stemm"], df["words_stemm"], df["words"] = asd[0], asd[1], asd[2], asd[3], asd[4]   # resultados joga no df
total_words = df.words_count.sum()                                                                                                         # qts palavras no total
words_output = df.groupby('output')['words_stemm'].sum()                                                                                   # agrupa as palavras stemmer pelo output
WORD = df['words_stemm'].sum()                                                                                                             # agrupa todas as palavras stemmer
t2 = time()
print("tempo de algoritmo:", round(t2-t0, 3), "s")

all_uniques = collections.Counter(WORD).most_common()                                                                                      # contabiliza frequencia das palavras stemmer
course_uniques = collections.Counter(words_output.course).most_common()
department_uniques = collections.Counter(words_output.department).most_common()
faculty_uniques = collections.Counter(words_output.faculty).most_common()
other_uniques = collections.Counter(words_output.other).most_common()
project_uniques = collections.Counter(words_output.project).most_common()
staff_uniques = collections.Counter(words_output.staff).most_common()
student_uniques = collections.Counter(words_output.student).most_common()

all_uniques200 = collections.Counter(WORD).most_common(200)                                                                                # contabiliza frequencia das palavras stemmer 200 mais freq
course_uniques100 = collections.Counter(words_output.course).most_common(100)
department_uniques100 = collections.Counter(words_output.department).most_common(100)
faculty_uniques100 = collections.Counter(words_output.faculty).most_common(100)
other_uniques100 = collections.Counter(words_output.other).most_common(100)
project_uniques100 = collections.Counter(words_output.project).most_common(100)
staff_uniques100 = collections.Counter(words_output.staff).most_common(100)
student_uniques100 = collections.Counter(words_output.student).most_common(100)

all_uniques200_words = select(all_uniques200)
df2 = pd.DataFrame(data)

# flattened = [val for sublist in all_words for val in sublist]
# countFlat = collections.Counter(flattened).most_common()
# uniques = [x[0] for x in countFlat if len(x[0])>1 and x[0] not in sw]
# words_stemmer = [stemmer.stem(i) for i in uniques]


"""

t_reg_al = len(al)                                               # total ocorrências
t_tim_al = al.Delta.sum()                                        # total tempo de atuados
ocorr_aero = al.AlarmAero.value_counts()                         # quantidade de ocorrências por aero
ocorr_alarm = al.Codes.value_counts()                            # quantidade de ocorrências de cada alarme
t_aero = al.groupby('AlarmAero')['Delta'].sum()                  # tempo de registros atuados por aero
t_alarm = al.groupby('Codes')['Delta'].sum()                     # tempo de registros atuados por alarm


Bsoup = get_soup(df.iloc[0])
words = re.findall('\w+', Bsoup.getText().lower())                                                  # acha todas as palavras e numeros do texto
no_integers = [x for x in words if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())]            # retira os numeros
count = collections.Counter(no_integers).most_common()                                              # faz a contagem da frequencia das palavras no texto
lista = [x[1] for x in count]                                                                       # so faz uma listinha com as freq e contabiliza soma no fim pra ver se bate com a quantidade total
lista = np.array(lista)
words_count = lista.sum()
flattened = [val for sublist in p for val in sublist]
if len(no_integers) == lista.sum():
    print("belezinha")
else:
    print("opa deu ruim")
data = sorted(data, key=lambda k: k['output'])


Temos a pasta principal Webkb com os arquivos > Classificação: course, departament, faculty, other, project, staff, student > 
Instituições: cornell, misc, texas, washington, wisconsin > Arquivos.

Objetivo: Ler os arquivos e os classificar apenas nas classes mencionadas acima, sem contar instituição.

Método: Através das palavras contidas em cada arquivo, iremos classificar em course, departament, faculty...

Preparação: Ler arquivos, retirar texto, separar e contar cada palavra. Retirar outliers (numeros, palavras sem nexo que não serão uteis);
            Teremos uma lista de palavras existentes em cada arquivo, assim como a frequencia das mesmas no arquivo.
            Teremos uma lista de todas as palavras existentes em todos os arquivos, assim como frequencia das mesmas.
            Montar um dataframe com [Index] [file_name] [institution] [output] [palavra1] [palavra2] [palavra3]    ...
                                       0       http_^^    cornell       course   5           4           5         ...
                                       1       http_^^    cornell       course   3           1           2         ...
            O numero reprensentando as palavras é a frequencia das mesmas em cada arquivo, assim teremos um vetor 
            com as palavras e frequencias delas em cada arquivo, bem como a classificaçao do mesmo (output).
            
            Assim, o vetor X de treino sera [palavra1, palavra2, palavra3, ...] = [output] que é o vetor y de treino
            
Assim teremos multiplas dimensões, + de 100 provavelmente, recurso adequado para aplicação do SVM.
"""