import query_to_bd
import create_bd
import os


def query_1(n):
    print("5 студентів із найбільшим середнім балом:")
    result = query_to_bd.query(n)
    if result == 'DatabaseError':
        print('DatabaseError')
    else:
        for student_id, avg_grade in result:
            print(f"Студент - {student_id}: Середній бал - {avg_grade:.1f}")

def query_2(n):
    print("Студент із найвищим середнім балом з певного предмета")
    result = query_to_bd.query(n)[0]
    if result == 'DatabaseError':
        print('DatabaseError')
    else:
        print(f"\n Студент із найвищим середнім балом з математики - {result[0]}:  Середній бал  - {result[1]:.1f}")

def query_3(n):
    print("Середній бал у групах з певного предмета (математика).")
    result = query_to_bd.query(n)
    if result == 'DatabaseError':
        print('DatabaseError')
    else:
        for groups, avg_grade in result:
            print(f"Група {groups}: Середній бал - {avg_grade:.2f}")

def query_4(n):
    print("Середній бал на потоці (по всій таблиці оцінок).")
    result = query_to_bd.query(n)[0]
    if result == 'DatabaseError':
        print('DatabaseError')
    else:
        print(f"\nСередній бал на потоці: {result[0]:.1f}")

def query_5(n):
    print("Курси читає певний викладач (наприклад, викладач із ID 3)).")
    result = query_to_bd.query(n)[0]
    if result == 'DatabaseError':
        print('DatabaseError')
    else:
        for course in result:
            print(course)

def query_6(n):
    print("Список студентів у певній групі (наприклад, група з ID 2)")
    result = query_to_bd.query(n)
    if result == 'DatabaseError':
        print('DatabaseError')
    else:
        for student, group in result:
            print(f"{student} - {group}")

def query_7(n):
    print("Оцінки студентів у окремій групі з певного предмета (наприклад, група з ID 1, предмет із ID 5)")
    result = query_to_bd.query(n)
    if result == 'DatabaseError':
        print('DatabaseError')
    else:
        for student, grades, data, lessons in result:
            print(f"{lessons}: {student} - {grades}, {data}")

def query_8(n):
    print("Середній бал, який ставить певний викладач зі своїх предметів (викладач із ID 1)")
    result = query_to_bd.query(n)[0]
    grades, lessons, lecturer = result
    if result == 'DatabaseError':
        print('DatabaseError')
    else:
        print(f"\nСередній бал з {lessons}, читаним викладачем {lecturer}: {grades:.1f}")

def query_9(n):
    print("Список курсів, які відвідує певний студент (наприклад, студент із ID 10)")
    result = query_to_bd.query(n)
    if result == 'DatabaseError':
        print('DatabaseError')
    else:
        for course in result:
            print(course[0])

def query_10(n):
    print("Список курсів, які студенту читає певний викладач (студент з ID 20 та викладач з ID 3)")
    result = query_to_bd.query(n)
    if result == 'DatabaseError':
        print('DatabaseError')
    else:
        for course in result:
            print(course[0])

def no_query_bd(_):
    print('No command!!! Введіть номер запроса від 1 до 10 або exit')


def query_bd(n):
    query_nomber = {'1': query_1, '2': query_2, '3': query_3, '4': query_4, '5': query_5, '6': query_6, '7': query_7, '8': query_8, '9': query_9, '10': query_10,}
    query_nomber.get(n, no_query_bd) and query_nomber.get(n, no_query_bd)(n)

def main():
    if not os.path.exists('university.db'):
        result = create_bd.create_bd()
        print(result)
    else:
        print("База даних готова до роботи")
    while True:
        n = input("Введіть номер запроса від 1 до 10 або exit >>> ")
        if n == "exit":
            break
        else:
            query_bd(n)
    print("EXIT")


if __name__ == '__main__':
    main()


