import pymssql

conn = pymssql.connect(host='GUILHERME', user='roquec', password='roquec', database='DAS5316', as_dict=False,
                       charset='UTF-8')

cur = conn.cursor()

def create_table():
    cur.execute("CREATE TABLE IF NOT EXISTS Alunos(Nome TEXT, Matrícula REAL, Idade INTEGER, Ingresso INTEGER, Situação TEXT )")

def data_entry():
    cur.execute("INSERT INTO Alunos VALUES('Henrique',11202989,26,2011,'Cursando')")

create_table()
data_entry()

conn.commit()
cur.close()
conn.close()
