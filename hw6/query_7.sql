SELECT students.students, grades.grade, grades.date_received, lessons.lessons FROM grades INNER JOIN students ON students.id = grades.student_id INNER JOIN lessons ON grades.lessons_id = lessons.id WHERE students.group_id = 1 AND grades.lessons_id = 5;