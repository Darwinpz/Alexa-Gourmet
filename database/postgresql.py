import psycopg2
import os

conn = psycopg2.connect(host='localhost',
                       dbname='alexa_gourmet',
                       user='postgres',
                       password='123',
                       port='5432'
)
