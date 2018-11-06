import sqlite3
import pymssql

conn = sqlite3.connect('aula.db')
c = conn.cursor()

def read_from_db():

    c.execute('SELECT * FROM Alunos')
    data = c.fetchall()
    for row in data:
        print(row)

    c.execute('SELECT Ingresso FROM Alunos WHERE idade > 20')
    data = c.fetchall()
    for row in data:
        print(row)

read_from_db()

c.close
conn.close()


# ---------------------------------------------------------------------------------------------------------------- #
value = []
timestamp = []
for row in cur:
    value.append(row[1])
    timestamp.append(row[2])