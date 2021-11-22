import os
import psycopg2

DATABASE_URL = os.environ['postgres://mxyqaquulvmnyl:7c939bb8e7a76ef0a196a873ca37bf38ca2288e9b1bd270ea0194774e0e59329@ec2-54-155-200-16.eu-west-1.compute.amazonaws.com:5432/d348v205q9ut8n']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

cursor=conn.cursor()

cursor.execute('INSERT INTO fpb(id) VALUES (6357);')

conn.commit()