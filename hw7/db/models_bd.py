from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    student_name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))

    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    groups_name = Column(String, nullable=False)

    students = relationship("Student", back_populates="group")

class Lecturer(Base):
    __tablename__ = 'lecturer'
    id = Column(Integer, primary_key=True)
    lecturer_name = Column(String, nullable=False)

    lessons = relationship("Lessons", back_populates="lecturer")

class Lessons(Base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True)
    lessons_name = Column(String, nullable=False)
    lecturer_id = Column(Integer, ForeignKey('lecturer.id'))

    lecturer = relationship("Lecturer", back_populates="lessons")
    grades = relationship("Grade", back_populates="lessons")

class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'))
    lessons_id = Column(Integer, ForeignKey('lessons.id'))

    student = relationship("Student", back_populates="grades")
    lessons = relationship("Lessons", back_populates="grades")

def create_db():
    url_bd = 'sqlite:///university.db'
    engine = create_engine(url_bd)
    Base.metadata.create_all(engine)
    return 'База даних створена!'

if __name__ == '__main__':
    result = create_db()
    print(result)
