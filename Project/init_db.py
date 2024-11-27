import psycopg2

conn = psycopg2.connect(database='postgres', user='postgres', password='12345', host='localhost', port='5432')


cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY, firstName varchar(50), lastName varchar(50), email varchar(255), password varchar(255)) ''');

conn.commit()

cur.close()
conn.close()