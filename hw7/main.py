from sqlalchemy import func
from seed import session
from db.models_bd import Student, Group, Lecturer, Lessons, Grade
import os

def query_1():
    print("5 студентів із найбільшим середнім балом:")
    result = session.query(Student, func.avg(Grade.value).label('avg_grade')) \
        .join(Grade).group_by(Student.id) \
        .order_by(func.avg(Grade.value).desc()) \
        .limit(5).all()

    for student, avg_grade in result:
        print(f"Студент: {student.student_name}, -  {avg_grade}")

def query_2():
    print("Студент із найвищим середнім балом з певного предмета")
    subject_name = "Math"
    result = session.query(Student, func.avg(Grade.value).label('avg_grade')) \
        .join(Grade).join(Lessons) \
        .filter(Lessons.lessons_name == subject_name) \
        .group_by(Student.id) \
        .order_by(func.avg(Grade.value).desc()) \
        .first()

    if result:
        student, avg_grade = result
        print(f"Студент: {student.student_name}, предмет {subject_name} - {avg_grade}")

def query_3():
    print("Середній бал у групах з певного предмета (Фізика).")

    subject_name = "Physics"
    result = session.query(Group.groups_name, func.avg(Grade.value).label('avg_grade')) \
    .select_from(Group) \
    .join(Student, Group.id == Student.group_id) \
    .join(Grade, Student.id == Grade.student_id) \
    .join(Lessons, Grade.lessons_id == Lessons.id) \
    .filter(Lessons.lessons_name == subject_name) \
    .group_by(Group.groups_name) \
    .all()

    for group_name, avg_grade in result:
        print(f"Група: {group_name}, Предмет: {subject_name}, Середній бал: {avg_grade:.2f}")

def query_4():
    print("Середній бал на потоці (по всій таблиці оцінок).")
    result = session.query(func.avg(Grade.value)).scalar()
    print(f"Середній бал на потоці: {result:.2f}")

def query_5():
    print("Курси читає певний викладач (наприклад, викладач із ID 2)).")
    #lecturer_name = "Леонід Якименко"
    result = session.query(Lecturer, Lessons) \
                       .join(Lessons) \
                       .filter(Lecturer.id == 2) \
                       .all()

    for lecturer, lesson in result:
        print(f"Викладач: {lecturer.lecturer_name}, курс: {lesson.lessons_name}")

def query_6():
    print("Список студентів у певній групі (наприклад, група з ID 2)")
    result = session.query(Student).join(Group).filter(Group.id == 2).all()
    for student in result:
        print(student.student_name)

def query_7():
    print("Оцінки студентів у окремій групі з певного предмета (наприклад, група з ID 1, предмет із ID 2)")

    result = session.query(Student.student_name, Group.groups_name, Lessons.lessons_name, Grade.value) \
        .join(Group).join(Grade).join(Lessons) \
        .filter(Group.id == 1, Lessons.id == 2).all()
    for student_name, group_name, lessons_name, grade_value in result:
        print(f"Студент: {student_name}, Група: {group_name}, Предмет: {lessons_name}, Оцінка: {grade_value}")

def query_8():
    print("Середній бал, який ставить певний викладач зі своїх предметів (викладач із ID 1)")

    result = session.query(Lecturer.lecturer_name, Lessons.lessons_name,
                  func.avg(Grade.value).label('avg_grade')) \
                .select_from(Lecturer) \
                .join(Lessons).join(Grade).filter(Lecturer.id == 1) \
                .group_by(Lecturer.lecturer_name, Lessons.lessons_name).all()

    for lecturer_name, lessons_name, avg_grade in result:
        print(f"Викладач: {lecturer_name}, Предмет: {lessons_name}, Середній бал: {avg_grade:.2f}")

def query_9():
    print("Список курсів, які відвідує певний студент (наприклад, студент із ID 10)")
    student = session.get(Student, 10)
    result = {grade.lessons.lessons_name for grade in student.grades}
    for course in result:
        print(course)

def query_10():
    print("Список курсів, які студенту читає певний викладач (студент з ID 20 та викладач з ID 3)")

    student = session.get(Student, 20)
    lecturer = session.get(Lecturer, 3)
    result = {grade.lessons.lessons_name for grade in student.grades if
                        grade.lessons.lecturer == lecturer}
    for course in result:
        print(f"Student: {student.student_name}, Lecturer: {lecturer.lecturer_name}, Lesson: {course}")



def no_query_bd():
    print('No command!!! Введіть номер запроса від 1 до 10 або exit')

def query_bd(n):
    query_nomber = {'1': query_1, '2': query_2, '3': query_3, '4': query_4, '5': query_5, '6': query_6, '7': query_7, '8': query_8, '9': query_9, '10': query_10,}
    query_nomber.get(n, no_query_bd) and query_nomber.get(n, no_query_bd)()

def main():
    db_path = os.path.join("db", "university.db")
    if os.path.isfile(db_path):
        print("База даних готова до роботи.")
    else:
        print("База даних не створена")

    while True:
        n = input("Введіть номер запроса від 1 до 10 або exit >>> ")
        if n == "exit":
            break
        else:
            query_bd(n)
    print("EXIT")


if __name__ == '__main__':
    main()



