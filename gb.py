#!/usr/bin/python
import psycopg2


def main():
    conn_string = "host='ec2-75-101-138-26.compute-1.amazonaws.com' dbname='d3qk68q18jl2dl' user='oklxncuvckroyk' password='1267be3ab42456adf92e9d28c88769112a51e3747c7cace34d8235fc6dd8f253' port='5432'"
    # print the connection string we will use to connect
    print("Connecting to database\n	->%s" % conn_string)

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()

    # execute our Query
    cursor.execute("SELECT * FROM historico")

    # retrieve the records from the database
    records = cursor.fetchall()

    # print out the records using pretty print
    # note that the NAMES of the columns are not shown, instead just indexes.
    # for most people this isn't very useful so we'll show you how to return
    # columns as a dictionary (hash) in the next example.
    print(records)
    conn.close()

if __name__ == "__main__":
    main()