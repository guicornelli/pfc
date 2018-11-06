"""
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

# -------------------------------------------------------------------------------------------------------------------- # Import das bibliotecas utilizadas
import os
import re
import random
import graphviz
import collections
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from time import time
from bs4 import BeautifulSoup
from sklearn.svm import SVC
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split, cross_validate
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

# -------------------------------------------------------------------------------------------------------------------- # Configurar display de valores e resultados no console
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 100)

# -------------------------------------------------------------------------------------------------------------------- # Leitura e extracao dos dados da pasta Webkb
data_folder = "C:/Users/guilh/PycharmProjects/17274-COAtlantic/Trabalho_Pratico_Aprendizado_Maquina/webkb"     # modificar para pasta em que se encontra o arquivo no seu pc
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
# -------------------------------------------------------------------------------------------------------------------- # Treinamento,teste e validacao do SVM
x = df_class[all_uniques_count_words]                                                            # todas as features selecionadas
y = df_class["classificacao"]                                                                    # vetor de classificacao manual
# parametros test_size=Defaut eh 0.25, random_state=Defaut eh None)
x_train, x_test, y_train, y_test = train_test_split(x, y)                                        # separa os dados para treinamento e teste do algoritmos

clf_svm = SVC(kernel="rbf")                                                                          # cria o classificador SVM
# clf = SVC(kernel="rbf", C = 215, gamma=3.643)
# reduzir conjunto de treinamento pra 1% (dividir por 100)
# features_train = features_train[:len(features_train)/100]
# labels_train = labels_train[:len(labels_train)/100]
t3 = time()
clf_svm.fit(x_train, y_train)                                                                        # treina o classificador com os dados de treino
t_train_SVM = round(time()-t3, 3)
print("tempo de treinamento:", t_train_SVM, "s")
t4 = time()
pred_svm = clf_svm.predict(x_test)                                                                       # usa para classificar os dados do vetor x de teste, retornando em "pred"
t_test_SVM = round(time()-t4, 3)
print("tempo de testes:", t_test_SVM, "s")

# Accuracy
acc_svm = accuracy_score(pred_svm, y_test)                                                               # compara a predicao com a classificacao original manual de y_test
print("Accuracy: {0:.2f} % ".format(100*acc_svm))

# Confusion Matrix
print(confusion_matrix(y_test, pred_svm))
print("Confusion Matrix:")
cm_svm = confusion_matrix(y_test, pred_svm)
cm_svm = cm_svm.astype('float') / cm_svm.sum(axis=1)[:, np.newaxis]
df_cm_svm = pd.DataFrame(cm_svm, index=outputs, columns=outputs)
plt.figure(figsize=(10, 7))
plt.tight_layout()
ax_svm = sns.heatmap(df_cm_svm, annot=True, cmap=plt.cm.RdPu)
ax_svm.set(xlabel='Predicted label', ylabel='True label', title='Confusion Matrix')
plt.show()

# Relatorio da classificacao (predicao)
print(classification_report(y_test, pred_svm))

# Cross-Validation
number_of_cross_validations = 10
cvs_svm = cross_validate(clf_svm, x, y, cv=number_of_cross_validations)
cvs_mean_svm = {k+"_mean": v.mean() for k, v in cvs_svm.items()}
cvs_std_svm = {k+"_std": v.std() for k, v in cvs_svm.items()}
print("Test Score: {test_score_mean:.4f} (+/- {test_score_std:.4f}) \n"
      "Fit Time: {fit_time_mean:.4f} s (+/- {fit_time_std:.4f}) \n"
      "Score Time:  {score_time_mean:.4f} s (+/- {score_time_std:.4f}) \n"
      "Train Score:  {train_score_mean:.4f} (+/- {train_score_std:.4f})".format(**{**cvs_mean_svm, **cvs_std_svm}))

# -------------------------------------------------------------------------------------------------------------------- # Treinamento,teste e validacao do decisiontree
seed = 389751212
random.seed(a=seed)

clf_dt = tree.DecisionTreeClassifier(criterion='gini', min_samples_split=20, random_state=seed)     # cria o classificador DT
clf_dt.fit(x_train, y_train)                                                                        # treina o classificador com os dados de treino
t5 = time()
t_train_DT = round(time()-t5, 3)
print("tempo de treinamento:", t_train_DT, "s")
t6 = time()
pred_dt = clf_dt.predict(x_test)                                                                    # usa para classificar os dados do vetor x de teste, retornando em "pred"
t_test_DT = round(time()-t6, 3)
print("tempo de testes:", t_test_DT, "s")

# Accuracy
acc_dt = accuracy_score(pred_dt, y_test)                                                               # compara a predicao com a classificacao original manual de y_test
print("Accuracy: {0:.2f} % ".format(100*acc_dt))

# Confusion Matrix
print(confusion_matrix(y_test, pred_dt))
print("Confusion Matrix:")
cm_dt = confusion_matrix(y_test, pred_dt)
cm_dt = cm_dt.astype('float') / cm_dt.sum(axis=1)[:, np.newaxis]
df_cm_dt = pd.DataFrame(cm_dt, index=outputs, columns=outputs)
plt.figure(figsize=(10, 7))
plt.tight_layout()
ax_dt = sns.heatmap(df_cm_dt, annot=True,cmap=plt.cm.RdPu)
ax_dt.set(xlabel='Predicted label', ylabel='True label', title='Confusion Matrix')
plt.show()

# Relatorio da classificacao (predicao)
print(classification_report(y_test, pred_dt))

# Cross-Validation
number_of_cross_validations = 10
cvs_dt = cross_validate(clf_dt, x, y, cv=number_of_cross_validations)
cvs_mean_dt = {k+"_mean": v.mean() for k, v in cvs_dt.items()}
cvs_std_dt = {k+"_std": v.std() for k, v in cvs_dt.items()}
print("Test Score: {test_score_mean:.4f} (+/- {test_score_std:.4f}) \n"
      "Fit Time: {fit_time_mean:.4f} s (+/- {fit_time_std:.4f}) \n"
      "Score Time:  {score_time_mean:.4f} s (+/- {score_time_std:.4f}) \n"
      "Train Score:  {train_score_mean:.4f} (+/- {train_score_std:.4f})".format(**{**cvs_mean_dt, **cvs_std_dt}))

dot_data = tree.export_graphviz(clf_dt, out_file=None,                                          # Plotar a árvore de decisão
                                feature_names=x.columns,
                                class_names=outputs,
                                filled=True, rounded=True,
                                special_characters=True)
graph = graphviz.Source(dot_data)

# -------------------------------------------------------------------------------------------------------------------- # Treinamento,teste e validacao do RF
clf_rf = RandomForestClassifier(n_estimators=90, criterion='entropy')                            # cria o classificador RF
clf_rf.fit(x_train, y_train)                                                                     # treina o classificador com os dados de treino
t5 = time()
t_train_RF = round(time()-t5, 3)
print("tempo de treinamento:", t_train_RF, "s")
t6 = time()
pred_rf = clf_rf.predict(x_test)                                                                    # usa para classificar os dados do vetor x de teste, retornando em "pred"
t_test_RF = round(time()-t6, 3)
print("tempo de testes:", t_test_RF, "s")

# Accuracy
acc_rf = accuracy_score(pred_rf, y_test)                                                                # compara a predicao com a classificacao original manual de y_test
print("Accuracy: {0:.2f} % ".format(100*acc_rf))

# Confusion Matrix
print(confusion_matrix(y_test, pred_rf))
print("Confusion Matrix:")
cm_rf = confusion_matrix(y_test, pred_rf)
cm_rf = cm_rf.astype('float') / cm_rf.sum(axis=1)[:, np.newaxis]
df_cm_rf = pd.DataFrame(cm_rf, index=outputs, columns=outputs)
plt.figure(figsize=(10, 7))
plt.tight_layout()
ax_rf = sns.heatmap(df_cm_rf, annot=True, cmap=plt.cm.RdPu)
ax_rf.set(xlabel='Predicted label', ylabel='True label', title='Confusion Matrix')
plt.show()

# Relatorio da classificacao (predicao)
print(classification_report(y_test, pred_rf))

# Cross-Validation
number_of_cross_validations = 10
cvs_rf = cross_validate(clf_rf, x, y, cv=number_of_cross_validations)
cvs_mean_rf = {k+"_mean": v.mean() for k, v in cvs_rf.items()}
cvs_std_rf = {k+"_std": v.std() for k, v in cvs_rf.items()}
print("Test Score: {test_score_mean:.4f} (+/- {test_score_std:.4f}) \n"
      "Fit Time: {fit_time_mean:.4f} s (+/- {fit_time_std:.4f}) \n"
      "Score Time:  {score_time_mean:.4f} s (+/- {score_time_std:.4f}) \n"
      "Train Score:  {train_score_mean:.4f} (+/- {train_score_std:.4f})".format(**{**cvs_mean_rf, **cvs_std_rf}))
