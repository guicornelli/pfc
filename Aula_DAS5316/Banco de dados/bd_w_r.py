# Banco de Dados - Exercício de implementação

import pymssql

conn = pymssql.connect(host='GUILHERME', user='aa', password='aa', database='DAS5316', as_dict=False,
                       charset='UTF-8')

cur = conn.cursor()

# Criar tabela no SQL Server

def create_table():
    cur.execute("CREATE TABLE IF NOT EXISTS Alunos(Nome TEXT, Matrícula REAL, Idade INTEGER, Ingresso INTEGER, Situação TEXT )")

# Inserir dados na tabela criada

def data_entry():
    cur.execute("INSERT INTO Alunos VALUES('Henrique',11202989,26,2011,'Cursando')")
    cur.execute("INSERT INTO Alunos VALUES('João',10114385,28,2010,'Formado')")
    cur.execute("INSERT INTO Alunos VALUES('Pedro',13100001,2,2013,'Trancamento')")
    cur.execute("INSERT INTO Alunos VALUES('Maísa',11280821,26,2011,'Cursando')")
    cur.execute("INSERT INTO Alunos VALUES('Patrick',14204123,24,2014,'Desistiu')")
create_table()
data_entry()

conn.commit()

# Ler todos dados do banco
def read_from_db():
    cur.execute('SELECT * FROM Alunos')
    data = cur.fetchall()
    for row in data:
        print(row)

# Saber quem trancou o curso
def read_trancou():
    cur.execute("SELECT Nome FROM Alunos WHERE situação = 'Trancamento'")
    data = cur.fetchall()
    print('Trancamento: ')
    for row in data:
        print(row)

# Saber quem entrou depois de 2012
def read_ing():
    cur.execute("SELECT Nome FROM Alunos WHERE ingresso > 2012")
    data = cur.fetchall()
    print('Ingresso Após 2012 ')
    for row in data:
        print(row)

# Saber quem tem o nome específico
def read_nome():
    cur.execute("SELECT idade FROM Alunos WHERE nome = 'Patrick'")
    data = cur.fetchall()
    print('Idade de Patrick ')
    for row in data:
        print(row)

def update_name():
    cur.execute("UPDATE Alunos SET nome='Carlos' WHERE nome = 'João'")
    conn.commit()
    print('Atualizou nome de João para Carlos')
    cur.execute('SELECT * FROM Alunos')
    data = cur.fetchall()
    for row in data:
        print(row)


read_from_db()
read_trancou()
read_ing()
read_nome()
update_name()

# fecha cursor e conexão com o banco
cur.close
conn.close()

