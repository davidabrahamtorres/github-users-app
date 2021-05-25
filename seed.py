import sqlite3
from sqlite3 import Error
from github import Github
import argparse

def create_table():
    conn = None
    try:
        conn = sqlite3.connect('GitUsersDb.db')
        cursor = conn.cursor()
        create_table = '''CREATE TABLE USERS
                        ([id] INTEGER PRIMARY KEY,
                        [user_name] text, 
                        [image_url] text, 
                        [type] text,
                        [github_url] text)'''
        cursor.execute(create_table)
        conn.commit()
        cursor.close()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            print("GitUsersDb created successfully")

def insert_table(record_list):
    conn = None
    try:
        conn = sqlite3.connect('GitUsersDb.db')
        cursor = conn.cursor()
        insert_table = '''INSERT INTO USERS
                        (id, user_name, image_url, type, github_url)
                        VALUES (?, ?, ?, ?, ?);'''
        cursor.executemany(insert_table, record_list)
        conn.commit()
        print("Total", cursor.rowcount, "records inserted successfully into GitUsersDb")
        cursor.close()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def get_users(num_users):
    # Using an access token
    try:
        access_token='USE_YOUR_VALID_TOKEN'
        total_users = num_users

        g = Github(access_token)
        users = g.get_users()

        record_list = [[] for i in range(total_users)]

        for i in range(total_users):
            record_list[i].append(users[i].id)
            record_list[i].append(users[i].name)
            record_list[i].append(users[i].avatar_url)
            record_list[i].append(users[i].type)
            record_list[i].append(users[i].html_url)
            record_list[i] = tuple(record_list[i])

    except Error as e:
        print(e)
    finally:
        print("Users information pulled successfully")

    return record_list

def main(num_users):
    create_table()
    record_list = get_users(num_users)
    insert_table(record_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--total', default= 150, type=int)
    args = parser.parse_args()
    main(args.total)
