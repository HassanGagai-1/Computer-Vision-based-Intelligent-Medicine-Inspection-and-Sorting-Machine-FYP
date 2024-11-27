import psycopg2

from models.users import User


def deb_conn():
    return psycopg2.connect(database='postgres', user='postgres', password='12345', host='localhost', port='5432')

def get_all_users():
    conn = deb_conn()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM users''');
    data = cur.fetchall()
    cur.close()
    conn.close()
    
    users = [User(id=user[0], firstname=user[1], lastname=user[2], email=user[3], password=[4]) for user in data]
    return users


def insert_user(firstname, lastname, email, password):
    conn = deb_conn()
    cur = conn.cursor()
    cur.execute('''INSERT INTO users(firstname, lastname, email, password) VALUES (%s, %s, %s, %s)''');
    new_user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    
    return new_user_id

