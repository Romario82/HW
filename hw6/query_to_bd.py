import sqlite3
from sqlite3 import DatabaseError

def query(n):
    with open(f"query_{int(n)}.sql") as file:
        query_file = file.read()
        try:
            conn = sqlite3.connect(r'university.db')
            cursor = conn.cursor()
            cursor.execute(query_file)
            result = cursor.fetchall()
            conn.close()
            return result
        except DatabaseError:
            return 'DatabaseError'
if __name__ == '__main__':
    query("2")