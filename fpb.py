import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

cursor=conn.cursor()

#cursor.execute('INSERT INTO fpb(id) VALUES (7437246);')
cursor.execute('DELETE FROM fpb;')

conn.commit()
