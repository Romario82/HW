from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from db.models_bd import Student, Group, Lecturer, Lessons, Grade
from faker import Faker
import random

fake = Faker("uk_UA")

engine = create_engine("sqlite:///db/university.db")
Session = sessionmaker(bind=engine)
session = Session()

def data_db():
    group_names = ["Group A", "Group B", "Group C"]
    groups = [Group(groups_name=name) for name in group_names]
    session.add_all(groups)
    session.commit()

    lecturer_names = [fake.name() for _ in range(5)]
    lecturers = [Lecturer(lecturer_name=name) for name in lecturer_names]
    session.add_all(lecturers)
    session.commit()

    lesson_names = ['Math', 'Physics', 'Computer Science', 'History', 'Literature']
    for lecturer in lecturers:
        lesson = Lessons(lessons_name=random.choice(lesson_names), lecturer=lecturer)
        session.add(lesson)
    session.commit()

    for _ in range(30):
        student = Student(student_name=fake.name(), group=random.choice(groups))
        session.add(student)
    session.commit()

    for student in session.query(Student).all():
        for lesson in session.query(Lessons).all():
            for _ in range(20):
                grade = Grade(value=random.randint(2, 5), student=student, lessons=lesson)
                session.add(grade)
    session.commit()
    return 'База даних заповнена!'


if __name__ == '__main__':
    result = data_db()
    print(result)