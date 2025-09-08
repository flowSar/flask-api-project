#!/usr/bin/python3
import psycopg2
from psycopg2.extras import RealDictCursor


# replace all these data with your own database data
connect = psycopg2.connect(
    user="sardb",
    password="password", 
    host="localhost",
    port="5433", # default port of postgres is 5432
    database="blog_post",
    cursor_factory=RealDictCursor
)

cursor = connect.cursor()
