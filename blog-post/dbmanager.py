#!/usr/bin/python3
from db import connect, cursor

class DbManager:
    
    def __init__(self):
        user_query = f'''
                CREATE TABLE IF NOT EXISTS users (
                    user_id VARCHAR(255) NOT NULL UNIQUE,
                    username VARCHAR(255) NOT NULL UNIQUE,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    password VArCHAR(20) NOT NULL,
                    created_at DATE DEFAULT CURRENT_DATE,
                    updated_at DATE DEFAULT CURRENT_DATE
                )
                '''
        post_query = '''
                CREATE TABLE IF NOT EXISTS posts (
                    post_id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    content TEXT NOT NULL,
                    user_id VARCHAR(255) NOT NULL,
                    created_at DATE DEFAULT CURRENT_DATE,
                    updated_at DATE DEFAULT CURRENT_DATE,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
                '''
        cursor.execute(user_query)
        cursor.execute(post_query)
        connect.commit()

    # user functions
    def insert_user(self, user_id, user_name, email, password):
        try:
            cursor.execute('INSERT INTO users (user_id, username, email, password) values (%s, %s, %s, %s)', (user_id,user_name, email, password))
            connect.commit()
            return cursor.rowcount
        except Exception as e:
            print('insert user error: ', e)
    
    def get_user(self, email, password):
        try:
            cursor.execute('SELECT * FROM users WHERE email=%s and password=%s', (email, password))
            return cursor.fetchone()
        except Exception as e:
            print('insert user error: ', e)


    def update_user(self, user_id, username, email, password):
        try:
            cursor.execute('UPDATE users SET username=%s, email=%s, password=%s where user_id=%s', (user_id, username, email, password))
            connect.commit()
        except Exception as e:
            print('update user error: ', e)

    def delete_user(self, user_id):
        try:
            cursor.execute('delete from users where user_id=%s', (user_id))
            connect.commit()
        except Exception as e:
            print('delete user error: ', e)

    # user functions
    def insert_post(self, title, content, user_id):
        try:
            cursor.execute('INSERT INTO posts (title, content, user_id) values (%s, %s, %s)', (title, content, user_id))
            connect.commit()
            return cursor.rowcount
        except Exception as e:
            connect.rollback()
            print('error: ', e)

    def get_all_posts(self):
        try:
            cursor.execute('select * from posts p join users u on p.user_id=u.user_id')
            connect.commit()
            return cursor.fetchall()
        except Exception as e:
            print('error: ', e)

    def update_post(self, post_id, title, content, user_id):
        try:
            cursor.execute('UPDATE posts SET title=%s, content=%s WHERE post_id=%s AND user_id=%s', (title, content, post_id, user_id))
            connect.commit()
        except Exception as e:
            connect.rollback()
            print('error: ', e)

    def delete_post(self, post_id, user_id):
        try:
            cursor.execute('DELETE FROM posts WHERE post_id=%s and user_id=', (post_id, user_id))
            connect.commit()
        except Exception as e:
            print('error: ', e)

    def save(self):
        connect.commit()

dbManager = DbManager()