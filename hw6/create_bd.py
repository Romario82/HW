import sqlite3
from faker import Faker
import random


fake = Faker("uk_UA")

def create_bd():
    conn = sqlite3.connect(r'university.db')
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS students(
                   id INTEGER PRIMARY KEY,
                   students TEXT,
                   group_id INTEGER);
                   """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS groups(
                   id INTEGER PRIMARY KEY,
                   groups TEXT);
                    """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS lecturer(
                   id INTEGER PRIMARY KEY,
                   lecturer TEXT);
                   """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS lessons(
                   id INTEGER PRIMARY KEY,
                   lessons TEXT,
                   lecturer_id INTEGER);
                   """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS grades (
                   id INTEGER PRIMARY KEY,
                   student_id INTEGER,
                   lessons_id INTEGER,
                   grade INTEGER,
                   date_received TEXT);
                       """)
    conn.commit()
#-----------------------------------------------------------------------------------------
    groups = ['Group A', 'Group B', 'Group C']
    for group_name in groups:
        cursor.execute('INSERT INTO groups (groups) VALUES (?)', (group_name,))
    conn.commit()
# -----------------------------------------------------------------------------------------
    for _ in range(30):
        students = fake.name()
        group_id = random.randint(1, len(groups))
        cursor.execute('INSERT INTO students (students, group_id) VALUES (?, ?)',
                       (students, group_id))
    conn.commit()
# -----------------------------------------------------------------------------------------
    for student_id in range(1, 31):
        for lessons_id in range(1, 6):
            grade = random.randint(3, 13)
            date_received = fake.date_between(start_date='-4d', end_date='today')
            cursor.execute('INSERT INTO grades (student_id, lessons_id, grade, date_received) VALUES (?, ?, ?, ?)',
                           (student_id, lessons_id, grade, date_received))
    conn.commit()
# -----------------------------------------------------------------------------------------
    lecturers = [(fake.name()) for _ in range(5)]
    for lecturer in lecturers:
        cursor.execute('INSERT INTO lecturer (lecturer) VALUES (?)', (lecturer,))
    conn.commit()
# -----------------------------------------------------------------------------------------
    lessons = [('Math', 1), ('Physics', 2), ('Computer Science', 3), ('History', 4), ('Literature', 5)]
    for lessons in lessons:
        cursor.execute('INSERT INTO lessons (lessons, lecturer_id) VALUES (?, ?)', lessons)
    conn.commit()
#-----------------------------------------------------------------------------------------
    conn.close()
    return "База даних создана. Можна працювати!"

if __name__ == '__main__':
    create_bd()